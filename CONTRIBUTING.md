# Contributing to NoobBook

Thanks for your interest in contributing to NoobBook!

## Branch Strategy

We use two main branches:

| Branch | Purpose |
|--------|---------|
| `main` | Stable release. Use this to test and play around with NoobBook. |
| `develop` | Latest changes. This is where all new work goes. |

We don't have a separate staging branch yet - `develop` serves as both development and staging for now.

## How to Contribute

1. **Fork the repository**

2. **Pull from `develop`** (not main)
   ```bash
   git checkout develop
   git pull origin develop
   ```

3. **Create your feature branch**
   ```bash
   git checkout -b your-feature-name
   ```

4. **Make your changes**
   - See `CLAUDE.md` for code guidelines
   - Follow existing patterns in the codebase
   - Write tests for new features
   - Run linters and formatters before committing

5. **Push and create a Pull Request to `develop`**
   ```bash
   git push origin your-feature-name
   ```
   Then open a PR targeting the `develop` branch.

## Code Quality Standards

### Backend (Python)
- **Formatting**: Use Black (`black .`)
- **Import sorting**: Use isort (`isort .`)
- **Linting**: Use flake8 (`flake8 .`)
- **Type hints**: Add type hints for function parameters and return values
- **Line length**: Maximum 100 characters

### Frontend (TypeScript/React)
- **Formatting**: Use Prettier (`npm run format`)
- **Linting**: Use ESLint (`npm run lint`)
- **Type checking**: Use TypeScript (`npm run type-check`)
- **Code style**: Follow existing patterns

## Running Tests Locally

### Backend Tests
```bash
cd backend
pip install -r requirements-dev.txt
pytest -v
pytest --cov=app  # with coverage
```

### Frontend Tests
```bash
cd frontend
npm install
npm run test
npm run test:coverage  # with coverage
```

## CI/CD Pipeline

All pull requests must pass CI checks:

### Backend CI
- ✅ Black formatting check
- ✅ isort import sorting check
- ✅ flake8 linting
- ✅ pytest tests with 40% minimum coverage
- Tests run on Python 3.10, 3.11, 3.12

### Frontend CI
- ✅ Prettier formatting check
- ✅ ESLint linting
- ✅ TypeScript type checking
- ✅ Vitest tests with 30% minimum coverage
- ✅ Production build
- Tests run on Node 18.x, 20.x

## Pre-commit Hooks (Optional)

Install pre-commit hooks to automatically check code quality:

```bash
pip install pre-commit
pre-commit install
```

This will run formatters and linters before each commit.

## Important

- PRs to `main` will be rejected
- Always target `develop` for your pull requests
- Keep PRs focused on a single feature or fix
- All CI checks must pass before merge

## Questions?

Open an issue or reach out at [noob@noobbooklm.com](mailto:noob@noobbooklm.com)

