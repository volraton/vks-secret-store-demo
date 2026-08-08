# VKS Secret Store Demo

A minimal VMware Cloud Foundation 9 / VKS demo showing:

- VKS workload cluster
- Argo CD GitOps deployment
- Flask sample application
- PostgreSQL
- VCF Secret Store Service / OpenBao as the secret system of record
- External Secrets Operator as the Kubernetes synchronization layer
- Secret rotation without storing the credential in Git

## Demo credential

For this lab only:

```text
Username: demo
Password: VMware123!
```

> This repository is public. `VMware123!` is intentionally a non-production lab password. Never use it in production.

## Architecture

```text
                         VCF 9
                           |
                   vSphere Supervisor
                           |
              +------------+-------------+
              |                          |
      Secret Store Service              VKS
              |                          |
           OpenBao                    Argo CD
              |                          |
              |                    Git repository
              |                          |
              +---- ESO / secret ------> Flask App
                                      |
                                      v
                                  PostgreSQL
```

## GitOps flow

```text
Git -> Argo CD -> VKS -> ExternalSecret -> Kubernetes Secret -> App/PostgreSQL

VCF Secret Store Service -> External Secrets integration -> ExternalSecret
```

The application manifests do not contain the database password. The remote secret is expected to be named `demo-db`, and the Kubernetes-side store is expected to be `ClusterSecretStore/vcf-secret-store`.

## Repository layout

```text
app/
  app.py
  requirements.txt
  Dockerfile

k8s/
  namespace.yaml
  external-secret.yaml
  postgres.yaml
  app.yaml

argocd/
  application.yaml

secret-store/
  README.md

.github/workflows/
  build.yml
```

## Prerequisites

- VMware Cloud Foundation 9.x
- vSphere Supervisor with Secret Store Service enabled
- VKS workload cluster
- Argo CD installed in the VKS cluster
- VKS Secret Store integration/add-on and ESO integration appropriate to your VCF/VKS release
- A container registry accessible by the VKS nodes

## 1. Build the application image

The included GitHub Actions workflow builds and publishes:

```text
ghcr.io/volraton/vks-secret-store-demo:latest
ghcr.io/volraton/vks-secret-store-demo:<commit-sha>
```

If the GHCR package is private, configure an image pull secret in the VKS cluster or make the demo package public for a lab.

## 2. Create the VCF Secret Store secret

In VCF Secret Store Service create:

```text
demo-db
  username = demo
  password = VMware123!
```

Do not commit the value to Git.

## 3. Prepare the VKS secret integration

The repository expects:

```text
ClusterSecretStore/vcf-secret-store
```

to be available in the VKS cluster and to read the `demo-db` secret from the VCF Secret Store integration.

Check the VKS add-on catalog:

```bash
kubectl get addon -A | grep -i secret-store
kubectl get addonrelease -A | grep -i secret-store
```

See `secret-store/README.md` for the version-specific integration notes.

## 4. Deploy Argo CD Application

From a kubeconfig context pointing to the VKS cluster:

```bash
kubectl apply -f argocd/application.yaml
```

Argo CD will synchronize `k8s/` into the `demo` namespace.

## 5. Verify

```bash
kubectl get pods -n demo
kubectl get externalsecret -n demo
kubectl get secret -n demo db-credentials
kubectl get svc -n demo
```

Access the application locally:

```bash
kubectl -n demo port-forward svc/secret-demo 8080:80
```

Open:

```text
http://localhost:8080
```

The page shows the database connection status, but never displays the password.

## 6. Test GitOps

Change the application source or Kubernetes manifest, commit and push to `main`, then watch Argo CD reconcile the change:

```bash
kubectl -n demo rollout status deployment/secret-demo
```

## 7. Test secret rotation

Change the password in VCF Secret Store Service, wait for the configured ESO refresh interval, and verify that `db-credentials` is reconciled. Because this demo injects the secret as environment variables, restart the application and PostgreSQL Pods after rotation:

```bash
kubectl -n demo rollout restart deployment/postgres deployment/secret-demo
kubectl -n demo rollout status deployment/postgres
kubectl -n demo rollout status deployment/secret-demo
```

## Security note

The password in this README is intentionally a disposable lab credential. For production, use a unique random secret and never store it in Git, image layers, Helm values, or Kubernetes manifests.
