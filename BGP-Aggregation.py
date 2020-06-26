import requests
import json
import time
import meraki
import logging
import re
import urllib.request
import os
import datetime as dt
from datetime import datetime, timedelta
import ast
from netaddr import *
import pprint

# Meraki credentials are placed below
meraki_config = {
	'api_key': "",
	'orgName': ""
}

# writing function to obtain org ID via linking ORG name
mdashboard = meraki.DashboardAPI(meraki_config['api_key'])
result_org_id = mdashboard.organizations.getOrganizations()
for x in result_org_id:
    if x['name'] == meraki_config['orgName']:
        meraki_config['org_id'] = x['id']

# branch subnets is a variable to display local branch site info
branchsubnets = []
# variable with new and existing s2s VPN config
merakivpns = []

# performing initial get to obtain all Meraki existing VPN info to add to merakivpns list above
originalvpn = mdashboard.organizations.getOrganizationThirdPartyVPNPeers(
    meraki_config['org_id']
)
merakivpns.append(originalvpn)

# Meraki call to obtain Network information
tagsnetwork = mdashboard.networks.getOrganizationNetworks(meraki_config['org_id'])

# place holder list that prefixes will be appended to
list_of_prefixes = []

# loop that iterates through the variable tagsnetwork and matches networks with vWAN in the tag
for i in tagsnetwork:
    if i['tags'] is None or i['name'] == 'Tag-Placeholder':
        pass
    elif "2914:2346" in i['tags']:
        network_info = i['id'] # need network ID in order to obtain device/serial information
        netname = i['name'] # network name used to label Meraki VPN and Azure config
        nettag = i['tags']  # obtaining all tags for network as this will be placed in VPN config
        va = mdashboard.networks.getNetworkSiteToSiteVpn(network_info) # gets branch local vpn subnets
        testextract = ([x['localSubnet'] for x in va['subnets']
						if x['useVpn'] == True])  # list comprehension to filter for subnets in vpn
        (testextract)
        print(testextract)
        list_of_prefixes = list_of_prefixes + testextract

print(list_of_prefixes)
print(cidr_merge(list_of_prefixes)) # netaddr package autosummarizes prefixes in list of prefixes
