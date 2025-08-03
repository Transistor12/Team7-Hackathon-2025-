# Contributing to HarvestNet

Thank you for your interest in contributing to HarvestNet! We welcome contributions from developers, agricultural experts, and community members.

## How to Contribute

### 1. Fork the Repository
- Click the "Fork" button at the top right of the repository page
- Clone your fork locally: `git clone https://github.com/yourusername/harvestnet.git`

### 2. Set Up Development Environment
```bash
# Install frontend dependencies
npm install

# Install backend dependencies
pip install -r requirements.txt

# Run tests to ensure everything works
npm test
python test_suite.py
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Your Changes
- Follow our coding standards (see below)
- Write tests for new functionality
- Update documentation if needed

### 5. Test Your Changes
```bash
# Run frontend tests
npm test

# Run backend tests
python test_suite.py

# Run data validation
python data_validation.py
```

### 6. Submit a Pull Request
- Push your changes to your fork
- Create a pull request with a clear description
- Reference any related issues

## Coding Standards

### React/JavaScript
- Use functional components with hooks
- Follow ESLint configuration
- Use meaningful component and variable names
- Write JSDoc comments for complex functions

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all functions
- Handle exceptions gracefully

### CSS
- Use BEM methodology for class naming
- Maintain responsive design principles
- Use CSS custom properties for theming
- Keep specificity low

## Reporting Issues

### Bug Reports
- Use the bug report template
- Include steps to reproduce
- Provide screenshots if applicable
- Specify browser/environment details

### Feature Requests
- Use the feature request template
- Explain the use case and benefits
- Consider implementation complexity
- Discuss with maintainers first for major features

## Development Guidelines

### Commit Messages
Use conventional commit format:
```
feat: add weather alerts functionality
fix: resolve user authentication issue
docs: update API documentation
test: add unit tests for user management
```

### Branch Naming
- `feature/feature-name` for new features
- `fix/bug-description` for bug fixes
- `docs/documentation-update` for documentation
- `test/test-description` for test additions

### Code Review Process
1. All PRs require at least one review
2. Tests must pass before merging
3. Documentation must be updated for new features
4. Consider performance and security implications

## Agricultural Domain Knowledge

We especially welcome contributions from:
- Agricultural experts and extension officers
- Kenyan farmers with platform feedback
- Agricultural technology specialists
- Localization experts (Swahili translation)

## Recognition

Contributors will be recognized in:
- README acknowledgments
- Release notes
- Project documentation
- Annual contributor highlights

## Questions?

- Join our [Discussions](https://github.com/yourusername/harvestnet/discussions)
- Reach out to maintainers
- Check existing issues and documentation

Thank you for helping make agriculture more accessible and efficient for Kenyan farmers!
