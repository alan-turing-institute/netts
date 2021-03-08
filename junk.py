
ollie_edges, ollie_edges_text_excerpts, ollie_one_node_edges, ollie_one_node_edges_text_excerpts = create_edges_ollie(
    ex_ollie)

edges = ollie_edges


stanza_edges, stanza_edges_text_excerpts = create_edges_stanza(ex_stanza)


no_noun, poss_pronouns, dts, nouns, nouns_origtext, adjectives = get_word_types(
    ex_stanza)

adjectives, adjective_edges = get_adj_edges(ex_stanza)

prepositions, preposition_edges = get_prep_edges(ex_stanza)

obliques, oblique_edges = get_obl_edges(ex_stanza)


add_obl_edges(edges, oblique_edges)

edges = add_obl_edges(edges, oblique_edges)

node_name_synonyms = get_node_synonyms(ex_stanza)


edges, node_name_synonyms = split_node_synonyms(
    node_name_synonyms, preposition_edges, edges)

edges = split_nodes(edges, preposition_edges)

edges, orig_edges = merge_corefs(edges, node_name_synonyms)

edges = clean_nodes(edges)

edges = add_adj_edges(edges, adjective_edges, add_adjective_edges=True)


edges = add_prep_edges(edges, preposition_edges,
                       add_all_preposition_edges=True)

unconnected_nodes = get_unconnected_nodes(edges, orig_edges)


def display_closestwords_tsnescatterplot(model, word):
    # from https://medium.com/@aneesha/using-tsne-to-plot-a-subset-of-similar-words-from-word2vec-bb8eeaea6229
    #
    # load pre-trained word2vec embeddings
    # The embeddings were downloaded from command prompt:
    # wget -c "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"

    #
    arr = np.empty((0, 300), dtype='f')
    word_labels = [word]
    #
    # get close words
    close_words = model.similar_by_word(word)
    #
    # add the vector for each of the closest words to the array
    arr = np.append(arr, np.array([model[word]]), axis=0)
    for wrd_score in close_words:
        wrd_vector = model[wrd_score[0]]
        word_labels.append(wrd_score[0])
        arr = np.append(arr, np.array([wrd_vector]), axis=0)
    #
    # find tsne coords for 2 dimensions
    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(arr)
    #
    x_coords = Y[:, 0]
    y_coords = Y[:, 1]
    # display scatter plot
    plt.scatter(x_coords, y_coords)
    #
    for label, x, y in zip(word_labels, x_coords, y_coords):
        plt.annotate(label, xy=(x, y), xytext=(
            0, 0), textcoords='offset points')
    plt.xlim(x_coords.min() + 0.00005, x_coords.max() + 0.00005)
    plt.ylim(y_coords.min() + 0.00005, y_coords.max() + 0.00005)
    plt.show()

# # Save the image in the img folder:
# wordcloud.to_file("img/first_review.png")


# word = 'lamppost'
# doc = nlp(word)
# doc.lemma
# print(
#     *[f'word: {word.text+" "}\tlemma: {word.lemma}' for sent in doc.sentences for word in sent.words], sep='\n')


# for i in nx.weakly_connected_components(G):
#     print(i)
# for c in sorted(nx.weakly_connected_components(G), key=len, reverse=True):
#     print(nx.average_shortest_path_length(c))
# # --------------------- Visualise parallel edges-----------------------------------
# # for g, G in enumerate(graphs):
# # Plot graph as matrix
# fig, ax = plt.subplots()
# arr = nx.to_numpy_matrix(G)
# im = plt.imshow(arr, interpolation='nearest', cmap='gray')
# node_labels = list(G.nodes())
# ax.set_xticks(np.arange(len(node_labels)))
# ax.set_xticklabels(node_labels)
# ax.set_yticks(np.arange(len(node_labels)))
# ax.set_yticklabels(node_labels)
# plt.show()

# --------------------- Print parallel edges ---------------------------------------
# Print all parallel edge data
for g, G in enumerate(graphs):
    # print('\n', filelist[g].split('SpeechGraph_')[1])
    arr = nx.to_numpy_matrix(G)
    boo = (arr >= 2)
    if boo.any():
        parallel_edges = np.where(boo)
        node_labels = list(G.nodes())
        # print info for all parallel edges
        for p in range(0, parallel_edges[0].shape[0]):
            node1 = node_labels[parallel_edges[0][p]]
            node2 = node_labels[parallel_edges[1][p]]
            print('\n', g, ' : ', node1, node2)
            # print(node1, node2)
            # par_edges_info = G.get_edge_data(node1, node2)
            # print([edge_info['confidence']
            #        for edge_info in par_edges_info.values()])
            # print([edge_info['relation']
            #        for edge_info in par_edges_info.values()])
            #             pprint(par_edges_info)
# ---> There are no parallel edges after the edge cleaning!

# # --------------------- Get edge labels ---------------------------------------
# edge_labels = dict([((u, v,), d['relation'])
#                     for u, v, d in G.edges(data=True)])


# ----------- Get largest connected component -----------
largest = max(nx.strongly_connected_components(G), key=len)
weakest = max(nx.weakly_connected_components(G), key=len)

