
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
