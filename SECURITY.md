# Security Policy

## Reporting a vulnerability

This repository contains a research dataset, analysis code, and documentation.
If you find a security issue (for example in the parser, notebooks, or analysis
code), please report it privately using GitHub's
[private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)
on this repository ("Security" tab → "Report a vulnerability").

Please do not open a public issue for security vulnerabilities.

## Supported versions

| Version | Status              |
| ------- | ------------------- |
| main    | actively maintained |

## Scope

- `parse_ibm_json.py` (untrusted JSON input handling)
- `analysis/` code
- `notebooks/` code
- Repository automation (`scripts/`, GitHub Actions workflows)

Reports are triaged on a best-effort basis; fixes are published as regular
commits and noted in `CHANGELOG.md`.
