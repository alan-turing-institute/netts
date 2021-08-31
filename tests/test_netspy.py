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

    text = open("demo_data/3138838-TAT30.txt", "r")
    transcript = text.read()
    text.close()
    graph3 = speech_graph(transcript)
    expected_node_list3 = [
        "i",
        "man",
        "lightbulb",
        "it",
        "middle",
        "there",
        "picture",
        "dark",
        "anything",
        "hoodie",
        "jacket",
        "hat",
        "concept",
        "very , very mysterious",
        "standing",
        "post",
        "night",
        "balls",
        "reflections",
        "context",
        "light",
    ]
    expected_edges3 = [
        ("i", "man"),
        ("i", "lightbulb"),
        ("i", "anything"),
        ("i", "concept"),
        ("i", "picture"),
        ("man", "hoodie"),
        ("man", "jacket"),
        ("man", "hat"),
        ("man", "picture"),
        ("man", "standing"),
        ("man", "post"),
        ("it", "middle"),
        ("it", "dark"),
        ("middle", "night"),
        ("there", "picture"),
        ("picture", "very , very mysterious"),
        ("standing", "dark"),
        ("post", "light"),
        ("balls", "reflections"),
        ("context", "picture"),
    ]
    expected_degree3 = [
        ("i", 5),
        ("man", 7),
        ("lightbulb", 1),
        ("it", 2),
        ("middle", 2),
        ("there", 1),
        ("picture", 5),
        ("dark", 2),
        ("anything", 1),
        ("hoodie", 1),
        ("jacket", 1),
        ("hat", 1),
        ("concept", 1),
        ("very , very mysterious", 1),
        ("standing", 2),
        ("post", 2),
        ("night", 1),
        ("balls", 1),
        ("reflections", 1),
        ("context", 1),
        ("light", 1),
    ]

    assert list(graph3.nodes()) == expected_node_list3
    assert list(graph3.edges()) == expected_edges3
    assert list(graph3.degree) == expected_degree3

    text = open("demo_data/3138849-TAT10.txt", "r")
    transcript = text.read()
    text.close()
    graph4 = speech_graph(transcript)

    expected_node_list4 = [
        "image",
        "pretty boring",
        "child",
        "home",
        "father",
        "bread",
        "wife",
        "time",
        "obviously",
        "it",
        "development",
        "women",
        "photo",
    ]
    expected_edges4 = [
        ("image", "pretty boring"),
        ("child", "home"),
        ("child", "bread"),
        ("father", "bread"),
        ("wife", "home"),
        ("wife", "bread"),
        ("time", "obviously"),
        ("it", "development"),
        ("it", "development"),
        ("it", "photo"),
        ("development", "women"),
        ("women", "time"),
    ]
    expected_degree4 = [
        ("image", 1),
        ("pretty boring", 1),
        ("child", 2),
        ("home", 2),
        ("father", 1),
        ("bread", 3),
        ("wife", 2),
        ("time", 2),
        ("obviously", 1),
        ("it", 3),
        ("development", 3),
        ("women", 2),
        ("photo", 1),
    ]

    assert list(graph4.nodes()) == expected_node_list4
    assert list(graph4.edges()) == expected_edges4
    assert list(graph4.degree) == expected_degree4