# ----------- Size of largest connected component -----------
# Not implemented for directed graphs. See:
# https://stackoverflow.com/questions/47283612/networkx-node-connected-component-not-implemented-for-directed-type
# ----------- Average size of most connected component -----------
# ----------- Average shortest path length for each connected component -----------
for C in (G.subgraph(c).copy() for c in nx.strongly_connected_components(G)):
    print(nx.average_shortest_path_length(C))
# ----------- Motifs -----------
# ----------- XX -----------
for m, M in enumerate(graphs):
    print(' ')
    DG = nx.DiGraph()
    for u, v, d in M.edges(data=True):
        if DG.has_edge(u, v):
            # print('MultiEdge in graph{}'.format(m))
            print('{} {} \t {} / {} || {} / {} || {}'.format(u, v,
                                                             d['relation'], DG[u][v]['relation'],
                                                             d['extractor'], DG[u][v]['extractor'],
                                                             d['sentence'] == DG[u][v]['sentence']))
            DG[u][v]['weight'] += 1
        else:
            DG.add_edge(u, v,
                        relation=d['relation'],
                        extractor=d['extractor'],
                        sentence=d['sentence'], weight=1)

# Make MultiDiGraph into DiGraph by setting weights as number of edges
for M in graphs:
    DG = nx.DiGraph()
    for u, v in M.edges():
        if DG.has_edge(u, v):
            DG[u][v]['weight'] += 1
        else:
            DG.add_edge(u, v, weight=1)
    #
    # Draw graph weighted by number of edges between nodes
    pos = nx.spring_layout(DG)
    weights = nx.get_edge_attributes(DG, 'weight')
    weights = weights.values()
    options = {
        "node_color": "#A0CBE2",
        "edge_color": weights,
        "width": 4,
        "edge_cmap": plt.cm.Blues,
        "with_labels": False,
    }
    nx.draw(DG, pos, **options)
    edge_labels = dict([((u, v,), d['relation'])
                        for u, v, d in M.edges(data=True)])
    nx.draw_networkx_edge_labels(
        DG, pos, edge_labels=edge_labels, font_color='red')
    plt.show()

# create weighted graph from M
# G = nx.DiGraph()
for u, v in M.edges():
    if G.has_edge(u, v):
        G[u][v]['weight'] += 1
    else:
        G.add_edge(u, v, weight=1)


clustering = nx.clustering(G, weight='weight')
# --------------------- Make directed multigraph into undirected graph ---------------------------------------
G = G.to_undirected()
G = nx.Graph(G)
# --------------------- Get graph properties ---------------------------------------
# size, clustering, path lengths

# Size
G.size()
# Clustering
nx.clustering(G)
nx.average_clustering(G)
nx.generalized_degree(G)
# Path lengths
nx.non_randomness(G)
len(G.edges())
len(G.nodes())
nx.shortest_path_length(G)
# Efficiency
nx.global_efficiency(G)
nx.local_efficiency(G)

# Find parallel edges
for G in graphs:
    # For every node in graph
    for node in G.nodes():
        # We look for adjacent nodes
        for adj_node in G[node]:
            # If adjacent node has an edge to the first node
            # Or our graph have several edges from the first to the adjacent node
            if node != adj_node and node in G[adj_node] or len(G[node][adj_node]) > 1:
                # DO MAGIC!!
                print(node, adj_node)


# Construct Speech Graphs
# G = nx.read_gpickle((graph))

weights = nx.get_edge_attributes(G, 'confidence')
weights = weights.values()


# If I change the arrowstyle (to get a bigger arrowhead), the graphs are not curved anymore
node_labels = {node: node for node in G.nodes()}
options_graph = {
    "node_color": "pink",
    "node_size": 2000,
    "font_size": 18,
    "alpha": 0.9,
    "arrowsize": 20,
    "arrowstyle": "-|>",
    "labels": node_labels,
    "edge_color": "black",
    "width": 1,
    "linewidths": 1,
    "edge_cmap": plt.cm.Blues,
    # "connectionstyle" :’arc1,rad : 0.9’
}
pos = nx.spring_layout(G)
# pos = nx.circular_layout(G)
nx.draw(G, pos, **options_graph)


edge_labels = dict([((u, v,), d['relation'])
                    for u, v, d in G.edges(data=True)])
options_edge_label = {
    "edge_labels": edge_labels,
    "font_color": 'red',
    "font_size": 12
}
nx.draw_networkx_edge_labels(G, pos, **options_edge_label)
plt.axis('off')
plt.show()

# --------------------- Plot graph ---------------------------------------
pos = nx.spring_layout(G)
nx.draw(G, pos,
        edge_color='black',
        width=1,
        linewidths=1,
        node_size=500,
        node_color='pink',
        alpha=0.9,
        labels={node: node for node in G.nodes()})
edge_labels = dict([((u, v,), d['relation'])
                    for u, v, d in G.edges(data=True)])
nx.draw_networkx_edge_labels(
    G, pos, edge_labels=edge_labels, font_color='red')
plt.show(block=False)
