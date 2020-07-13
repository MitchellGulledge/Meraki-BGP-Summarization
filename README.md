# Meraki BGP Summarization Toolkit

The Cisco Meraki BGP Summarization Toolkit was built to enable aggregate routing within the datacenter. This toolkit enables the automation of aggregate routes to be later placed in the config file of the upstream IOS/XE device. 

This toolkit enables the automation of aggregate (summary) addresses to be applied to the upstream router of the MX BGP concentrator.
Customers will need to provide 3 variables in order to utilize the toolkit:

- Organization Name
- API Key
- Network name of the concentrator performing EBGP

The netaddr library is used to summarize the list of prefixes obtained from the Meraki API. More information on the netaddr library can be found here: https://netaddr.readthedocs.io/en/latest/tutorial_01.html#summarizing-list-of-addresses-and-subnets

A reference architecture can be seen below:

[Cisco Meraki BGP Summarization Architectue](https://app.lucidchart.com/documents/view/4ba9e8e6-7b73-4d8f-b936-1c6a073ccec1)
