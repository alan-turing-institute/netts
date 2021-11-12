import matplotlib.pyplot as plt

import netts

settings = netts.get_settings()
print(f"Installing dependencies to {settings.netts_dir}")
netts.install_dependencies()

with netts.OpenIEClient() as openie_client, netts.CoreNLPClient(
    properties={"annotators": "tokenize,ssplit,pos,lemma,parse,depparse,coref,openie"},
) as corenlp_client:

    with open("transcript.txt", encoding="utf-8") as f:
        transcript = f.read()

    graph = netts.SpeechGraph(transcript)

    graph.process(
        openie_client=openie_client,
        corenlp_client=corenlp_client,
        preprocess_config=settings.netts_config.preprocess,
    )

fig, ax = plt.subplots()
graph.plot_graph(ax)

plt.savefig("transcript.png")

with open("transcript.pkl", "wb") as output_f:
    netts.pickle_graph(graph.graph, output_f)
