# Cloud IP Ranges

The idea of this repository is to have one source for all major cloud providers,
which shows their assigned IP ranges.

**Note:** This repository contains only the output of the crawler. The crawler itself is available on it's own [Repository](https://github.com/disposable/cloud-ip-ranges-crawler) and can be run on your own hardware to generate the latest IP ranges data.

## Statistics

<!-- STATS_START -->
_No statistics available yet — run after the first crawl._
<!-- STATS_END -->

## Data sources

<!-- SOURCES_TABLE_START -->
| Provider | Source | Method | IPv4 | IPv6 | Last Changed | JSON | TXT | CSV |
|----------|--------|--------|-----:|-----:|--------------|------|-----|-----|
| A2Hosting | AS55293 | ASN Prefix | — | — | — | [JSON](json/a2hosting.json) | [TXT](txt/a2hosting.txt) | [CSV](csv/a2hosting.csv) |
| Aruba Cloud | AS200185 | ASN Prefix | — | — | — | [JSON](json/aruba-cloud.json) | [TXT](txt/aruba-cloud.txt) | [CSV](csv/aruba-cloud.csv) |
| Choopa | AS46407, AS20473, AS133795, AS11508 | ASN Prefix | — | — | — | [JSON](json/choopa.json) | [TXT](txt/choopa.txt) | [CSV](csv/choopa.csv) |
| CYSO Cloud | AS25151 | ASN Prefix | — | — | — | [JSON](json/cyso-cloud.json) | [TXT](txt/cyso-cloud.txt) | [CSV](csv/cyso-cloud.csv) |
| Dreamhost | AS26347 | ASN Prefix | — | — | — | [JSON](json/dreamhost.json) | [TXT](txt/dreamhost.txt) | [CSV](csv/dreamhost.csv) |
| Fly.io | AS40509 | ASN Prefix | — | — | — | [JSON](json/flyio.json) | [TXT](txt/flyio.txt) | [CSV](csv/flyio.csv) |
| GoDaddy | AS26496, AS30083 | ASN Prefix | — | — | — | [JSON](json/godaddy.json) | [TXT](txt/godaddy.txt) | [CSV](csv/godaddy.csv) |
| gridscale | AS29423 | ASN Prefix | — | — | — | [JSON](json/gridscale.json) | [TXT](txt/gridscale.txt) | [CSV](csv/gridscale.csv) |
| Heroku/AWS | AS14618 | ASN Prefix | — | — | — | [JSON](json/heroku-aws.json) | [TXT](txt/heroku-aws.txt) | [CSV](csv/heroku-aws.csv) |
| IONOS Cloud | AS8560 | ASN Prefix | — | — | — | [JSON](json/ionos-cloud.json) | [TXT](txt/ionos-cloud.txt) | [CSV](csv/ionos-cloud.csv) |
| Kamatera | AS36007 | ASN Prefix | — | — | — | [JSON](json/kamatera.json) | [TXT](txt/kamatera.txt) | [CSV](csv/kamatera.csv) |
| Open Telekom Cloud | AS6878 | ASN Prefix | — | — | — | [JSON](json/open-telekom-cloud.json) | [TXT](txt/open-telekom-cloud.txt) | [CSV](csv/open-telekom-cloud.csv) |
| Render | AS397273 | ASN Prefix | — | — | — | [JSON](json/render.json) | [TXT](txt/render.txt) | [CSV](csv/render.csv) |
| Seeweb | AS12637 | ASN Prefix | — | — | — | [JSON](json/seeweb.json) | [TXT](txt/seeweb.txt) | [CSV](csv/seeweb.csv) |
| Ucloud | AS135377, AS59077 | ASN Prefix | — | — | — | [JSON](json/ucloud.json) | [TXT](txt/ucloud.txt) | [CSV](csv/ucloud.csv) |
| UpCloud | AS202053, AS25697 | ASN Prefix | — | — | — | [JSON](json/upcloud.json) | [TXT](txt/upcloud.txt) | [CSV](csv/upcloud.csv) |
| Wasabi | AS395717 | ASN Prefix | — | — | — | [JSON](json/wasabi.json) | [TXT](txt/wasabi.txt) | [CSV](csv/wasabi.csv) |
| Ahrefs | [ahrefs.com/…/crawler-ips](https://api.ahrefs.com/v3/public/crawler-ips) | Published List | — | — | — | [JSON](json/ahrefs.json) | [TXT](txt/ahrefs.txt) | [CSV](csv/ahrefs.csv) |
| Atlassian | [ip-ranges.atlassian.com](https://ip-ranges.atlassian.com/) | Published List | — | — | — | [JSON](json/atlassian.json) | [TXT](txt/atlassian.txt) | [CSV](csv/atlassian.csv) |
| Datadog | [ip-ranges.datadoghq.com](https://ip-ranges.datadoghq.com/) | Published List | — | — | — | [JSON](json/datadog.json) | [TXT](txt/datadog.txt) | [CSV](csv/datadog.csv) |
| Fastly | [api.fastly.com/…/public-ip-list](https://api.fastly.com/public-ip-list) | Published List | — | — | — | [JSON](json/fastly.json) | [TXT](txt/fastly.txt) | [CSV](csv/fastly.csv) |
| GitHub | [api.github.com/meta](https://api.github.com/meta) | Published List | — | — | — | [JSON](json/github.json) | [TXT](txt/github.txt) | [CSV](csv/github.csv) |
| Grafana Cloud | Multiple API endpoints | Published List | — | — | — | [JSON](json/grafana-cloud.json) | [TXT](txt/grafana-cloud.txt) | [CSV](csv/grafana-cloud.csv) |
| HCP Terraform | [app.terraform.io/…/ip-ranges](https://app.terraform.io/api/meta/ip-ranges) | Published List | — | — | — | [JSON](json/hcp-terraform.json) | [TXT](txt/hcp-terraform.txt) | [CSV](csv/hcp-terraform.csv) |
| Linode | [geoip.linode.com](https://geoip.linode.com/) | Published List | — | — | — | [JSON](json/linode.json) | [TXT](txt/linode.txt) | [CSV](csv/linode.csv) |
| Microsoft Azure | [azservicetags.azurewebsites.net](https://azservicetags.azurewebsites.net/) | Published List | — | — | — | [JSON](json/microsoft-azure.json) | [TXT](txt/microsoft-azure.txt) | [CSV](csv/microsoft-azure.csv) |
| Sentry | [sentry.io/…/uptime-ips](https://sentry.io/api/0/uptime-ips/) | Published List | — | — | — | [JSON](json/sentry.json) | [TXT](txt/sentry.txt) | [CSV](csv/sentry.csv) |
| Zendesk | [support.zendesk.com/ips](https://support.zendesk.com/ips) | Published List | — | — | — | [JSON](json/zendesk.json) | [TXT](txt/zendesk.txt) | [CSV](csv/zendesk.csv) |
| Apple Private Relay | [mask-api.icloud.com/…/egress-ip-ranges.csv](https://mask-api.icloud.com/egress-ip-ranges.csv) | Published List | — | — | — | [JSON](json/apple-private-relay.json) | [TXT](txt/apple-private-relay.txt) | [CSV](csv/apple-private-relay.csv) |
| DigitalOcean | [digitalocean.com/geo/google.csv](https://digitalocean.com/geo/google.csv) | Published List | — | — | — | [JSON](json/digitalocean.json) | [TXT](txt/digitalocean.txt) | [CSV](csv/digitalocean.csv) |
| Starlink ISP | [geoip.starlinkisp.net/feed.csv](https://geoip.starlinkisp.net/feed.csv) | Published List | — | — | — | [JSON](misc/starlink-isp.json) | [TXT](misc/starlink-isp.txt) | [CSV](misc/starlink-isp.csv) |
| Adyen | [docs.adyen.com/…/allowlisting](https://docs.adyen.com/development-resources/security/integration-security/allowlisting) | Published List | — | — | — | [JSON](json/adyen.json) | [TXT](txt/adyen.txt) | [CSV](csv/adyen.csv) |
| Branch | [help.branch.io/…/webhook-ip-address-allowlist](https://help.branch.io/docs/postback-webhook-ip-address-allowlist-expands) | Published List | — | — | — | [JSON](json/branch.json) | [TXT](txt/branch.txt) | [CSV](csv/branch.csv) |
| Amazon Web Services | [ip-ranges.amazonaws.com/ip-ranges.json](https://ip-ranges.amazonaws.com/ip-ranges.json) | Published List | — | — | — | [JSON](json/aws.json) | [TXT](txt/aws.txt) | [CSV](csv/aws.csv) |
| Bing Bot | [bing.com/toolbox/bingbot.json](https://www.bing.com/toolbox/bingbot.json) | Published List | — | — | — | [JSON](json/bing-bot.json) | [TXT](txt/bing-bot.txt) | [CSV](csv/bing-bot.csv) |
| CircleCI | [circleci.com/…/ip-ranges-list.json](https://circleci.com/docs/ip-ranges-list.json) | Published List | — | — | — | [JSON](json/circleci.json) | [TXT](txt/circleci.txt) | [CSV](csv/circleci.csv) |
| Google Bot | [developers.google.com/…/googlebot.json](https://developers.google.com/static/search/apis/ipranges/googlebot.json) | Published List | — | — | — | [JSON](json/google-bot.json) | [TXT](txt/google-bot.txt) | [CSV](csv/google-bot.csv) |
| Google Cloud | [gstatic.com/ipranges/cloud.json](https://www.gstatic.com/ipranges/cloud.json) | Published List | — | — | — | [JSON](json/google-cloud.json) | [TXT](txt/google-cloud.txt) | [CSV](csv/google-cloud.csv) |
| Intercom | Multiple regional endpoints | Published List | — | — | — | [JSON](json/intercom.json) | [TXT](txt/intercom.txt) | [CSV](csv/intercom.csv) |
| New Relic Synthetics | [nr-synthetics-assets.s3…/ip-ranges.json](https://nr-synthetics-assets.s3.amazonaws.com/nat-ip-dnsname/production/ip-ranges.json) | Published List | — | — | — | [JSON](json/new-relic-synthetics.json) | [TXT](txt/new-relic-synthetics.txt) | [CSV](csv/new-relic-synthetics.csv) |
| Okta | [s3.amazonaws.com/okta-ip-ranges/ip_ranges.json](https://s3.amazonaws.com/okta-ip-ranges/ip_ranges.json) | Published List | — | — | — | [JSON](json/okta.json) | [TXT](txt/okta.txt) | [CSV](csv/okta.csv) |
| OpenAI | [openai.com/chatgpt-user.json](https://openai.com/chatgpt-user.json)<br>[openai.com/gptbot.json](https://openai.com/gptbot.json) | Published List | — | — | — | [JSON](json/openai.json) | [TXT](txt/openai.txt) | [CSV](csv/openai.csv) |
| Oracle Cloud | [docs.oracle.com/…/public_ip_ranges.json](https://docs.oracle.com/iaas/tools/public_ip_ranges.json) | Published List | — | — | — | [JSON](json/oracle-cloud.json) | [TXT](txt/oracle-cloud.txt) | [CSV](csv/oracle-cloud.csv) |
| Perplexity | [perplexity.ai/perplexitybot.json](https://www.perplexity.ai/perplexitybot.json)<br>[perplexity.ai/perplexity-user.json](https://www.perplexity.ai/perplexity-user.json) | Published List | — | — | — | [JSON](json/perplexity.json) | [TXT](txt/perplexity.txt) | [CSV](csv/perplexity.csv) |
| Salesforce Hyperforce | [ip-ranges.salesforce.com/ip-ranges.json](https://ip-ranges.salesforce.com/ip-ranges.json) | Published List | — | — | — | [JSON](json/salesforce-hyperforce.json) | [TXT](txt/salesforce-hyperforce.txt) | [CSV](csv/salesforce-hyperforce.csv) |
| Stripe | [stripe.com/…/ips_api.json](https://stripe.com/files/ips/ips_api.json)<br>[stripe.com/…/ips_webhooks.json](https://stripe.com/files/ips/ips_webhooks.json) | Published List | — | — | — | [JSON](json/stripe.json) | [TXT](txt/stripe.txt) | [CSV](csv/stripe.csv) |
| Vultr | [geofeed.constant.com/?json](https://geofeed.constant.com/?json) | Published List | — | — | — | [JSON](json/vultr.json) | [TXT](txt/vultr.txt) | [CSV](csv/vultr.csv) |
| Zscaler | [config.zscaler.com/…/cidr/json](https://config.zscaler.com/api/zscaler.net/hubs/cidr/json/) | Published List | — | — | — | [JSON](json/zscaler.json) | [TXT](txt/zscaler.txt) | [CSV](csv/zscaler.csv) |
| Exoscale | [exoscale-prefixes.sos-ch-dk-2.exo.io/…](https://exoscale-prefixes.sos-ch-dk-2.exo.io/exoscale_prefixes.json) | Published List | — | — | — | [JSON](json/exoscale.json) | [TXT](txt/exoscale.txt) | [CSV](csv/exoscale.csv) |
| Telegram | [core.telegram.org/resources/cidr.txt](https://core.telegram.org/resources/cidr.txt) | Published List | — | — | — | [JSON](json/telegram.json) | [TXT](txt/telegram.txt) | [CSV](csv/telegram.csv) |
| Cloudflare | [cloudflare.com/ips-v4](https://www.cloudflare.com/ips-v4)<br>[cloudflare.com/ips-v6](https://www.cloudflare.com/ips-v6) | Published List | — | — | — | [JSON](json/cloudflare.json) | [TXT](txt/cloudflare.txt) | [CSV](csv/cloudflare.csv) |
| Akamai | [techdocs.akamai.com/…/CIDRs-txt.zip](https://techdocs.akamai.com/property-manager/pdfs/akamai_ipv4_ipv6_CIDRs-txt.zip) | Published List | — | — | — | [JSON](json/akamai.json) | [TXT](txt/akamai.txt) | [CSV](csv/akamai.csv) |
| Alibaba | RADB::AS-ALIBABA-CN-NET, AS134963 | RADB AS-SET | — | — | — | [JSON](json/alibaba.json) | [TXT](txt/alibaba.txt) | [CSV](csv/alibaba.csv) |
| Hetzner | RADB::AS-HETZNER | RADB AS-SET | — | — | — | [JSON](json/hetzner.json) | [TXT](txt/hetzner.txt) | [CSV](csv/hetzner.csv) |
| Huawei Cloud | RADB::AS-HUAWEI | RADB AS-SET | — | — | — | [JSON](json/huawei-cloud.json) | [TXT](txt/huawei-cloud.txt) | [CSV](csv/huawei-cloud.csv) |
| IBM/Softlayer | RADB::AS-SOFTLAYER | RADB AS-SET | — | — | — | [JSON](json/softlayer-ibm.json) | [TXT](txt/softlayer-ibm.txt) | [CSV](csv/softlayer-ibm.csv) |
| Meta Crawler | RADB::AS-FACEBOOK | RADB AS-SET | — | — | — | [JSON](json/meta-crawler.json) | [TXT](txt/meta-crawler.txt) | [CSV](csv/meta-crawler.csv) |
| nForce | RADB::AS-NFORCE | RADB AS-SET | — | — | — | [JSON](json/nforce.json) | [TXT](txt/nforce.txt) | [CSV](csv/nforce.csv) |
| Online SAS | RADB::AS-ONLINESAS | RADB AS-SET | — | — | — | [JSON](json/onlinesas.json) | [TXT](txt/onlinesas.txt) | [CSV](csv/onlinesas.csv) |
| OVH | RADB::AS-OVH | RADB AS-SET | — | — | — | [JSON](json/ovh.json) | [TXT](txt/ovh.txt) | [CSV](csv/ovh.csv) |
| Rackspace | RADB::AS-RACKSPACE | RADB AS-SET | — | — | — | [JSON](json/rackspace.json) | [TXT](txt/rackspace.txt) | [CSV](csv/rackspace.csv) |
| Tencent | RADB::AS132203:AS-TENCENT | RADB AS-SET | — | — | — | [JSON](json/tencent.json) | [TXT](txt/tencent.txt) | [CSV](csv/tencent.csv) |
| Vercel | RDAP/ARIN registry | RDAP/ARIN Registry | — | — | — | [JSON](json/vercel.json) | [TXT](txt/vercel.txt) | [CSV](csv/vercel.csv) |
| Backblaze | [backblaze.com/…/backblaze-ip-addresses](https://www.backblaze.com/computer-backup/docs/backblaze-ip-addresses) | Published List | — | — | — | [JSON](json/backblaze.json) | [TXT](txt/backblaze.txt) | [CSV](csv/backblaze.csv) |
| Cisco Webex | [help.webex.com/…/WBX000028782](https://help.webex.com/article/WBX000028782/Network-Requirements-for-Webex-Teams-Services)<br>[help.webex.com/…/WBX264](https://help.webex.com/en-us/article/WBX264/How-Do-I-Allow-Webex-Meetings-Traffic-on-My-Network) | Published List | — | — | — | [JSON](json/cisco-webex.json) | [TXT](txt/cisco-webex.txt) | [CSV](csv/cisco-webex.csv) |
| Scaleway | [scaleway.com/…/scaleway-network-information](https://www.scaleway.com/en/docs/account/reference-content/scaleway-network-information/) | Published List | — | — | — | [JSON](json/scaleway.json) | [TXT](txt/scaleway.txt) | [CSV](csv/scaleway.csv) |
<!-- SOURCES_TABLE_END -->

## Notes

* Some providers use ASN prefixes, which are now resolved via RIPEstat "Announced Prefixes" for BGP-announced prefixes, with HackerTarget as fallback.
* Vercel uses RDAP/ARIN registry lookups to emit Vercel-owned netblocks only (not cloud egress/edge IPs).
* All JSON outputs include metadata: provider_id, method, coverage_notes, generated_at, source_updated_at, and source_http.
* CI workflows use `--max-delta-ratio` to reject runs with extreme IP count changes.
* Misc providers (like Starlink ISP) are excluded from default runs and saved to the `misc/` directory.
* Consolidated files containing all providers' data are available as [all-providers.json](json/all-providers.json), [all-providers.txt](txt/all-providers.txt), and [all-providers.csv](csv/all-providers.csv).
* **Retired IPs**: IP ranges removed from a provider's source continue to appear in output files for 4 weeks (with a `retired_at` timestamp in JSON/CSV). Historical state is tracked in `meta/history.duckdb`.
