# Cloud IP Ranges

The idea of this repository is to have one source for all major cloud providers,
which shows their assigned IP ranges.

**Note:** This repository contains only the output of the crawler. The crawler itself is available on it's own [Repository](https://github.com/disposable/cloud-ip-ranges-crawler) and can be run on your own hardware to generate the latest IP ranges data.

## Data sources

* Amazon Web Services (AWS) - https://ip-ranges.amazonaws.com/ip-ranges.json
* Cloudflare
    * IPv4 - https://www.cloudflare.com/ips-v4
    * IPv6 - https://www.cloudflare.com/ips-v6
* DigitalOcean (DO) - https://digitalocean.com/geo/google.csv
* Google Cloud (GCloud) - https://www.gstatic.com/ipranges/cloud.json
* Google Bot - https://developers.google.com/static/search/apis/ipranges/googlebot.json
* Bing Bot - https://www.bing.com/toolbox/bingbot.json
* Oracle Cloud - https://docs.oracle.com/iaas/tools/public_ip_ranges.json
* Ahrefs - https://api.ahrefs.com/v3/public/crawler-ips
* Linode - https://geoip.linode.com/
* Vultr - https://geofeed.constant.com/?json
* OpenAI - https://openai.com/chatgpt-user.json, https://openai.com/gptbot.json
* Perplexity - https://www.perplexity.ai/perplexitybot.json, https://www.perplexity.ai/perplexity-user.json
* GitHub - https://api.github.com/meta
* Apple Private Relay - https://mask-api.icloud.com/egress-ip-ranges.csv
* Starlink ISP - https://geoip.starlinkisp.net/feed.csv (saved to misc/ directory as user ISP traffic)
* Akamai - https://techdocs.akamai.com/property-manager/pdfs/akamai_ipv4_ipv6_CIDRs-txt.zip
* Zscaler - https://config.zscaler.com/api/zscaler.net/hubs/cidr/json/
* Fastly - https://api.fastly.com/public-ip-list
* Microsoft Azure - https://azservicetags.azurewebsites.net/
* Telegram - https://core.telegram.org/resources/cidr.txt
* WhatsApp - https://developers.facebook.com/docs/whatsapp/guides/network-requirements/
* Atlassian - https://ip-ranges.atlassian.com/
* Datadog - https://ip-ranges.datadoghq.com/
* Okta - https://s3.amazonaws.com/okta-ip-ranges/ip_ranges.json
* Zendesk - https://support.zendesk.com/ips
* CircleCI - https://circleci.com/docs/ip-ranges-list.json
* HCP Terraform - https://app.terraform.io/api/meta/ip-ranges
* New Relic Synthetics - https://nr-synthetics-assets.s3.amazonaws.com/nat-ip-dnsname/production/ip-ranges.json
* Grafana Cloud - https://grafana.com/api/hosted-alerts/source-ips, https://grafana.com/api/hosted-grafana/source-ips, https://grafana.com/api/hosted-metrics/source-ips, https://grafana.com/api/hosted-traces/source-ips, https://grafana.com/api/hosted-logs/source-ips, https://grafana.com/api/hosted-profiles/source-ips, https://grafana.com/api/hosted-otlp/source-ips
* Intercom - https://static.intercomcdn.com/intercom-ips/us/intercom-ip-ranges.json, https://static.intercomcdn.com/intercom-ips/eu/intercom-ip-ranges.json, https://static.intercomcdn.com/intercom-ips/au/intercom-ip-ranges.json
* Stripe - https://stripe.com/files/ips/ips_api.json, https://stripe.com/files/ips/ips_webhooks.json
* Adyen - https://docs.adyen.com/development-resources/security/integration-security/allowlisting
* Salesforce Hyperforce - https://ip-ranges.salesforce.com/ip-ranges.json
* Sentry - https://sentry.io/api/0/uptime-ips/
* Branch - https://help.branch.io/docs/postback-webhook-ip-address-allowlist-expands
* IBM/Softlayer (from RADB AS-SET) - RADB::AS-SOFTLAYER
* Heroku/AWS (from ASN Prefix) - AS14618
* Fly.io (from ASN Prefix) - AS40509
* Render (from ASN Prefix) - AS397273
* A2Hosting (from ASN Prefix) - AS55293
* GoDaddy (from ASN Prefix) - AS26496, AS30083
* Dreamhost (from ASN Prefix) - AS26347
* Alibaba (from RADB AS-SET) - RADB::AS-ALIBABA-CN-NET, AS134963
* Tencent (from RADB AS-SET) - RADB::AS132203:AS-TENCENT
* Ucloud (from ASN Prefix) - AS135377, AS59077
* Meta Crawler (from RADB AS-SET) - RADB::AS-FACEBOOK
* Huawei Cloud (from RADB AS-SET) - RADB::AS-HUAWEI
* Hetzner (from RADB AS-SET) - RADB::AS-HETZNER
* Choopa (from ASN Prefix) - AS46407, AS20473, AS133795, AS11508
* OVH (from RADB AS-SET) - RADB::AS-OVH
* Online SAS (from RADB AS-SET) - RADB::AS-ONLINESAS
* Rackspace (from RADB AS-SET) - RADB::AS-RACKSPACE
* nForce (from RADB AS-SET) - RADB::AS-NFORCE
* Vercel - RDAP/ARIN registry-owned netblocks

## Notes

* Some providers use ASN prefixes, which are now resolved via RIPEstat "Announced Prefixes" for BGP-announced prefixes, with HackerTarget as fallback.
* Vercel uses RDAP/ARIN registry lookups to emit Vercel-owned netblocks only (not cloud egress/edge IPs).
* All JSON outputs include metadata: provider_id, method, coverage_notes, generated_at, source_updated_at, and source_http.
* CI workflows use `--max-delta-ratio` to reject runs with extreme IP count changes.
* Misc providers (like Starlink ISP) are excluded from default runs and saved to the `misc/` directory.
