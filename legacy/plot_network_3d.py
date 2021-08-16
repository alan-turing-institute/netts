
import plotly.graph_objects as go
# Graph analysis functions
from compile_graphs_dataset import get_graphs, graph_properties, exclude_empty_graphs
from graph_analysis_functions import print_bidirectional_edges, print_parallel_edges, get_parallel_edges, central_words, calc_vector_distance, calc_vector_distance_adj, choose_representative_word, find_representative_node_words

# --------------------- Import graphs ---------------------------------------
graph_dir = '/Users/CN/Dropbox/speech_graphs/all_tats'
graphs, filelist = get_graphs(graph_dir)
graphs, filelist = exclude_empty_graphs(graphs, filelist, be_quiet=True)

max_x_G = graphs[int(max_x[0])]
max_y_G = graphs[int(max_y[0])]
max_z_G = graphs[int(max_z[0])]
G = graphs[0]
G = nx.convert_node_labels_to_integers(G)
spring_3D = nx.spring_layout(G, dim=3, seed=18)

# we need to seperate the X,Y,Z coordinates for Plotly
x_nodes = [spring_3D[i][0]
           for i in range(len(G.nodes()))]  # x-coordinates of nodes
y_nodes = [spring_3D[i][1] for i in range(len(G.nodes()))]  # y-coordinates
z_nodes = [spring_3D[i][2] for i in range(len(G.nodes()))]  # z-coordinates

# We also need a list of edges to include in the plot
edge_list = G.edges()

# we  need to create lists that contain the starting and ending coordinates of each edge.
x_edges = []
y_edges = []
z_edges = []
# need to fill these with all of the coordiates
for edge in edge_list:
    #format: [beginning,ending,None]
    x_coords = [spring_3D[edge[0]][0], spring_3D[edge[1]][0], None]
    x_edges += x_coords
    #
    y_coords = [spring_3D[edge[0]][1], spring_3D[edge[1]][1], None]
    y_edges += y_coords
    #
    z_coords = [spring_3D[edge[0]][2], spring_3D[edge[1]][2], None]
    z_edges += z_coords


# create a trace for the edges
trace_edges = go.Scatter3d(x=x_edges,
                           y=y_edges,
                           z=z_edges,
                           mode='lines',
                           line=dict(color='black', width=2),
                           hoverinfo='none')

# create a trace for the nodes
trace_nodes = go.Scatter3d(x=x_nodes,
                           y=y_nodes,
                           z=z_nodes,
                           mode='markers',
                           marker=dict(symbol='circle',
                                       size=10,
                                       color='green',  # color the nodes according to their community
                                       # either green or mageneta
                                       colorscale=['lightgreen', 'magenta'],
                                       line=dict(color='black', width=0.5)),
                           hoverinfo='text')

# we need to set the axis for the plot
axis = dict(showbackground=False,
            showline=False,
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title='')

# also need to create the layout for our plot
layout = go.Layout(title="Two Predicted Factions of Zachary's Karate Club",
                   width=650,
                   height=625,
                   showlegend=False,
                   scene=dict(xaxis=dict(axis),
                              yaxis=dict(axis),
                              zaxis=dict(axis),
                              ),
                   margin=dict(t=100),
                   hovermode='closest')

# Include the traces we want to plot and create a figure
data = [trace_edges, trace_nodes]
fig = go.Figure(data=data, layout=layout)

fig.show()
