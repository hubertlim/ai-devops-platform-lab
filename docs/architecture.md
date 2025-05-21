# Architecture Decision Records

## ADR-001: Mock AI Provider as Default

**Status**: Accepted

**Context**: The platform needs to demonstrate AI integration without requiring paid API keys or external dependencies for local development and CI.

**Decision**: Ship with a mock AI provider as the default. The provider interface is pluggable, allowing real providers (OpenAI, Anthropic, Ollama) to be swapped in via environment variable.

**Consequences**:
- Local development works without any API keys
- CI/CD pipeline can test the full request flow
- Real providers can be added without changing application code
- Mock responses are deterministic, enabling reliable testing

---

## ADR-002: Monorepo Structure

**Status**: Accepted

**Context**: The project includes frontend, backend, infrastructure, and observability configs. We need a structure that supports independent development while maintaining cohesion.

**Decision**: Use a monorepo with clear directory boundaries (`apps/`, `infra/`, `observability/`).

**Consequences**:
- Single repository for all components
- Shared CI/CD pipeline
- Atomic commits across frontend + backend
- Clear ownership boundaries via directory structure

---

## ADR-003: OpenTelemetry over Vendor-Specific SDKs

**Status**: Accepted

**Context**: Observability instrumentation should be portable across backends (Jaeger, Datadog, New Relic, etc.).

**Decision**: Use OpenTelemetry SDK and Collector as the instrumentation layer. Export to Prometheus for metrics.

**Consequences**:
- Vendor-neutral instrumentation
- Can switch observability backends without code changes
- Collector handles batching, retry, and export
- Slightly more complex local setup (collector container)

---

## ADR-004: Kustomize over Helm for Kubernetes

**Status**: Accepted

**Context**: Need environment-specific Kubernetes configurations (staging vs production).

**Decision**: Use Kustomize with base + overlays pattern. Helm is overkill for this project's scope.

**Consequences**:
- No template engine complexity
- Native kubectl support (`kubectl apply -k`)
- Clear diff between environments
- Easy to migrate to Helm later if needed

---

## ADR-005: GitHub Actions with Minimal Permissions

**Status**: Accepted

**Context**: CI/CD pipelines are a common attack vector. We need to demonstrate security-conscious pipeline design.

**Decision**: Every GitHub Actions job declares explicit `permissions:` blocks with the minimum required access.

**Consequences**:
- Reduced blast radius if a dependency is compromised
- Explicit documentation of what each job can access
- Slightly more verbose workflow files
- Aligns with OpenSSF Scorecard requirements
