# Deployment Options

![Deployment Options Block Diagram](architecture-options.svg)

The demo is intentionally modular. Choose the deployment model that matches the lab objective.

## Option 1 — Core / Manual

```text
kubectl → VKS → Flask/PostgreSQL
              ↑
       VCF Secret Store
              │
       Foundation LB / VIP
```

Use this for a simple lab or troubleshooting session. Argo CD is not required.

## Option 2 — GitOps App-of-Apps

```text
GitHub → Argo CD Root App → Child App → VKS
                                      │
                                      └→ Flask/PostgreSQL
```

Use this for the recommended production-style demonstration. The AppProject controls repository and destination boundaries, while the App-of-Apps pattern manages child applications.

## Option 3 — Pinniped Identity

```text
User → OIDC IdP → Pinniped → VKS API → Kubernetes RBAC
```

Optional identity/authentication layer. It demonstrates who the user is and what Kubernetes resources the user can access. It does not replace Secret Store Service.

See `../addons/pinniped/README.md`.

## Option 4 — Shared Secret + Network Path

Both GitOps and non-GitOps modes use the same runtime pattern:

```text
VCF Secret Store → ExternalSecret → Kubernetes workload
                                          │
                                          ▼
                              Foundation Load Balancer
                                          │
                                          ▼
                                         Client
```

This makes the architecture easy to explain:

| Concern | Component |
|---|---|
| Identity | Pinniped / OIDC |
| Secrets | VCF Secret Store / OpenBao |
| Deployment | Argo CD or kubectl |
| Runtime | VKS |
| Exposure | VCF Foundation Load Balancer |
| Application | Flask + PostgreSQL |

## Recommended demo sequence

1. Start with Option 1.
2. Add Option 2 to demonstrate GitOps.
3. Add Option 3 if identity/SSO is part of the workshop.
4. Use Option 4 to explain why secret management and network exposure remain independent of the deployment method.
