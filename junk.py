

oblique_edges

for e, edge_info in enumerate(edges):
    edge = edge_info[:2]
    for n, node in enumerate(edge):
        # Test if node includes oblique
        for o, oblique_edge in enumerate(oblique_edges):
            oblique = oblique_edge[2]['relation']
            oblique_match_idx = []
            oblique_match_idx = [m for m, match in enumerate(
                node.split(' ')) if oblique == match]
            match_idx = []
            match_idx = [m for m, match in enumerate(
                node.split(' ')) if oblique == match and m > 1]
            if match_idx != []:
                m = match_idx[0]
                part1 = (' ').join(node.split(' ')[:m]).strip()
                part2 = (' ').join(node.split(' ')[m:]).strip()
                new_edge[n] = part1
                print(part1, ' \t\t|\t ', part2)
                # If second part of node is anywhere else in edges, then split
                # Find where part1 does not appear in node but part2 appears (something other than obliques or no_noun element)
                p2_words = [w for w in part2.split(
                    ' ') if not w in no_noun]  # remove stopwords
                p2_list = []
                for x in other_edges:
                    for p2 in p2_words:
                        p2_list.append(p2 in x.split(' '))
                p1_words = [w for w in part1.split(
                    ' ') if not w in no_noun]  # remove stopwords
                p1_list = []
                for x in other_edges:
                    for p1 in p1_words:
                        p1_list.append(p1 not in x.split(' '))
                if any(p1_list and p2_list):
                    print(oblique_edge)
    edges[e] = tuple(new_edge)
    if oblique_edge not in edges:
        edges.append(oblique_edge)


oblique_edges
