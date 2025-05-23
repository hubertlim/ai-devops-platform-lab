# Argo CD Application Manifests

These files declare how Argo CD should deploy this project to a Kubernetes cluster.

## Files

| File | Purpose |
|------|---------|
| `project.yaml` | `AppProject` that restricts what the application can deploy and to which namespace |
| `application.yaml` | `Application` for the staging environment with auto-sync and self-heal |
| `application-production.yaml` | `Application` for production with manual sync (safety gate) |

## Sync model

| Environment | Auto-sync | Self-heal | Prune |
|-------------|-----------|-----------|-------|
| Staging | ✅ | ✅ | ✅ |
| Production | ❌ (manual) | ❌ | ❌ |

Auto-sync on staging means every commit to `main` is deployed automatically. Production requires a human to click "Sync" in Argo CD or run `argocd app sync ai-platform-production`. This pattern catches issues in staging before they reach prod.

## Forking this repository

If you fork this repo, update the `repoURL` in all three files to point to your fork:

```bash
# From the repository root
sed -i '' 's|github.com/hubertlim/ai-devops-platform-lab|github.com/<your-user>/ai-devops-platform-lab|g' infra/argocd/*.yaml
```

Without that, Argo CD will keep syncing the upstream manifests instead of yours.

## Applying the manifests

```bash
# Bootstrap the project and applications (run once per cluster)
kubectl apply -n argocd -f infra/argocd/project.yaml
kubectl apply -n argocd -f infra/argocd/application.yaml
kubectl apply -n argocd -f infra/argocd/application-production.yaml

# Watch sync status
argocd app get ai-platform-staging
argocd app get ai-platform-production
```

## Rollback

Argo CD keeps a history of synced revisions. To roll back:

```bash
argocd app history ai-platform-staging
argocd app rollback ai-platform-staging <revision-id>
```

For production rollback, prefer reverting the offending commit on `main` and letting Argo CD detect the drift, then manually syncing.
