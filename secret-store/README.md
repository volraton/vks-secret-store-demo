# VCF 9 Secret Store -> VKS

This demo uses the VCF Secret Store Service as the system of record for credentials and External Secrets Operator (ESO) as the Kubernetes-side synchronization layer.

VMware describes Secret Store Service as a solution for centralized secret management and secure injection into workloads. VCF 9.0 provides Secret Store Service 9.0.0; the service uses OpenBao underneath. citeturn5search0turn4search2

## 1. Create the lab secret

In the VCF 9 Secret Store Service, create a KV secret with the logical name:

```text
 demo-db
```

Values:

```text
username = demo
password = VMware123!
```

Do not put the real value into Git. `VMware123!` is intentionally a lab-only credential.

## 2. Prepare VKS secret integration

The VKS cluster needs the VMware-supported Secret Store integration/add-on and the External Secrets Operator integration appropriate to the installed VKS/VCF versions.

Check the VKS add-on catalog first:

```bash
kubectl get addon -A | grep -i secret-store
kubectl get addonrelease -A | grep -i secret-store
```

VKS exposes a `secret-store` add-on through its add-on framework; the available release is selected by the VKS version and compatibility rules. citeturn6search0

The VCF Supervisor Services catalog also documents Secret Store Service and an External Secrets Operator lab service. citeturn5search0

## 3. Configure the ESO store

The application expects a `ClusterSecretStore` named:

```text
vcf-secret-store
```

The exact provider configuration is intentionally not hard-coded here because it depends on the VCF Secret Store Service/VKS integration version installed in the environment. The important contract for this repository is:

```text
ClusterSecretStore/vcf-secret-store
        |
        +-- remote secret: demo-db
              +-- username
              +-- password
```

Once that integration is configured, `k8s/external-secret.yaml` creates the Kubernetes Secret `demo/db-credentials` from the remote secret.

ESO's role is to read an external provider and materialize a native Kubernetes Secret for workloads; VMware's Supervisor Services catalog documents ESO as the Kubernetes operator for external secret systems. citeturn5search0

## 4. Verify the secret sync

```bash
kubectl get externalsecret -n demo db-credentials
kubectl get secret -n demo db-credentials
```

Expected:

```text
ExternalSecret: Ready=True / SecretSynced
Secret:         db-credentials
```

Do not print the password into terminal output during a real demonstration.

## 5. Secret rotation

Change only the value in VCF Secret Store Service, for example:

```text
password = VMware123!
```

Then wait for the ESO refresh interval (`1m`). The Kubernetes Secret should be reconciled from the external store. If the application consumes the value through environment variables, restart the application Pod to load the new environment value; file-mounted secret consumption has different update semantics.

## Troubleshooting

If the VCF Secret Store Service reports permission errors, check the Supervisor Secret Store Service health and its OpenBao/Kubernetes authentication configuration. Broadcom documents certificate/SAN problems with the Supervisor kube-vip endpoint as one cause of Secret Store permission failures. citeturn4search2
