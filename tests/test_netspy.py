# pylint: disable=C0114, C0116
import netspy
from netspy import __version__
from netspy.speech_graph import plot_graph, speech_graph


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_speech_graph() -> None:
    text = open("demo_data/3138838-TAT10.txt", "r")
    transcript = text.read()
    text.close()
    graph1 = speech_graph(transcript)
    # assert graph1.__dict__ == graph2.__dict__
    expected_node_list1 = [
        "girl",
        "maid",
        "very dismissive",
        "away",
        "upset",
        "it",
        "exactly",
        "i",
        "eyes",
        "closed",
        "interested at all",
        "book",
        "something",
        "hands",
        "mouth",
        "young",
    ]
    expected_edges1 = [
        ("girl", "maid"),
        ("girl", "very dismissive"),
        ("girl", "away"),
        ("girl", "upset"),
        ("girl", "it"),
        ("girl", "interested at all"),
        ("girl", "book"),
        ("girl", "girl"),
        ("girl", "young"),
        ("maid", "girl"),
        ("it", "exactly"),
        ("i", "it"),
        ("eyes", "closed"),
        ("eyes", "girl"),
        ("book", "girl"),
        ("something", "hands"),
        ("hands", "girl"),
        ("mouth", "girl"),
    ]

    expected_degree1 = [
        ("girl", 15),
        ("maid", 2),
        ("very dismissive", 1),
        ("away", 1),
        ("upset", 1),
        ("it", 3),
        ("exactly", 1),
        ("i", 1),
        ("eyes", 2),
        ("closed", 1),
        ("interested at all", 1),
        ("book", 2),
        ("something", 1),
        ("hands", 2),
        ("mouth", 1),
        ("young", 1),
    ]
    assert list(graph1.nodes()) == expected_node_list1
    assert list(graph1.edges()) == expected_edges1
    assert list(graph1.degree()) == expected_degree1

    text2 = open("demo_data/3138838-TAT13.txt", "r")
    transcript2 = text2.read()
    text2.close()
    graph2 = speech_graph(transcript2)
    expected_node_list2 = [
        "it",
        "midday",
        "hats",
        "heads",
        "the men",
        "presumably",
        "tired",
        "i",
        "sort",
        "picture",
        "floor",
        "one of the men",
        "pain",
        "he",
        "asleep or very tired",
        "man",
        "this",
        "one",
        "men",
        "face",
        "person",
        "all",
    ]
    expected_edges2 = [
        ("it", "midday"),
        ("hats", "heads"),
        ("hats", "the men"),
        ("heads", "the men"),
        ("the men", "presumably"),
        ("the men", "tired"),
        ("the men", "the men"),
        ("the men", "sort"),
        ("the men", "picture"),
        ("the men", "floor"),
        ("i", "the men"),
        ("i", "this"),
        ("one of the men", "pain"),
        ("he", "asleep or very tired"),
        ("man", "he"),
        ("man", "the men"),
        ("one", "the men"),
        ("one", "men"),
        ("face", "person"),
        ("all", "the men"),
    ]
    expected_degree2 = [
        ("it", 1),
        ("midday", 1),
        ("hats", 2),
        ("heads", 2),
        ("the men", 13),
        ("presumably", 1),
        ("tired", 1),
        ("i", 2),
        ("sort", 1),
        ("picture", 1),
        ("floor", 1),
        ("one of the men", 1),
        ("pain", 1),
        ("he", 2),
        ("asleep or very tired", 1),
        ("man", 2),
        ("this", 1),
        ("one", 2),
        ("men", 1),
        ("face", 1),
        ("person", 1),
        ("all", 1),
    ]
    assert list(graph2.nodes()) == expected_node_list2
    assert list(graph2.edges()) == expected_edges2
    assert list(graph2.degree) == expected_degree2
