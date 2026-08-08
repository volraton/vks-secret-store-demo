#!/usr/bin/env bash
set -euo pipefail

# Non-GitOps deployment path. Run from the repository root with a kubeconfig
# context pointing at the VKS workload cluster.

kubectl apply -k k8s/
kubectl get pods -n demo
kubectl get externalsecret -n demo 2>/dev/null || true
kubectl get secret -n demo db-credentials 2>/dev/null || true
