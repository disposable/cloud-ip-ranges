# Cloud IP Ranges

The idea of this repository is to have one source for all major cloud providers,
which shows their assigned IP ranges.

**Note:** This repository contains only the output of the crawler. The crawler itself is available on it's own [Repository](https://github.com/disposable/cloud-ip-ranges-crawler) and can be run on your own hardware to generate the latest IP ranges data.

## Statistics

<!-- STATS_START -->
| Metric | Value |
|--------|------:|
| Providers tracked | **100** (99 cloud + 1 misc) |
| Active IPv4 addresses | **366,528,327** (167,427 subnets) |
| Active IPv6 /64 subnets | **23,260,144,949,866** (279,718 ranges) |
| Retired IPv4 (≤ 4 weeks) | 55,792,780 addresses (22,857 subnets) |
| Retired IPv6 (≤ 4 weeks) | 770,022,772,183 /64s (9,968 ranges) |
| Last crawled | 2026-10-10 06:30 UTC |
<!-- STATS_END -->

## Data sources

All tracked providers, their source feeds and generated output files are listed in
[SOURCES.md](SOURCES.md). A few examples:

All tracked providers, their source feeds and generated output files are listed in
[SOURCES.md](SOURCES.md). A few examples:

<!-- SOURCES_TABLE_START -->
| Provider | Source | Method | IPv4 IPs | IPv6 /64s | Last Changed | JSON | TXT | CSV |
|----------|--------|--------|---------:|----------:|--------------|------|-----|-----|
| Aws | [ip-ranges.amazonaws.com/ip-ranges.json](https://ip-ranges.amazonaws.com/ip-ranges.json) | Published List | 102,542,008 (7,860 subnets)<br>+192,668 retired | 94,248,091,194 (3,472 ranges)<br>+1,950,632,725 retired | 2026-10-10 | [JSON](json/aws.json) | [TXT](txt/aws.txt) | [CSV](csv/aws.csv) |
| Google Cloud | [www.gstatic.com/ipranges/cloud.json](https://www.gstatic.com/ipranges/cloud.json)<br>[www.gstatic.com/ipranges/goog.json](https://www.gstatic.com/ipranges/goog.json) | Published List | 43,358,336 (1,155 subnets)<br>+8,704 retired | 77,457,588,240 (110 ranges)<br>+68,720,263,168 retired | 2026-10-10 | [JSON](json/google-cloud.json) | [TXT](txt/google-cloud.txt) | [CSV](csv/google-cloud.csv) |
| Cloudflare | [www.cloudflare.com/ips-v4](https://www.cloudflare.com/ips-v4)<br>[www.cloudflare.com/ips-v6](https://www.cloudflare.com/ips-v6)<br>[api.cloudflare.com/…/ips](https://api.cloudflare.com/client/v4/ips?networks=jdcloud) | Published List | 1,526,336 (61 subnets)<br>+224 retired | 60,129,542,188 (51 ranges)<br>+7 retired | 2026-09-30 | [JSON](json/cloudflare.json) | [TXT](txt/cloudflare.txt) | [CSV](csv/cloudflare.csv) |
| Github | [api.github.com/meta](https://api.github.com/meta) | Published List | 10,322 (41 subnets) | 38,654,705,664 (2 ranges) | 2026-10-07 | [JSON](json/github.json) | [TXT](txt/github.txt) | [CSV](csv/github.csv) |
| Microsoft Azure | [azservicetags.azurewebsites.net](https://azservicetags.azurewebsites.net/) | Published List | 104,868,614 (44,193 subnets)<br>+52,652,958 retired | 612,617,892 (16,905 ranges)<br>+233,672,938 retired | 2026-10-08 | [JSON](json/microsoft-azure.json) | [TXT](txt/microsoft-azure.txt) | [CSV](csv/microsoft-azure.csv) |
| Hetzner | RADB::AS-HETZNER AS1342 AS2876 AS7896 AS9197 AS11528 AS12630 AS13251 AS15372 AS15540 AS15866 AS16097 AS16302 AS20774 AS20795 AS21413 AS24940 AS24978 AS25234 AS26383 AS29192 AS30774 AS31184 AS31259 AS31639 AS31723 AS34387 AS35065 AS35170 AS35205 AS35382 AS35624 AS35830 AS39441 AS39857 AS41242 AS41369 AS41466 AS41701 AS41745 AS42265 AS42335 AS42699 AS43016 AS43329 AS43444 AS43581 AS43847 AS43937 AS44477 AS44559 AS45012 AS47105 AS47279 AS47462 AS47518 AS48154 AS48403 AS48585 AS48755 AS49189 AS49283 AS49866 AS50050 AS50053 AS50064 AS50113 AS51176 AS51311 AS51401 AS51571 AS51726 AS51728 AS51765 AS51895 AS52125 AS56418 AS56594 AS56971 AS57037 AS57043 AS58003 AS58243 AS59651 AS59921 AS60156 AS60412 AS60414 AS60522 AS60574 AS61074 AS61177 AS61352 AS61990 AS62365 AS132359 AS136258 AS153622 AS153947 AS197249 AS197540 AS197558 AS197753 AS198130 AS198167 AS198180 AS198225 AS198364 AS198550 AS199326 AS199446 AS199479 AS199644 AS199854 AS200096 AS200173 AS200186 AS200249 AS200297 AS200303 AS200508 AS200599 AS200651 AS200740 AS201014 AS201048 AS201059 AS201206 AS201600 AS201744 AS201764 AS201832 AS202071 AS202147 AS202208 AS202269 AS202373 AS202426 AS202437 AS202509 AS202753 AS202784 AS202851 AS203034 AS203195 AS203224 AS203296 AS203391 AS203437 AS203592 AS203602 AS203724 AS203872 AS203969 AS204187 AS204339 AS204591 AS204603 AS204785 AS204877 AS204924 AS205071 AS205089 AS205090 AS205435 AS205582 AS205691 AS205741 AS205876 AS206141 AS206196 AS206240 AS206303 AS206491 AS206715 AS206813 AS206855 AS206978 AS206990 AS207038 AS207077 AS207202 AS207210 AS207567 AS207569 AS207610 AS207713 AS207729 AS207793 AS207797 AS208281 AS208290 AS208451 AS208470 AS208508 AS208976 AS208987 AS208989 AS209148 AS209165 AS209325 AS209620 AS209693 AS209809 AS209847 AS210006 AS210143 AS210285 AS210414 AS210536 AS210570 AS210589 AS210633 AS210711 AS210751 AS210803 AS211003 AS211007 AS211582 AS211657 AS211873 AS212112 AS212316 AS212386 AS212613 AS212706 AS212820 AS212952 AS213021 AS213143 AS213164 AS213275 AS213459 AS213520 AS213547 AS213683 AS213702 AS213757 AS213819 AS213877 AS213954 AS214079 AS214238 AS214417 AS214422 AS214494 AS214602 AS215232 AS215392 AS215428 AS215449 AS215540 AS215556 AS215836 AS215876 AS215939 AS216024 AS216039 AS216068 AS216070 AS216253 AS216300 AS216421 AS216451 AS216473 AS218964 AS219141 AS219359 AS219498 AS398088 AS398578 | RADB AS-SET | 6,275,328 (6,516 subnets)<br>+305,408 retired | 3,243,109,056,513 (627 ranges)<br>+133,426,315,264 retired | 2026-10-10 | [JSON](json/hetzner.json) | [TXT](txt/hetzner.txt) | [CSV](csv/hetzner.csv) |
| Starlink | [geoip.starlinkisp.net/feed.csv](https://geoip.starlinkisp.net/feed.csv) | Published List | 861,620 (3,544 subnets)<br>+29,440 retired | 16,307,519,572 (911 ranges)<br>+104,923,136 retired | 2026-10-08 | [JSON](misc/starlink.json) | [TXT](misc/starlink.txt) | [CSV](misc/starlink.csv) |
<!-- SOURCES_TABLE_END -->

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
