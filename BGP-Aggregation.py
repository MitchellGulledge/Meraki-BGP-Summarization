import requests, json, time
import meraki
import ast
from netaddr import *

# Meraki credentials are placed below
meraki_config = {
	'api_key': "",
	'org_name': ""
}

# this function obtains the org ID by inputting org name and API key
mdashboard = meraki.DashboardAPI(meraki_config['api_key'])
result_org_id = mdashboard.organizations.getOrganizations()
for x in result_org_id:
    if x['name'] == meraki_config['org_name']:
        meraki_config['org_id'] = x['id']

# this function maps the network name to obtain the network ID
def get_net_id(net_name):
    # performing org wide API call
    meraki_network_list = mdashboard.networks.getOrganizationNetworks(meraki_config['org_id'])
    # iterating through list to match network with net_name
    for networks in meraki_network_list:
    # if statement matching on the network name and net_name variable user inputs
        if net_name == networks['name']:
            # variable to hold the network ID of the specified net name 
            get_net_id.network_id = networks['id']

# this function performs an org wide Meraki call for all sites VPN statuses
# not using the SDK for this call as it is currently unavailable for now..
def org_wide_vpn_status(list_of_meraki_ids):
    # defining the URL for the GET below
    org_vpn_url = 'https://api.meraki.com/api/v1/organizations/'\
        +meraki_config['org_id']+'/appliance/vpn/statuses?networkIds[]='\
            +(list_of_meraki_ids) # this is the hubs network id
    # creating the header in order to authenticate the call
    header = {"X-Cisco-Meraki-API-Key": meraki_config['api_key'], "Content-Type": "application/json"}
    # performing API call to meraki dashboard
    vpn_statuses = requests.get(org_vpn_url, headers=header).content
    # vpn_status is a data type of bytes, going to convert to a string then adictionary
    decoded_vpn_statuses = vpn_statuses[1:-1].decode("UTF-8") # parsing outer brackets
    # converting string to dictionary
    meraki_vpn_peers = ast.literal_eval(decoded_vpn_statuses)
    # parsing list to just meraki vpn peers
    list_of_peers = meraki_vpn_peers['merakiVpnPeers']
    # creating list as placeholder for later call
    list_of_bgp_peers = []
    # creating list to hold all Auto VPN subnets connected to this hub
    list_of_bgp_prefixes = []
    # iterating through list of peers to create a list of network ids
    for peers in list_of_peers:
        # creating variable to match on network ID to later append to list of IDs for org wide call
        ibgp_peer = peers['networkId']
        # appending the ibgp_peer to the list_of_bgp_peers list
        list_of_bgp_peers.append(ibgp_peer)
        mx_subnets = mdashboard.networks.getNetworkSiteToSiteVpn(ibgp_peer) # gets branch subnets
        in_meraki_vpn = ([x['localSubnet'] for x in mx_subnets['subnets'] \
            if x['useVpn'] == True])  # list comprehension to filter for subnets in vpn
        # concatanating prefix/s to the list list_of_bgp_prefixes
        list_of_bgp_prefixes = list_of_bgp_prefixes + in_meraki_vpn
    # summarizing the list of prefixes created
    summarized_prefixes = cidr_merge(list_of_bgp_prefixes)
    # creating aggregate address statements from summarized prefix
    formatted_prefixes = str(summarized_prefixes).replace("IPNetwork('","aggregate-address ")
    finalized_formatted_prefixes = str(formatted_prefixes).replace ("')", " summary-only")
    print(finalized_formatted_prefixes)

# below is the list of network IDs that are built with the get_meraki_networks_by_tag() function
get_net_id("enter your dashboard network name here") # statically defining the network name here
org_wide_vpn_status(get_net_id.network_id)
