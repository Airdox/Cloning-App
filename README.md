# Voice Cloning App

A secure voice cloning application built with Kivy framework, emphasizing security and privacy.

## Features

- **Secure File Handling**: Protected against path traversal attacks
- **Input Validation**: Comprehensive sanitization of all user inputs
- **Modern Security**: Uses cryptographically secure random generation
- **Privacy Focused**: Minimal permissions and data collection
- **Cross-Platform**: Runs on Android and desktop platforms

## Security Highlights

This application has been thoroughly analyzed and secured:

- ✅ **Fixed Critical Vulnerabilities**: Eliminated insecure random usage (CWE-330)
- ✅ **Input Validation**: Prevents injection attacks and path traversal
- ✅ **Secure File Access**: Restricted to safe directories only
- ✅ **Error Handling**: Comprehensive exception handling
- ✅ **Logging**: Security-focused logging throughout the application
- ✅ **Code Quality**: 7.64/10 Pylint score with security best practices

## Installation

### Requirements
- Python 3.11+
- Kivy 2.2.0+

### Setup
```bash
# Clone the repository
git clone https://github.com/Airdox/Cloning-App.git
cd Cloning-App

# Install dependencies
pip install kivy>=2.2.0

# Run the application
python main_apk.py
```

### Android Build
```bash
# Install buildozer
pip install buildozer

# Build for Android
buildozer android debug
```

## Usage

1. **Training Tab**: Select audio files and create voice models
   - Choose audio files from secure directories
   - Enter a valid model name (alphanumeric, _, - only)
   - Monitor training progress

2. **Text-to-Speech Tab**: Generate speech from text
   - Select a trained model
   - Enter text (max 1000 characters)
   - Generate and play audio

## Security Features

### File Security
- Path validation prevents directory traversal attacks
- File access restricted to user home and temporary directories
- No unauthorized file system access

### Input Security
- Text input sanitization removes dangerous characters
- Model name validation prevents file system manipulation
- Length limits prevent buffer overflow attacks

### Cryptographic Security
- Secure random number generation using `secrets` module
- No hardcoded secrets or credentials
- Minimal attack surface

## Development

### Code Quality
The codebase follows security best practices:
- Comprehensive docstrings and type hints
- Exception handling throughout
- Secure logging practices
- Regular security analysis with Bandit

### Contributing
Please read [SECURITY.md](SECURITY.md) before contributing.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security Policy

See [SECURITY.md](SECURITY.md) for our security policy and how to report vulnerabilities.

## Changelog

### v0.2.0 (Current)
- Major security improvements
- Fixed all critical vulnerabilities
- Added comprehensive input validation
- Improved code quality (7.64/10 Pylint score)
- Updated to modern Android API levels

### v0.1.0 (Legacy)
- Initial version with security vulnerabilities
- Not recommended for use