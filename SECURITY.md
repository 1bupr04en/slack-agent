# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Agent Slouch Mode, please **do not** open a public issue. Instead, please email us at Ibuprofen753@outlook.com with:

1. Description of the vulnerability
2. Steps to reproduce (if applicable)
3. Potential impact
4. Your suggested fix (if any)

We will acknowledge receipt of your report within 48 hours and work towards a fix.

## Security Considerations

### Data Privacy

- **Camera Access**: All camera processing is done locally. No images are stored or transmitted.
- **Window Control**: Window automation only affects the specified target window.
- **Logging**: Logs do not contain sensitive information. You can disable logging by setting `SLOTH_LOG_LEVEL=ERROR`.

### Permissions

- Requires camera device access to your system
- May require window management permissions (platform-dependent)
- Does not require network access in default configuration

### Best Practices

1. **Camera Positioning**: Ensure your camera only captures your workspace
2. **Configuration**: Use environment variables for sensitive configuration
3. **Logging**: Use appropriate log levels for your environment
4. **Dependencies**: Keep dependencies updated: `pip install --upgrade agent-slouch-mode`

### Vulnerability Handling

- We aim to release security patches within 30 days of disclosure
- Critical vulnerabilities will be fast-tracked
- Security updates will be released as patch versions (x.y.Z)

## Security-Related Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://docs.python.org/3/library/security_warnings.html)

## Dependency Security

We use the following dependency management practices:

- Regular dependency updates
- Use of pinned versions in `pyproject.toml` for stability
- Monitoring of security advisories

## Questions?

For security-related questions, please contact: Ibuprofen753@outlook.com

---

**Last Updated**: 2026-06-05
