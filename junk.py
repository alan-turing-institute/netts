'density',
'diameter',
'average_shortest_path',
'clustering',
# edge_list = list(G.edges(data=False))
# nx.write_edgelist(my_G, "test.edgelist", data=False)
# nx.read_edgelist(my_G, "test.edgelist", data=False)
# edge_dict = dict(my_G.edges)


# data = {1: edge_list}
data = {1: [edge_list]}
key = 1
graphs = data[key]
index = 0
G = graphs[0]

# graph = nx.DiGraph(G)

degree = 0

np.count_nonzero(G) < len(G) * degree

graph = nx.DiGraph(G > threshold)

import FinalMotif as fm
fm.findMotifs(data, key, motifSize=3, degree=degree,
              randGraphs=None, useCache=True)


# objects = []
# with (open("aznorbert_corrsd_new.pkl", "rb")) as openfile:
#     while True:
#         try:
#             objects.append(pickle.load(openfile))
#         except EOFError:
#             break

with open("aznorbert_corrsd_new.pkl", mode='r+b', encoding='utf-8') as handle:
    tfidf_vectorizer = pickle.load(handle)


g = my_G

# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
# PCA Stuff
