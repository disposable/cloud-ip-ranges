# cloud-ip-ranges

The idea of this repository is to have one source for all major cloud providers,
which shows their assigned IP ranges.

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
* Starlink ISP - https://geoip.starlinkisp.net/feed.csv
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
* Vercel - RDAP/ARIN registry-owned netblocks
* Fly.io - BGP-announced prefixes (AS40509)
* Render - BGP-announced prefixes (AS397273)
* IBM/Softlayer (from ASN Prefix) - AS36351
* Heroku/AWS (from ASN Prefix) - AS14618
* A2Hosting (from ASN Prefix) - AS55293
* GoDaddy (from ASN Prefix) - AS26496, AS30083
* Dreamhost (from ASN Prefix) - AS26347
* Alibaba (from ASN Prefix) - AS45102, AS134963
* Tencent (from ASN Prefix) - AS45090, AS133478, AS132591, AS132203
* ucloud (from ASN Prefix) - AS135377, AS59077
* Meta Crawler (from ASN Prefix) - AS32934
* Huawei Cloud (from ASN Prefix) - AS136907, AS55990
* Hetzner (from ASN Prefix) - AS24940, AS37153
* Choopa (from ASN Prefix) - AS46407, AS20473, AS133795, AS11508
* OVH (from ASN Prefix) - AS35540, AS16276
* Online SAS (from ASN Prefix) - AS12876
* Rackspace (from ASN Prefix) - AS58683, AS54636, AS45187, AS39921, AS36248, AS27357, AS22720, AS19994, AS15395, AS12200, AS10532
* nForce (from ASN Prefix) - AS64437, AS43350

## Notes

* Some providers use ASN prefixes, which are now resolved via RIPEstat “Announced Prefixes” for BGP-announced prefixes, with HackerTarget as fallback.
* Vercel uses RDAP/ARIN registry lookups to emit Vercel-owned netblocks only (not cloud egress/edge IPs).
* All JSON outputs include metadata: provider_id, method, coverage_notes, generated_at, source_updated_at, and source_http.
* CI workflows can use `--max-delta-ratio` to reject runs with extreme IP count changes.
