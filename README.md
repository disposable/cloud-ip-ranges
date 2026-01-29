# Cloud IP Ranges

The idea of this repository is to have one source for all major cloud providers,
which shows their assigned IP ranges.

**Note:** This repository contains only the output of the crawler. The crawler itself is available on it's own [Repository](https://github.com/disposable/cloud-ip-ranges-crawler) and can be run on your own hardware to generate the latest IP ranges data.

## Data sources

| Provider | Source URL(s) | Method/Notes |
|----------|---------------|--------------|
| A2Hosting | AS55293 | ASN Prefix |
| Aruba Cloud | AS200185 | ASN Prefix |
| Choopa | AS46407, AS20473, AS133795, AS11508 | ASN Prefix |
| CYSO Cloud | AS25151 | ASN Prefix |
| Dreamhost | AS26347 | ASN Prefix |
| Fly.io (`flyio`) | AS40509 | ASN Prefix |
| GoDaddy | AS26496, AS30083 | ASN Prefix |
| gridscale | AS29423 | ASN Prefix |
| Heroku/AWS (`heroku_aws`) | AS14618 | ASN Prefix |
| IONOS Cloud | AS8560 | ASN Prefix |
| Kamatera | AS36007 | ASN Prefix |
| Open Telekom Cloud | AS6878 | ASN Prefix |
| Render | AS397273 | ASN Prefix |
| Seeweb | AS12637 | ASN Prefix |
| Ucloud | AS135377, AS59077 | ASN Prefix |
| UpCloud | AS202053, AS25697 | ASN Prefix |
| Wasabi | AS395717 | ASN Prefix |
| Ahrefs | https://api.ahrefs.com/v3/public/crawler-ips | Direct API |
| Atlassian | https://ip-ranges.atlassian.com/ | Direct API |
| Datadog | https://ip-ranges.datadoghq.com/ | Direct API |
| Fastly | https://api.fastly.com/public-ip-list | Direct API |
| GitHub | https://api.github.com/meta | Direct API |
| Grafana Cloud | Multiple API endpoints for different services | Direct API |
| HCP Terraform | https://app.terraform.io/api/meta/ip-ranges | Direct API |
| Linode | https://geoip.linode.com/ | Direct API |
| Microsoft Azure | https://azservicetags.azurewebsites.net/ | Direct API |
| Sentry | https://sentry.io/api/0/uptime-ips/ | Direct API |
| Zendesk | https://support.zendesk.com/ips | Direct API |
| Apple Private Relay | https://mask-api.icloud.com/egress-ip-ranges.csv | Direct CSV |
| DigitalOcean (DO) | https://digitalocean.com/geo/google.csv | Direct CSV |
| Starlink ISP | https://geoip.starlinkisp.net/feed.csv | Direct CSV (saved to misc/) |
| Adyen | https://docs.adyen.com/development-resources/security/integration-security/allowlisting | Direct docs |
| Branch | https://help.branch.io/docs/postback-webhook-ip-address-allowlist-expands | Direct docs |
| WhatsApp | https://developers.facebook.com/docs/whatsapp/guides/network-requirements/ | Direct docs |
| Amazon Web Services (AWS) | https://ip-ranges.amazonaws.com/ip-ranges.json | Direct JSON |
| Bing Bot | https://www.bing.com/toolbox/bingbot.json | Direct JSON |
| CircleCI | https://circleci.com/docs/ip-ranges-list.json | Direct JSON |
| Google Bot | https://developers.google.com/static/search/apis/ipranges/googlebot.json | Direct JSON |
| Google Cloud (GCloud) | https://www.gstatic.com/ipranges/cloud.json | Direct JSON |
| Intercom | Multiple regional endpoints | Direct JSON |
| New Relic Synthetics | https://nr-synthetics-assets.s3.amazonaws.com/nat-ip-dnsname/production/ip-ranges.json | Direct JSON |
| Okta | https://s3.amazonaws.com/okta-ip-ranges/ip_ranges.json | Direct JSON |
| OpenAI | https://openai.com/chatgpt-user.json<br>https://openai.com/gptbot.json | Direct JSON |
| Oracle Cloud | https://docs.oracle.com/iaas/tools/public_ip_ranges.json | Direct JSON |
| Perplexity | https://www.perplexity.ai/perplexitybot.json<br>https://www.perplexity.ai/perplexity-user.json | Direct JSON |
| Salesforce Hyperforce | https://ip-ranges.salesforce.com/ip-ranges.json | Direct JSON |
| Stripe | https://stripe.com/files/ips/ips_api.json<br>https://stripe.com/files/ips/ips_webhooks.json | Direct JSON |
| Vultr | https://geofeed.constant.com/?json | Direct JSON |
| Zscaler | https://config.zscaler.com/api/zscaler.net/hubs/cidr/json/ | Direct JSON |
| Exoscale | https://exoscale-prefixes.sos-ch-dk-2.exo.io/exoscale_prefixes.json | Direct JSON feed |
| Telegram | https://core.telegram.org/resources/cidr.txt | Direct text |
| Cloudflare | IPv4: https://www.cloudflare.com/ips-v4<br>IPv6: https://www.cloudflare.com/ips-v6 | Direct text files |
| Akamai | https://techdocs.akamai.com/property-manager/pdfs/akamai_ipv4_ipv6_CIDRs-txt.zip | Direct ZIP |
| Alibaba | RADB::AS-ALIBABA-CN-NET, AS134963 | RADB AS-SET |
| Hetzner | RADB::AS-HETZNER | RADB AS-SET |
| Huawei Cloud | RADB::AS-HUAWEI | RADB AS-SET |
| IBM/Softlayer (`softlayer_ibm`) | RADB::AS-SOFTLAYER | RADB AS-SET |
| Meta Crawler | RADB::AS-FACEBOOK | RADB AS-SET |
| nForce | RADB::AS-NFORCE | RADB AS-SET |
| Online SAS | RADB::AS-ONLINESAS | RADB AS-SET |
| OVH | RADB::AS-OVH | RADB AS-SET |
| Rackspace | RADB::AS-RACKSPACE | RADB AS-SET |
| Tencent | RADB::AS132203:AS-TENCENT | RADB AS-SET |
| Vercel | RDAP/ARIN registry-owned netblocks | RDAP/ARIN registry |
| Backblaze | https://www.backblaze.com/computer-backup/docs/backblaze-ip-addresses | Structured docs scrape |
| Cisco Webex | https://help.webex.com/article/WBX000028782/Network-Requirements-for-Webex-Teams-Services<br>https://help.webex.com/en-us/article/WBX264/How-Do-I-Allow-Webex-Meetings-Traffic-on-My-Network | Structured docs scrape |
| Scaleway | https://www.scaleway.com/en/docs/account/reference-content/scaleway-network-information/ | Structured docs scrape |

## Notes

* Some providers use ASN prefixes, which are now resolved via RIPEstat "Announced Prefixes" for BGP-announced prefixes, with HackerTarget as fallback.
* Vercel uses RDAP/ARIN registry lookups to emit Vercel-owned netblocks only (not cloud egress/edge IPs).
* All JSON outputs include metadata: provider_id, method, coverage_notes, generated_at, source_updated_at, and source_http.
* CI workflows use `--max-delta-ratio` to reject runs with extreme IP count changes.
* Misc providers (like Starlink ISP) are excluded from default runs and saved to the `misc/` directory.
