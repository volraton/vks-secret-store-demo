# Optional Pinniped Add-on

This directory documents Pinniped as an **optional identity/authentication demo** for the VKS cluster.

It is intentionally separate from the core Secret Store + Argo CD + Load Balancer sample.

## What Pinniped demonstrates

```text
User
  |
  v
OIDC Identity Provider
  |
  v
Pinniped
  |
  v
VKS Kubernetes API
  |
  +--> Kubernetes RBAC
  +--> Argo CD
  +--> Workload administration
```

The conceptual split is:

```text
Pinniped       = Who are you?
Secret Store   = Which workload secrets can be accessed?
Argo CD        = What should be deployed?
Load Balancer  = How does a client reach the application?
```

## Why it is optional

Pinniped configuration depends on the Kubernetes/VKS release and the identity provider used by the environment. This sample therefore does **not** hard-code an IdP client secret, issuer URL, certificate, or production identity configuration.

The core demo remains fully independent of Pinniped.

## Example IdP

A lab can use an OIDC provider such as Microsoft Entra ID, provided the tenant/application is configured according to the Pinniped and VKS documentation for the installed release.

Typical values are represented as placeholders:

```yaml
identityProvider:
  issuer: https://<OIDC-ISSUER>
  clientID: <OIDC-CLIENT-ID>
  clientSecret: <OIDC-CLIENT-SECRET>
```

Do not commit a real `clientSecret` to Git.

## Recommended demo sequence

1. Deploy the core VKS Secret Store demo.
2. Verify Flask through the Foundation Load Balancer.
3. Install/configure Pinniped for the VKS release.
4. Configure the OIDC identity provider.
5. Authenticate a non-admin user.
6. Apply Kubernetes RBAC to the user/group.
7. Demonstrate allowed and denied access to the `demo` namespace.

## Example RBAC concept

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: demo-readonly
  namespace: demo
rules:
  - apiGroups: [""]
    resources: ["pods", "services"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: demo-readonly
  namespace: demo
subjects:
  - kind: Group
    name: vks-demo-users
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: demo-readonly
  apiGroup: rbac.authorization.k8s.io
```

The group name is illustrative and must match the claims/group mapping configured in the actual identity provider and Pinniped setup.

## Security notes

- Keep IdP client secrets outside Git.
- Use a dedicated lab identity/application registration.
- Use least-privilege Kubernetes RBAC.
- Do not use the `administrator@vsphere.local` account for the end-user authentication demo.
- Pinniped is an identity/authentication layer; it does not replace VCF Secret Store Service.
