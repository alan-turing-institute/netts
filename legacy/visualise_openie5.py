#!/Users/CN/Documents/Projects/Cambridge/language_analysis/venv python
# ------------------------------------------------------------------------------
# Script name:  first_steps_openie5.py
#
# Description:
#               First steps using OpenIE5 (successor to OLLIE): the principal Open Information Extraction (Open IE) system from the University of Washington (UW) and Indian Institute of Technology,Delhi (IIT Delhi)
#
# Author:       Caroline Nettekoven, 2020
#
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
from pyopenie import OpenIE5
extractor = OpenIE5('http://localhost:8000')


extractions = extractor.extract(
    "But the man on the picture seems to wear a hat and, and has a jacket on and he seems to have a hoodie on as well.")

edges = []
edges_labels = {}
# Create nodes and edges
for e, extract in enumerate(extractions):
    # print(e, extract)
    node1 = extract['extraction']['arg1']['text']
    node2 = ''
    for arg2_no, arg2 in enumerate(extract['extraction']['arg2s']):
        # print(arg_no, arg['text'])
        node2 = node2 + ' ' + arg2['text']
        print(node2)
    if node2 != '':
        edges.append([node1, node2])
        edges_labels[(node1, node2)] = extract['extraction']['rel']['text']


# Create empty graph
G = nx.Graph()

# Plot graph
G.add_edges_from(edges)
pos = nx.spring_layout(G)

plt.figure()
nx.draw(G, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color='pink', alpha=0.9,
        labels={node: node for node in G.nodes()})
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edges_labels, font_color='red')
plt.axis('off')
plt.show()

# Output is a json that looks like this:
output = [
    {'confidence': 0.41051436014453063, 'sentence': 'But the man....', 'extraction': {
     'arg1': {'text': 'he', 'offsets': [[4, 5]]},
     'rel': {'text': 'to have', 'offsets': [[13, 14, 15, 16, 17, 18, 19]]},
     'arg2s': [{'text': 'a hoodie on', 'offsets': [[21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]]},
               {'text': 'as well', 'offsets': [[33, 34, 35, 36, 37, 38, 39]]}], 'context': None, 'negated': False, 'passive': False}},
    {'confidence': 0.1948871917044894, 'sentence': 'But the man....', 'extraction': {
     'arg1': {'text': 'he', 'offsets': [[4, 5]]},
     'rel': {'text': 'seems', 'offsets': [[7, 8, 9, 10, 11]]},
     'arg2s': [], 'context': None, 'negated': False, 'passive': False}},
    {'confidence': 0.9005286127300474, 'sentence': 'But the man....', 'extraction': {
     'arg1': {'text': 'the man', 'offsets': [[4, 5, 6, 7, 8, 9, 10]]},
     'rel': {'text': 'has on', 'offsets': [[12, 13, 14], [25, 26]]},
     'arg2s': [{'text': 'a jacket', 'offsets': [[16, 17, 18, 19, 20, 21, 22, 23]]}], 'context': None, 'negated': False, 'passive': False}},
    {'confidence': 0.913197594301744, 'sentence': 'But the man....', 'extraction': {
     'arg1': {'text': 'the man on the picture', 'offsets': [[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]]},
     'rel': {'text': 'to wear', 'offsets': [[33, 34, 35, 36, 37, 38, 39]]},
     'arg2s': [{'text': 'a hat', 'offsets': [[41, 42, 43, 44, 45]]}], 'context': None, 'negated': False, 'passive': False}},
    {'confidence': 0.7852615174453589, 'sentence': 'But the man....', 'extraction': {
     'arg1': {'text': 'the man on the picture', 'offsets': [[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]]},
     'rel': {'text': 'seems', 'offsets': [[27, 28, 29, 30, 31]]},
     'arg2s': [], 'context': None, 'negated': False, 'passive': False}}]


# Accessing individual properties:
extractions[0]
extractions[0]['confidence']
extractions[0]['extraction']['arg1']['text']
