# Misc IP Ranges

This directory contains IP ranges for services that are not typically considered cloud providers or harmful crawlers, but may be useful for reference.

## Included Services

- **Starlink ISP**: User ISP traffic from Starlink satellite internet service. These are regular user connections, not crawler or bot traffic.

## Usage

These ranges are excluded from the default crawler run. To generate them, use the `--misc` flag:

```bash
# Generate misc provider ranges only
uv run cloud-ip-ranges --misc

# Generate specific misc provider
uv run cloud-ip-ranges --misc --sources starlink
```

## Notes

- Misc providers are saved to this directory instead of the main json/csv/txt directories
- These ranges represent user traffic rather than infrastructure/crawler traffic
- Use with caution as they include many regular user IP addresses
