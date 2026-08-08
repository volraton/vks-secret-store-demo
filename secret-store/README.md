# VCF Secret Store Service

This directory documents the secret side of the demo.

## Lab secret

```text
username: demo
password: VMware123!
```

Store these values in the **VCF 9 Secret Store Service** rather than committing them to Git.

Recommended logical secret:

```text
secret: demo/database
  username = demo
  password = VMware123!
```

The application should receive the secret through the supported Secret Store integration for the Secret Store Service version installed on the Supervisor.

## Important

Secret Store Service APIs and workload integration details can differ by VCF/Secret Store Service release. Use the CRDs and commands exposed by the installed VCF 9.x service rather than applying a generic Vault or Kubernetes Secret manifest.

The repository keeps this file intentionally version-neutral so it does not claim an API shape that may not match the installed service.
