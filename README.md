# Cloud IP Ranges

The idea of this repository is to have one source for all major cloud providers,
which shows their assigned IP ranges.

**Note:** This repository contains only the output of the crawler. The crawler itself is available on it's own [Repository](https://github.com/disposable/cloud-ip-ranges-crawler) and can be run on your own hardware to generate the latest IP ranges data.

## Data sources

| Provider | Source URL(s) | Method/Notes | JSON | TXT | CSV |
|----------|---------------|--------------|------------|-----|-----|
| A2Hosting | AS55293 | ASN Prefix | [JSON](json/a2hosting.json) | [TXT](txt/a2hosting.txt) | [CSV](csv/a2hosting.csv) |
| Aruba Cloud | AS200185 | ASN Prefix | [JSON](json/aruba-cloud.json) | [TXT](txt/aruba-cloud.txt) | [CSV](csv/aruba-cloud.csv) |
| Choopa | AS46407, AS20473, AS133795, AS11508 | ASN Prefix | [JSON](json/choopa.json) | [TXT](txt/choopa.txt) | [CSV](csv/choopa.csv) |
| CYSO Cloud | AS25151 | ASN Prefix | [JSON](json/cyso-cloud.json) | [TXT](txt/cyso-cloud.txt) | [CSV](csv/cyso-cloud.csv) |
| Dreamhost | AS26347 | ASN Prefix | [JSON](json/dreamhost.json) | [TXT](txt/dreamhost.txt) | [CSV](csv/dreamhost.csv) |
| Fly.io (`flyio`) | AS40509 | ASN Prefix | [JSON](json/flyio.json) | [TXT](txt/flyio.txt) | [CSV](csv/flyio.csv) |
| GoDaddy | AS26496, AS30083 | ASN Prefix | [JSON](json/godaddy.json) | [TXT](txt/godaddy.txt) | [CSV](csv/godaddy.csv) |
| gridscale | AS29423 | ASN Prefix | [JSON](json/gridscale.json) | [TXT](txt/gridscale.txt) | [CSV](csv/gridscale.csv) |
| Heroku/AWS (`heroku_aws`) | AS14618 | ASN Prefix | [JSON](json/heroku-aws.json) | [TXT](txt/heroku-aws.txt) | [CSV](csv/heroku-aws.csv) |
| IONOS Cloud | AS8560 | ASN Prefix | [JSON](json/ionos-cloud.json) | [TXT](txt/ionos-cloud.txt) | [CSV](csv/ionos-cloud.csv) |
| Kamatera | AS36007 | ASN Prefix | [JSON](json/kamatera.json) | [TXT](txt/kamatera.txt) | [CSV](csv/kamatera.csv) |
| Open Telekom Cloud | AS6878 | ASN Prefix | [JSON](json/open-telekom-cloud.json) | [TXT](txt/open-telekom-cloud.txt) | [CSV](csv/open-telekom-cloud.csv) |
| Render | AS397273 | ASN Prefix | [JSON](json/render.json) | [TXT](txt/render.txt) | [CSV](csv/render.csv) |
| Seeweb | AS12637 | ASN Prefix | [JSON](json/seeweb.json) | [TXT](txt/seeweb.txt) | [CSV](csv/seeweb.csv) |
| Ucloud | AS135377, AS59077 | ASN Prefix | [JSON](json/ucloud.json) | [TXT](txt/ucloud.txt) | [CSV](csv/ucloud.csv) |
| UpCloud | AS202053, AS25697 | ASN Prefix | [JSON](json/upcloud.json) | [TXT](txt/upcloud.txt) | [CSV](csv/upcloud.csv) |
| Wasabi | AS395717 | ASN Prefix | [JSON](json/wasabi.json) | [TXT](txt/wasabi.txt) | [CSV](csv/wasabi.csv) |
| Ahrefs | https://api.ahrefs.com/v3/public/crawler-ips | Direct API | [JSON](json/ahrefs.json) | [TXT](txt/ahrefs.txt) | [CSV](csv/ahrefs.csv) |
| Atlassian | https://ip-ranges.atlassian.com/ | Direct API | [JSON](json/atlassian.json) | [TXT](txt/atlassian.txt) | [CSV](csv/atlassian.csv) |
| Datadog | https://ip-ranges.datadoghq.com/ | Direct API | [JSON](json/datadog.json) | [TXT](txt/datadog.txt) | [CSV](csv/datadog.csv) |
| Fastly | https://api.fastly.com/public-ip-list | Direct API | [JSON](json/fastly.json) | [TXT](txt/fastly.txt) | [CSV](csv/fastly.csv) |
| GitHub | https://api.github.com/meta | Direct API | [JSON](json/github.json) | [TXT](txt/github.txt) | [CSV](csv/github.csv) |
| Grafana Cloud | Multiple API endpoints for different services | Direct API | [JSON](json/grafana-cloud.json) | [TXT](txt/grafana-cloud.txt) | [CSV](csv/grafana-cloud.csv) |
| HCP Terraform | https://app.terraform.io/api/meta/ip-ranges | Direct API | [JSON](json/hcp-terraform.json) | [TXT](txt/hcp-terraform.txt) | [CSV](csv/hcp-terraform.csv) |
| Linode | https://geoip.linode.com/ | Direct API | [JSON](json/linode.json) | [TXT](txt/linode.txt) | [CSV](csv/linode.csv) |
| Microsoft Azure | https://azservicetags.azurewebsites.net/ | Direct API | [JSON](json/microsoft-azure.json) | [TXT](txt/microsoft-azure.txt) | [CSV](csv/microsoft-azure.csv) |
| Sentry | https://sentry.io/api/0/uptime-ips/ | Direct API | [JSON](json/sentry.json) | [TXT](txt/sentry.txt) | [CSV](csv/sentry.csv) |
| Zendesk | https://support.zendesk.com/ips | Direct API | [JSON](json/zendesk.json) | [TXT](txt/zendesk.txt) | [CSV](csv/zendesk.csv) |
| Apple Private Relay | https://mask-api.icloud.com/egress-ip-ranges.csv | Direct CSV | [JSON](json/apple-private-relay.json) | [TXT](txt/apple-private-relay.txt) | [CSV](csv/apple-private-relay.csv) |
| DigitalOcean (DO) | https://digitalocean.com/geo/google.csv | Direct CSV | [JSON](json/digitalocean.json) | [TXT](txt/digitalocean.txt) | [CSV](csv/digitalocean.csv) |
| Starlink ISP | https://geoip.starlinkisp.net/feed.csv | Direct CSV (saved to misc/) | [JSON](misc/starlink-isp.json) | [TXT](misc/starlink-isp.txt) | [CSV](misc/starlink-isp.csv) |
| Adyen | https://docs.adyen.com/development-resources/security/integration-security/allowlisting | Direct docs | [JSON](json/adyen.json) | [TXT](txt/adyen.txt) | [CSV](csv/adyen.csv) |
| Branch | https://help.branch.io/docs/postback-webhook-ip-address-allowlist-expands | Direct docs | [JSON](json/branch.json) | [TXT](txt/branch.txt) | [CSV](csv/branch.csv) |
| Amazon Web Services (AWS) | https://ip-ranges.amazonaws.com/ip-ranges.json | Direct JSON | [JSON](json/aws.json) | [TXT](txt/aws.txt) | [CSV](csv/aws.csv) |
| Bing Bot | https://www.bing.com/toolbox/bingbot.json | Direct JSON | [JSON](json/bing-bot.json) | [TXT](txt/bing-bot.txt) | [CSV](csv/bing-bot.csv) |
| CircleCI | https://circleci.com/docs/ip-ranges-list.json | Direct JSON | [JSON](json/circleci.json) | [TXT](txt/circleci.txt) | [CSV](csv/circleci.csv) |
| Google Bot | https://developers.google.com/static/search/apis/ipranges/googlebot.json | Direct JSON | [JSON](json/google-bot.json) | [TXT](txt/google-bot.txt) | [CSV](csv/google-bot.csv) |
| Google Cloud (GCloud) | https://www.gstatic.com/ipranges/cloud.json | Direct JSON | [JSON](json/google-cloud.json) | [TXT](txt/google-cloud.txt) | [CSV](csv/google-cloud.csv) |
| Intercom | Multiple regional endpoints | Direct JSON | [JSON](json/intercom.json) | [TXT](txt/intercom.txt) | [CSV](csv/intercom.csv) |
| New Relic Synthetics | https://nr-synthetics-assets.s3.amazonaws.com/nat-ip-dnsname/production/ip-ranges.json | Direct JSON | [JSON](json/new-relic-synthetics.json) | [TXT](txt/new-relic-synthetics.txt) | [CSV](csv/new-relic-synthetics.csv) |
| Okta | https://s3.amazonaws.com/okta-ip-ranges/ip_ranges.json | Direct JSON | [JSON](json/okta.json) | [TXT](txt/okta.txt) | [CSV](csv/okta.csv) |
| OpenAI | https://openai.com/chatgpt-user.json<br>https://openai.com/gptbot.json | Direct JSON | [JSON](json/openai.json) | [TXT](txt/openai.txt) | [CSV](csv/openai.csv) |
| Oracle Cloud | https://docs.oracle.com/iaas/tools/public_ip_ranges.json | Direct JSON | [JSON](json/oracle-cloud.json) | [TXT](txt/oracle-cloud.txt) | [CSV](csv/oracle-cloud.csv) |
| Perplexity | https://www.perplexity.ai/perplexitybot.json<br>https://www.perplexity.ai/perplexity-user.json | Direct JSON | [JSON](json/perplexity.json) | [TXT](txt/perplexity.txt) | [CSV](csv/perplexity.csv) |
| Salesforce Hyperforce | https://ip-ranges.salesforce.com/ip-ranges.json | Direct JSON | [JSON](json/salesforce-hyperforce.json) | [TXT](txt/salesforce-hyperforce.txt) | [CSV](csv/salesforce-hyperforce.csv) |
| Stripe | https://stripe.com/files/ips/ips_api.json<br>https://stripe.com/files/ips/ips_webhooks.json | Direct JSON | [JSON](json/stripe.json) | [TXT](txt/stripe.txt) | [CSV](csv/stripe.csv) |
| Vultr | https://geofeed.constant.com/?json | Direct JSON | [JSON](json/vultr.json) | [TXT](txt/vultr.txt) | [CSV](csv/vultr.csv) |
| Zscaler | https://config.zscaler.com/api/zscaler.net/hubs/cidr/json/ | Direct JSON | [JSON](json/zscaler.json) | [TXT](txt/zscaler.txt) | [CSV](csv/zscaler.csv) |
| Exoscale | https://exoscale-prefixes.sos-ch-dk-2.exo.io/exoscale_prefixes.json | Direct JSON feed | [JSON](json/exoscale.json) | [TXT](txt/exoscale.txt) | [CSV](csv/exoscale.csv) |
| Telegram | https://core.telegram.org/resources/cidr.txt | Direct text | [JSON](json/telegram.json) | [TXT](txt/telegram.txt) | [CSV](csv/telegram.csv) |
| Cloudflare | IPv4: https://www.cloudflare.com/ips-v4<br>IPv6: https://www.cloudflare.com/ips-v6 | Direct text files | [JSON](json/cloudflare.json) | [TXT](txt/cloudflare.txt) | [CSV](csv/cloudflare.csv) |
| Akamai | https://techdocs.akamai.com/property-manager/pdfs/akamai_ipv4_ipv6_CIDRs-txt.zip | Direct ZIP | [JSON](json/akamai.json) | [TXT](txt/akamai.txt) | [CSV](csv/akamai.csv) |
| Alibaba | RADB::AS-ALIBABA-CN-NET, AS134963 | RADB AS-SET | [JSON](json/alibaba.json) | [TXT](txt/alibaba.txt) | [CSV](csv/alibaba.csv) |
| Hetzner | RADB::AS-HETZNER | RADB AS-SET | [JSON](json/hetzner.json) | [TXT](txt/hetzner.txt) | [CSV](csv/hetzner.csv) |
| Huawei Cloud | RADB::AS-HUAWEI | RADB AS-SET | [JSON](json/huawei-cloud.json) | [TXT](txt/huawei-cloud.txt) | [CSV](csv/huawei-cloud.csv) |
| IBM/Softlayer (`softlayer_ibm`) | RADB::AS-SOFTLAYER | RADB AS-SET | [JSON](json/softlayer-ibm.json) | [TXT](txt/softlayer-ibm.txt) | [CSV](csv/softlayer-ibm.csv) |
| Meta Crawler | RADB::AS-FACEBOOK | RADB AS-SET | [JSON](json/meta-crawler.json) | [TXT](txt/meta-crawler.txt) | [CSV](csv/meta-crawler.csv) |
| nForce | RADB::AS-NFORCE | RADB AS-SET | [JSON](json/nforce.json) | [TXT](txt/nforce.txt) | [CSV](csv/nforce.csv) |
| Online SAS | RADB::AS-ONLINESAS | RADB AS-SET | [JSON](json/onlinesas.json) | [TXT](txt/onlinesas.txt) | [CSV](csv/onlinesas.csv) |
| OVH | RADB::AS-OVH | RADB AS-SET | [JSON](json/ovh.json) | [TXT](txt/ovh.txt) | [CSV](csv/ovh.csv) |
| Rackspace | RADB::AS-RACKSPACE | RADB AS-SET | [JSON](json/rackspace.json) | [TXT](txt/rackspace.txt) | [CSV](csv/rackspace.csv) |
| Tencent | RADB::AS132203:AS-TENCENT | RADB AS-SET | [JSON](json/tencent.json) | [TXT](txt/tencent.txt) | [CSV](csv/tencent.csv) |
| Vercel | RDAP/ARIN registry-owned netblocks | RDAP/ARIN registry | [JSON](json/vercel.json) | [TXT](txt/vercel.txt) | [CSV](csv/vercel.csv) |
| Backblaze | https://www.backblaze.com/computer-backup/docs/backblaze-ip-addresses | Structured docs scrape | [JSON](json/backblaze.json) | [TXT](txt/backblaze.txt) | [CSV](csv/backblaze.csv) |
| Cisco Webex | https://help.webex.com/article/WBX000028782/Network-Requirements-for-Webex-Teams-Services<br>https://help.webex.com/en-us/article/WBX264/How-Do-I-Allow-Webex-Meetings-Traffic-on-My-Network | Structured docs scrape | [JSON](json/cisco-webex.json) | [TXT](txt/cisco-webex.txt) | [CSV](csv/cisco-webex.csv) |
| Scaleway | https://www.scaleway.com/en/docs/account/reference-content/scaleway-network-information/ | Structured docs scrape | [JSON](json/scaleway.json) | [TXT](txt/scaleway.txt) | [CSV](csv/scaleway.csv) |

## Notes

* Some providers use ASN prefixes, which are now resolved via RIPEstat "Announced Prefixes" for BGP-announced prefixes, with HackerTarget as fallback.
* Vercel uses RDAP/ARIN registry lookups to emit Vercel-owned netblocks only (not cloud egress/edge IPs).
* All JSON outputs include metadata: provider_id, method, coverage_notes, generated_at, source_updated_at, and source_http.
* CI workflows use `--max-delta-ratio` to reject runs with extreme IP count changes.
* Misc providers (like Starlink ISP) are excluded from default runs and saved to the `misc/` directory.
* Consolidated files containing all providers' data are available as [all-providers.json](json/all-providers.json), [all-providers.txt](txt/all-providers.txt), and [all-providers.csv](csv/all-providers.csv).
