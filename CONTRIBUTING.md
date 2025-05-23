# Contributing

Thanks for your interest in this project. This is a portfolio repository, so contributions are welcome but the scope is intentionally narrow.

## Development setup

```bash
cp .env.example .env
make up           # starts the full stack
make test         # runs backend + frontend tests
make lint         # runs Ruff and ESLint
```

See the [README](README.md#local-quickstart) for full quickstart details.

## Branching

- `main` is the default branch and is auto-deployed to staging via Argo CD.
- Create feature branches from `main`: `feat/<short-description>` or `fix/<short-description>`.
- Open PRs against `main`. Direct pushes to `main` are discouraged.

## Commit messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>

<optional body>
```

Common types: `feat`, `fix`, `chore`, `docs`, `test`, `ci`, `refactor`.

Examples:
- `feat(api): add Anthropic provider`
- `fix(ci): cache Python dependencies`
- `docs: clarify deployment model`

## Pull requests

Before opening a PR:
- Run `make lint` and `make test` locally and ensure both pass.
- Update documentation if behavior changes.
- Add or update tests for new functionality.
- Keep PRs focused. One concern per PR is much easier to review.

CI must pass before merge. The pipeline runs lint, tests, security scans, and container builds.

## Reporting bugs

Open an issue using the bug report template. Include:
- What you expected
- What actually happened
- Steps to reproduce
- Environment (OS, Docker version, etc.)

## Reporting security issues

Do not open a public issue. See [SECURITY.md](SECURITY.md) for the disclosure process.

## Code style

- **Python**: Ruff handles linting and import order. 100-character line limit.
- **TypeScript**: ESLint with TypeScript and React Hooks plugins. Strict mode enabled.
- **YAML**: Two-space indentation.
- **Markdown**: Reference-style links for long URLs.
