# 🤝 Contributing to CodeSnippet Pro

Thank you for your interest in contributing to CodeSnippet Pro! We welcome contributions from the community.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/snippet-manager-pro.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
5. Install development dependencies: `pip install -e ".[dev]"`

## 📝 Code Style

We use:
- **Black** for code formatting
- **flake8** for linting
- **mypy** for type checking

Run before committing:
```bash
make format  # Format code with black
make lint    # Run linters
make test    # Run tests
```

## 🐛 Reporting Bugs

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## 💡 Feature Requests

We love new ideas! Please open an issue with:
- Clear description of the feature
- Use cases
- Potential implementation approach (optional)

## 🔄 Pull Request Process

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass: `make test`
5. Update documentation if needed
6. Commit with clear messages following conventional commits
7. Push to your fork
8. Open a Pull Request

## 🏷️ Commit Message Format

We follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build/tooling changes

Example: `feat: add fuzzy search capability`

## 📜 Code of Conduct

Be respectful, constructive, and inclusive in all interactions.

Thank you for contributing! 🎉
