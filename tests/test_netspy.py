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
    expected_node_list = [
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
    assert list(graph1.nodes()) == expected_node_list

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
    assert list(graph2.nodes()) == expected_node_list2
