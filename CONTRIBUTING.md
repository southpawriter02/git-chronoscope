# Contributing

Thank you for your interest in contributing to git-chronoscope!

## Development Setup

```bash
# Clone repository
git clone https://github.com/user/git-chronoscope.git
cd git-chronoscope

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For testing
```

## Running Tests

```bash
python -m unittest discover tests
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes and add tests
4. Run tests (`python -m unittest discover tests`)
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small

## Questions?

Open an issue for questions or discussions.
