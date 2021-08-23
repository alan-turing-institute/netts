# pylint: disable=C0114, C0116
from netspy import __version__
import netspy

def test_version() -> None:
    assert __version__ == "0.1.0"

def test_speech_graph():
    text=open('demo_data/3138838-TAT10.txt','r')
    transcript=text.read()
    text.close()
    graph=netspy.speech_graph(transcript)
    print(type(graph))