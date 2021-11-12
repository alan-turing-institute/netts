import pickle

with open("transcript.pkl", "rb") as graph_file:
    graph = pickle.load(graph_file)

print(type(graph))
