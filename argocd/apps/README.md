# Argo CD App-of-Apps

`argocd/root/application.yaml` is the bootstrap/root Application. It watches this directory and creates child Applications.

Current child application:

- `demo.yaml` -> deploys `k8s/` into the `demo` namespace

The AppProject is created separately from `argocd/project/vks-demo-project.yaml`.
