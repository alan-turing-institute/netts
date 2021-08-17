# Answer to https://stackoverflow.com/questions/10379448/plotting-directed-graphs-in-python-in-a-way-that-show-all-edges-separately

from graphviz import Digraph

dot = Digraph()
dot.node('A', 'A')
dot.node('B', 'B')
dot.node('C', 'C')
dot.edges(['AB', 'AB', 'AB', 'BC', 'BA', 'CB'])

print(dot.source)
dot.render(file_name, view=True)
