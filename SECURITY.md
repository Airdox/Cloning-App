# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| 0.1.x   | :x:                |

## Security Features

This application implements several security measures:

### Input Validation
- All file paths are validated to prevent path traversal attacks
- Text inputs are sanitized to prevent injection attacks
- Model names are restricted to safe characters only

### Secure Random Generation
- Uses cryptographically secure random number generation (`secrets` module)
- Replaced insecure `random` module usage throughout the application

### File Security
- File chooser restricted to safe directories (user home, /tmp)
- No write permissions to external storage by default
- Comprehensive logging for security monitoring

### Error Handling
- Comprehensive exception handling to prevent information leakage
- Secure logging practices with lazy formatting
- Graceful degradation on security failures

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please follow these steps:

1. **Do not** open a public issue
2. Email the security team at: security@voicecloning.example.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will acknowledge receipt within 48 hours and provide a detailed response within 5 business days.

## Security Best Practices for Users

1. Only use audio files from trusted sources
2. Keep the application updated to the latest version
3. Review file permissions before granting access
4. Monitor application logs for suspicious activity

## Dependencies Security

This application uses minimal dependencies to reduce attack surface:
- Kivy framework (UI)
- Python standard library (cryptography via `secrets`)

All dependencies are regularly updated to their latest secure versions.