# -*- coding: utf-8 -*-
with open('demos/data/sitedata_unlimit4.csv', 'r', encoding="utf-8") as f:
    network_data = f.read().split('\n')

# We select the first 750 edges and associated nodes for an easier visualization
edges = network_data
nodes = set()

cy_nodes = {}
cy_urls = {}

for network_edge in edges:
    print(network_edge)
    s_url, source, t_url, target, keyword, banner_count = network_edge.split(" ")
    if source not in nodes:
        nodes.add(source)
        cy_nodes[source] = 0
        cy_urls[source] = s_url
    if target not in nodes:
        cy_nodes[source] += 1
        cy_nodes[target] = 0
        cy_urls[target] = t_url

with open('demos/data/result.csv', 'w') as f:
    f.write('ip,weight,url\n')
    for ip in cy_nodes.keys():
        f.write(str(ip)+','+str(cy_nodes[ip])+','+cy_urls[ip]+'\n')

