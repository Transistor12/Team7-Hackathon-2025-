# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

The HarvestNet team takes security seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please send an email to: security@harvestnet.com (replace with your actual email)

Include the following information:
- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### What to Expect

- We will acknowledge your email within 48 hours
- We will provide a detailed response within 7 days indicating next steps
- We will keep you informed of the progress towards resolving the issue
- We may ask for additional information or guidance

### Security Features

HarvestNet implements several security measures:

- JWT token-based authentication
- Password hashing with SHA-256
- Input validation and sanitization
- SQL injection prevention
- CORS protection
- Protected API endpoints
- Environment variable protection

### Safe Harbor

We support safe harbor for security researchers who:
- Make a good faith effort to avoid privacy violations, destruction of data, and interruption or degradation of our service
- Only interact with accounts you own or with explicit permission of the account holder
- Do not access a third party's data
- Do not engage in social engineering
- Report vulnerabilities as soon as possible after discovery

Thank you for helping keep HarvestNet and our users safe!
