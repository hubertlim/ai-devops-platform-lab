# Deployment Guide

## Environments

| Environment | Infrastructure | Deployment Method | Auto-sync |
|-------------|---------------|-------------------|-----------|
| Local | docker-compose | `make up` | N/A |
| Staging | EKS (Terraform) | Argo CD (auto) | Yes |
| Production | EKS (Terraform) | Argo CD (manual) | No |

## Local Development

```bash
cp .env.example .env
make up
```

Services:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Grafana: http://localhost:3001
- Prometheus: http://localhost:9090

## Staging Deployment

Staging auto-deploys when changes merge to `main`:

1. CI pipeline builds and pushes images to GHCR
2. Argo CD detects new image tags
3. Argo CD syncs Kubernetes manifests from `infra/k8s/overlays/staging/`
4. Rolling update with health checks

## Production Deployment

Production requires manual approval:

1. CI pipeline builds and pushes images (same as staging)
2. Argo CD detects drift but does NOT auto-sync
3. Engineer reviews changes in Argo CD UI
4. Manual sync triggers rolling update
5. Rollback available via Argo CD revision history

## Infrastructure Provisioning

```bash
# Initialize Terraform
cd infra/terraform
terraform init

# Plan for staging
terraform plan -var-file=environments/staging.tfvars -out=tfplan

# Apply (requires AWS credentials)
terraform apply tfplan
```

## Rollback

### Application Rollback (Argo CD)
```bash
argocd app rollback ai-platform-staging
```

### Infrastructure Rollback (Terraform)
```bash
# Revert to previous state
git revert <commit>
# Argo CD will auto-sync the reverted manifests
```
