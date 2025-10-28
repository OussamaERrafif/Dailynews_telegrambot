# Contributing to Telegram News Bot

Thank you for considering contributing to the Telegram News Bot! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in your interactions with other contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

1. A clear, descriptive title
2. Steps to reproduce the issue
3. Expected behavior vs actual behavior
4. Your environment (OS, Python version, etc.)
5. Relevant logs or error messages

### Suggesting Enhancements

Enhancement suggestions are welcome! Please open an issue with:

1. A clear description of the enhancement
2. Why this enhancement would be useful
3. Example use cases

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes with clear commit messages
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Dailynews_telegrambot.git
   cd Dailynews_telegrambot
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your test bot token
   ```

5. Create test data:
   ```bash
   cp result.json.example result.json
   ```

## Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Add comments for complex logic

## Testing

Before submitting a pull request:

1. Test your changes manually
2. Ensure no syntax errors: `python3 -m py_compile main.py`
3. Verify all features work as expected
4. Test error handling scenarios

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in present tense (Add, Fix, Update, etc.)
- Keep the first line under 50 characters
- Add detailed description if needed

Examples:
- `Add /status command to check bot health`
- `Fix error handling in article loading`
- `Update README with new configuration options`

## Questions?

If you have questions, feel free to:
- Open an issue for discussion
- Contact the maintainer: [Oussama Errafif](https://github.com/OussamaERrafif)

Thank you for contributing! 🎉
