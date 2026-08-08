# VKS Secret Store Demo

A minimal VMware VCF 9 / VKS demo showing:

- VKS workload cluster
- Argo CD GitOps deployment
- Flask sample application
- PostgreSQL
- VCF Secret Store Service / OpenBao for credentials
- Secret value used by the application without storing the real credential in Git

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
              +------ secret ------> Flask App
                                      |
                                      v
                                  PostgreSQL
```

## GitOps flow

```text
Git -> Argo CD -> VKS -> Flask/PostgreSQL

VCF Secret Store Service -> secret -> workload
```

The application manifests intentionally do not contain the production secret value. Configure the VCF 9 Secret Store Service separately, then wire the resulting secret into the workload using the supported Secret Store integration for the installed VCF/VKS version.

## Repository layout

```text
app/
  app.py
  requirements.txt
  Dockerfile
k8s/
  namespace.yaml
  postgres.yaml
  app.yaml
  service.yaml
argocd/
  application.yaml
secret-store/
  README.md
```

## Prerequisites

- VMware Cloud Foundation 9.x
- vSphere Supervisor with Secret Store Service enabled
- VKS cluster
- Argo CD installed in the VKS cluster
- A container registry accessible by the VKS nodes

## Deploy with Argo CD

Edit `argocd/application.yaml` and set `repoURL` to this repository. Then:

```bash
kubectl apply -f argocd/application.yaml
```

Argo CD will synchronize the application manifests into the `demo` namespace.

## Secret Store

See `secret-store/README.md` for the VCF Secret Store setup. The exact Secret Store API/CRD should match the Secret Store Service version installed on the Supervisor; do not substitute a generic Kubernetes Secret for the production flow.
