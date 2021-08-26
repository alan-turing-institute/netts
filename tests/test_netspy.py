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
    graph2 = speech_graph(
        "There are two… There is a young girl and who and seems to be maid, sitting on a couch. The little girl seems to be upset, she’s looking away and she looks very dismissive. She has something on her hands which I’m not sure what it is exactly, seems like, like a baby doll or yes, something, something looks familiar, like a toy. And the maid seems to convince her of, of something, but her eyes are closed and her mouth is shut. Oh and it seems to… She seems to be holding the book, maybe so she’s reading, but and the girl is not interested at all"
    )
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
        "interested",
        "book",
        "something",
        "hands",
        "mouth",
        "young",
    ]
    assert list(graph2.nodes()) == expected_node_list
    assert list(graph1.nodes()) == expected_node_list
