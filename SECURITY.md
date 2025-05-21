# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.x.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in this project, please report it responsibly.

### How to Report

1. **Do NOT** open a public GitHub issue for security vulnerabilities.
2. Email your findings via [GitHub Security Advisories](https://github.com/hubertlim/ai-devops-platform-lab/security/advisories/new) or open a private vulnerability report.
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 48 hours of your report.
- **Assessment**: We will evaluate the severity within 5 business days.
- **Resolution**: Critical vulnerabilities will be patched within 7 days. Others within 30 days.
- **Disclosure**: We will coordinate disclosure timing with you.

### Scope

The following are in scope:
- Application code in `apps/`
- Docker configurations
- CI/CD pipeline configurations
- Infrastructure-as-code in `infra/`

The following are out of scope:
- Third-party dependencies (report to upstream maintainers)
- Issues in development-only tooling that don't affect production

## Security Practices

This project implements:
- Dependency scanning (pip-audit, npm audit)
- Container image scanning (Trivy)
- Static analysis (CodeQL)
- OpenSSF Scorecard monitoring
- Least-privilege CI/CD permissions
- No secrets in version control
- Structured logging without sensitive data exposure

## Secrets Handling

- All secrets are managed via environment variables
- `.env` files are gitignored
- `.env.example` contains only placeholder values
- CI/CD secrets use GitHub's encrypted secrets
- No API keys, tokens, or credentials are committed
