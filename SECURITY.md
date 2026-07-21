# Security policy

## Supported versions

| Version | Supported |
| --- | --- |
| 0.2.x | Yes |
| 0.1.x and earlier | No |

## Report a vulnerability

Please report suspected vulnerabilities privately through [GitHub Security Advisories](https://github.com/Doctacon/buoy/security/advisories/new). Do not open a public issue containing exploit details, credentials, private source data, or affected-user information.

Include the affected version, reproduction conditions, impact, and any suggested mitigation. Maintainers will acknowledge the report through the advisory and coordinate disclosure there.

## Scope reminders

Buoy reads public sources, local documents, local embedding models, a local DuckDB ledger, and—only on explicitly live commands—a Turbopuffer API key. Reports involving credential exposure, source-boundary bypass, unsafe artifact/state mutation, or unauthorized remote operations are especially useful.
