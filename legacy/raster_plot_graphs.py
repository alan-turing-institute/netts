
# Plotting
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

# Data Processing
import numpy as np
import pandas as pd
import datetime
import re
import networkx as nx


# --------------------- Raster Plot of all Graphs ---------------------------------------
fig = plt.figure(figsize=(25.6, 20))
for g, G in enumerate(graphs):
    ax = plt.subplot(np.ceil(np.sqrt(len(graphs))),
                     np.ceil(np.sqrt(len(graphs))), g + 1)
    pos = nx.spring_layout(G)
    plt.axis("off")
    nx.draw_networkx_nodes(G, pos, node_size=20)
    nx.draw_networkx_edges(G, pos, alpha=0.4)

# --- Optional: Save plot ---
output_figures = '/path/to/output/figures'
output = op.join(output_figures, 'GraphsRaster_' +
                 '_{0}'.format(str(datetime.date.today())))
plt.savefig(output)
plt.show()
