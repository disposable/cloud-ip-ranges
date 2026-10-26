# Cloud IP Ranges

The idea of this repository is to have one source for all major cloud providers,
which shows their assigned IP ranges.

**Note:** This repository contains only the output of the crawler. The crawler itself is available on it's own [Repository](https://github.com/disposable/cloud-ip-ranges-crawler) and can be run on your own hardware to generate the latest IP ranges data.

## Statistics

<!-- STATS_START -->
| Metric | Value |
|--------|------:|
| Providers tracked | **372** (370 cloud + 2 misc) |
| Active IPv4 addresses | **432,720,331** (319,479 subnets) |
| Active IPv6 /64 subnets | **48,596,110,753,591** (384,188 ranges) |
| Retired IPv4 (≤ 4 weeks) | 67,192,142 addresses (25,816 subnets) |
| Retired IPv6 (≤ 4 weeks) | 1,108,358,729,583 /64s (10,627 ranges) |
| Last crawled | 2026-10-26 03:27 UTC |
<!-- STATS_END -->

## Data sources

All tracked providers, their source feeds and generated output files are listed in
[SOURCES.md](SOURCES.md). A few examples:

<!-- SOURCES_TABLE_START -->
**Aws**, **Google Cloud**, **Cloudflare**, **Github**, **Microsoft Azure**, **Hetzner**, **Starlink**
<!-- SOURCES_TABLE_END -->

### Community sources

VPN providers that do not publish a usable server list (e.g. ProtonVPN, ExpressVPN, CyberGhost, IPVanish) are sourced from [qdm12/gluetun-servers](https://github.com/qdm12/gluetun-servers), the maintained server-list backend of the [Gluetun](https://github.com/qdm12/gluetun) VPN client project. Big thanks to the Gluetun community for publishing fresh server IPs.

These providers carry `"category": "proxy"` in their JSON metadata.

### Providers without published IP ranges

Some services deliberately do **not** publish IP allowlists. Their webhook and callback traffic egresses from dynamic cloud infrastructure whose addresses rotate without notice, so any collected list would silently go stale and break consumers. Providers such as **SendGrid, Mailgun, Twilio, Shopify, and Slack** are therefore intentionally absent from this dataset.

These providers authenticate requests with an **HMAC signature header** instead: the sender signs the request body with a shared secret (configured in their dashboard) and sends the signature in a request header, e.g. `X-Twilio-Signature`, `X-Shopify-Hmac-Sha256`, `X-Slack-Signature`, or SendGrid's signed Event Webhook. You can filter incoming requests by this client request header: recompute `HMAC(secret, body)` on your endpoint and compare it with the header value. A valid signature proves both origin and payload integrity regardless of the source IP, so spoofed requests are rejected without any IP allowlist.

Further reading: [HMAC (Wikipedia)](https://en.wikipedia.org/wiki/HMAC) - [RFC 2104](https://www.rfc-editor.org/rfc/rfc2104) (HMAC specification) - [RFC 9421](https://www.rfc-editor.org/rfc/rfc9421.html) (HTTP Message Signatures) - [Standard Webhooks specification](https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md) - [webhooks.fyi webhook directory](https://webhooks.fyi/docs/webhook-directory) (catalog of per-provider signature headers and schemes)

## Notes

* Some providers use ASN prefixes, which are now resolved via RIPEstat "Announced Prefixes" for BGP-announced prefixes, with HackerTarget as fallback.
* Vercel uses RDAP/ARIN registry lookups to emit Vercel-owned netblocks only (not cloud egress/edge IPs).
* All JSON outputs include metadata: provider_id, method, coverage_notes, generated_at, source_updated_at, and source_http.
* CI workflows use `--max-delta-ratio` to reject runs with extreme IP count changes.
* Misc providers (like Starlink ISP) are excluded from default runs and saved to the `misc/` directory.
* Consolidated files containing all providers' data are available as [all-providers.json](json/all-providers.json), [all-providers.txt](txt/all-providers.txt), and [all-providers.csv](csv/all-providers.csv).
* **Retired IPs**: IP ranges removed from a provider's source continue to appear in output files for 4 weeks (with a `retired_at` timestamp in JSON/CSV). Historical state is tracked in `meta/history.duckdb`, which lives on the orphan `state` branch (not `master`) to keep binary churn out of the data repo.
