# Observability Guide

## Overview

The platform implements the three pillars of observability:

1. **Metrics** — Prometheus counters and histograms exposed at `/metrics`
2. **Traces** — OpenTelemetry spans exported via OTLP to the Collector
3. **Logs** — Structured JSON logs with correlation IDs via structlog

## Correlation Flow

Every request through the system carries a correlation ID:

```
Client (generates UUID) 
  → X-Correlation-ID header 
    → Backend middleware extracts/generates 
      → Attached to log entries 
      → Attached to OpenTelemetry spans 
      → Returned in response header
```

This allows tracing a single request across all observability signals.

## Metrics

### Custom Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `http_requests_total` | Counter | method, endpoint, status_code | Total HTTP requests |
| `http_request_duration_seconds` | Histogram | method, endpoint | Request latency |
| `ai_requests_total` | Counter | provider, status | AI completion requests |
| `ai_request_duration_seconds` | Histogram | provider | AI request latency |

### Accessing Metrics

- **Raw**: `http://localhost:8000/metrics`
- **Prometheus UI**: `http://localhost:9090`
- **Grafana Dashboard**: `http://localhost:3001` (admin/admin)

## Grafana Dashboard

The pre-configured dashboard (`observability/grafana/dashboards/ai-platform-overview.json`) shows:

- Request rate (req/s)
- Request latency (p50, p95)
- AI request count and error rate
- AI latency gauge with thresholds

## Local Development

```bash
# Start the full observability stack
make up

# Generate some traffic
curl -X POST http://localhost:8000/api/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hello"}'

# View metrics
curl http://localhost:8000/metrics

# Open Grafana
open http://localhost:3001
```
