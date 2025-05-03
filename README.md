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
* Oracle Cloud - https://docs.oracle.com/iaas/tools/public_ip_ranges.json
* Linode - https://geoip.linode.com/
* Vultr - https://geofeed.constant.com/?json
* GitHub - https://api.github.com/meta
* Apple iCloud - https://mask-api.icloud.com/egress-ip-ranges.csv
* Akamai - https://techdocs.akamai.com/property-manager/pdfs/akamai_ipv4_ipv6_CIDRs-txt.zip
* Zscaler - https://config.zscaler.com/api/zscaler.net/hubs/cidr/json/
* Fastly - https://api.fastly.com/public-ip-list
* Microsoft Azure - https://azservicetags.azurewebsites.net/

### Missing data (to add)

* Tencent Cloud
* Alibaba Cloud (Aliyun)
* IBM
* ucloud