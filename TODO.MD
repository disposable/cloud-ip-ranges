Below is a concrete, repo-specific TODO list (crawler + data repo) focused on accuracy, repeatability, and adding more providers (only “verified” additions are listed as such, with sources).

---

## 0) Fix known correctness issues in current outputs

* Remove or replace `vercel-aws`

  * In the crawler repo `vercel_aws` is commented out with the correct note (“AS15169 is Google’s ASN”). The data repo still contains `vercel-aws.*`, and it’s misleading.
  * ✅ Replace with a real `vercel` provider built from registry ownership (RDAP/Whois), not an ASN.
  * Evidence that `76.76.21.0/24` is a direct allocation to *Vercel, Inc* in ARIN: ([Whois-RWS][1])

* Deduplicate / rename `apple-icloud`

  * `apple-icloud.*` and `apple-private-relay.*` are identical (same source URL), so one is redundant.

* Decide what to do with `whatsapp`

  * It’s disabled in crawler due to page-structure changes. Either re-implement with a stable source or remove the output from the data repo until it’s reliable.

---

## 1) Add a proper “source type” model (improves accuracy + transparency)

Right now everything ends up as `ipv4/ipv6` with optional `details_*`. Add explicit metadata so users understand what the list *means*:

* Add fields like:

  * `provider_id` (stable, lowercase)
  * `method` (`published_list` | `rdap_registry` | `bgp_announced` | `asn_lookup` | `geofeed` | `scrape`)
  * `coverage_notes` (short caveat: “provider-owned netblocks only”, “egress list”, “ingress list”, “dynamic by region”, etc.)
  * `generated_at` (ISO8601) + keep upstream timestamps separately (`source_updated_at`)

This makes it possible to include providers like Vercel honestly (registry-owned blocks ≠ “all traffic Vercel may use”).

---

## 2) Replace the ASN → prefixes mechanism (big accuracy win)

Today ASN-based providers depend on HackerTarget (`aslookup`) which is fragile (rate limits) and not clearly “announced vs allocated”.

* Implement BGP-announced prefixes as the primary method for ASN providers using RIPEstat:

  * RIPEstat “Announced Prefixes” endpoint: ([RIPEstat][2])
* Keep HackerTarget only as fallback (or remove entirely if you want fewer external dependencies).

Outcome: ASN-based providers become *routing-truthy* (“what is actually announced”), not just “what someone reports from whois-ish data”.

---

## 3) Implement RDAP-based crawling for “Vercel-like” providers (no ASN, but owns netblocks)

This is the answer to your original question (“can RDAP find new IPs for the company?”): yes for org-owned allocations, not for everything they might run on AWS/GCP.

* Add a new source type, e.g.:

  * `rdap_entity_handle` and/or `rdap_entity_name`
* For ARIN specifically, you can reverse-search IP networks by entity handle/name (officially documented):

  * ([ARIN][3])
* Use IANA RDAP bootstrap files if you later expand beyond ARIN-centric cases:

  * IPv4 bootstrap registry: ([IANA][4])
* Workflow for Vercel:

  1. Start with a seed net (example `76.76.21.0/24`) → get org handle (ARIN shows `Vercel, Inc (ZEITI)`). ([Whois-RWS][1])
  2. Use ARIN RDAP reverse search to list all nets for that handle.
  3. Emit them as `vercel.json` with `method=rdap_registry` and a clear note: “Vercel-owned netblocks (registry), not the full set of cloud egress/edge IPs.”

---

## 4) Make fetching/parsing more robust

* Add a default User-Agent and sensible headers (GitHub Meta and some docs sites can be picky).
* Add retries with backoff for transient failures.
* Store and log:

  * HTTP status, content-type
  * last-modified / etag (where available)
* Add “schema guards” per provider:

  * e.g., AWS must contain `createDate`, `prefixes/ipv6_prefixes`, etc.
  * fail fast with a helpful error if upstream breaks format.

---

## 5) CI/QA to catch bad updates before they land

* Add a “sanity check” step in the update workflow:

  * Reject updates with extreme swings unless explicitly allowed (e.g., >30% delta) and print a diff summary.
* Add an overlap/normalization audit (optional):

  * detect accidental inclusion of `0.0.0.0/0`, private ranges, malformed prefixes
* Expand unit tests:

  * make sure every provider has a sample and transform test (right now you already have a good structure for this).

---

## 6) Verified provider additions you can add now

### Atlassian (public machine-readable JSON)

