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
* Apple iCloud - https://mask-api.icloud.com/egress-ip-ranges.csv
* Starlink ISP - https://geoip.starlinkisp.net/feed.csv
* Akamai - https://techdocs.akamai.com/property-manager/pdfs/akamai_ipv4_ipv6_CIDRs-txt.zip
* Zscaler - https://config.zscaler.com/api/zscaler.net/hubs/cidr/json/
* Fastly - https://api.fastly.com/public-ip-list
* Microsoft Azure - https://azservicetags.azurewebsites.net/
* IBM/Softlayer (from ASN Prefix) - AS36351
* Vercel/AWS (from ASN Prefix) - AS15169
* Heroku/AWS (from ASN Prefix) - AS14618
* A2Hosting (from ASN Prefix) - AS55293
* GoDaddy (from ASN Prefix) - AS26496, AS30083
* Dreamhost (from ASN Prefix) - AS26347
* Alibaba (from ASN Prefix) - AS45102, AS134963
* Tencent (from ASN Prefix) - AS45090, AS133478, AS132591, AS132203
* ucloud (from ASN Prefix) - AS135377, AS59077
* Meta Crawler (from ASN Prefix) - AS32934
* Huawei Cloud (from ASN Prefix) - AS136907, AS55990
* Rackspace (from ASN Prefix) - AS39921, AS12200, AS15395, AS44009, AS45187, AS58683, AS27357, AS19994 	(from ASN Prefix)

## Notes

* Some providers use ASN prefixes, which can be resolved using https://api.hackertarget.com/aslookup/?q=AS12345