* Endpoint is JSON: ([IP Ranges][5])
* Atlassian documents this as the canonical machine-consumable list: ([Atlassian Support][6])

TODO

* Add provider `atlassian` → parse JSON, export `ipv4/ipv6`, keep tags/metadata if present.

### Datadog (public machine-readable JSON, by site + sections)

* Public JSON exists and includes multiple sections (`agents`, `api`, `logs`, `synthetics`, etc.): ([IP Ranges Datadog][7])

TODO

* Add provider `datadog`:

  * either emit one combined list, or separate derived outputs (`datadog-synthetics`, `datadog-logs`, …) from the same JSON.

### Okta (official JSON on S3 linked by Okta docs)

* Okta docs link to the JSON allowlist: ([Okta Hilfe][8])
* The linked file is JSON: ([Amazon Web Services, Inc.][9])

TODO

* Add provider `okta` → parse JSON, output combined `ipv4/ipv6`, optionally include “cell” grouping as `details_*`.

### Zendesk (official anonymous endpoint returning ingress/egress lists)

* Zendesk API docs describe `GET /ips` and show `https://{subdomain}.zendesk.com/ips` / `https://support.zendesk.com/ips`: ([Zendesk Entwicklerdokumentation][10])
* Live endpoint returns JSON with ingress/egress CIDRs: ([Zendesk Support][11])

TODO

* Add provider `zendesk`:

  * optionally output `zendesk-ingress` and `zendesk-egress` derived lists.

### Fly.io (ASN-based, but should be BGP-derived)

* ASN identified as Fly.io, Inc (AS40509): ([IPinfo][12])

TODO

* Add `flyio` via BGP-announced prefixes (RIPEstat method recommended).

### Render (ASN-based, but should be BGP-derived)

* ASN identified as Render (AS397273): ([BGP.Tools][13])

TODO

* Add `render` via BGP-announced prefixes.

### (Optional but useful) Scaleway: switch from ASN to official ranges page

* Scaleway publishes an official list of IP ranges (IPv4 + IPv6) in docs: ([Scaleway][14])

TODO

* Replace/augment `onlinesas` with `scaleway` using the published ranges (much simpler + clearer provenance).

---

## 7) Candidates to research later (not verified here)

Examples: Netlify (some features are UI-gated), GitLab (explicitly mentions dynamic cloud IPs), etc. Keep these as “research backlog” until you have an official/stable machine source.

---

If you want, I can also propose a small refactor of `sources = { ... }` into a declarative registry (YAML/JSON) with a `type` field (`aws_json`, `rdap_entity`, `ripestat_asn`, etc.) so adding providers becomes “data-only” rather than adding new `_transform_*` functions each time.

[1]: https://whois.arin.net/rest/net/NET-76-76-21-0-1?utm_source=chatgpt.com "Whois-RWS - ARIN"
[2]: https://stat.ripe.net/docs/data-api/api-endpoints/announced-prefixes?utm_source=chatgpt.com "Announced Prefixes - RIPEstat - RIPE NCC"
[3]: https://www.arin.net/resources/registry/whois/rdap/ "Whois/Registration Data Access Protocol (RDAP) - American Registry for Internet Numbers"
[4]: https://www.iana.org/assignments/rdap-ipv4?utm_source=chatgpt.com "Bootstrap Service Registry for IPv4 Address Space"
[5]: https://ip-ranges.atlassian.com/ "ip-ranges.atlassian.com"
[6]: https://support.atlassian.com/organization-administration/docs/ip-addresses-and-domains-for-atlassian-cloud-products/ "IP addresses and domains for Atlassian cloud apps | Atlassian Support"
[7]: https://ip-ranges.datadoghq.com/ "ip-ranges.datadoghq.com"
[8]: https://help.okta.com/en-us/content/topics/security/ip-address-allow-listing.htm "Okta IP address allow listing | Okta Classic Engine"
[9]: https://s3.amazonaws.com/okta-ip-ranges/ip_ranges.json "s3.amazonaws.com"
[10]: https://developer.zendesk.com/api-reference/ticketing/account-configuration/public_ips/ "Zendesk Public IPs | Zendesk Developer Docs"
[11]: https://support.zendesk.com/ips "support.zendesk.com"
[12]: https://ipinfo.io/AS40509?utm_source=chatgpt.com "AS40509 Fly.io, Inc. details"
[13]: https://bgp.tools/as/397273 "AS397273 Render - bgp.tools"
[14]: https://www.scaleway.com/en/docs/account/reference-content/scaleway-network-information/ "Scaleway network information | Scaleway Documentation"
