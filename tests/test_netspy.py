# pylint: disable=C0114, C0116

from netspy import __version__
from netspy.speech_graph import plot_graph, speech_graph
from typing import Dict, Any

def test_version() -> None:
    assert __version__ == "0.1.0"


def test_speech_graph() -> None:
    #text = open("demo_data/3138838-TAT10.txt", "r")
    #transcript = text.read()
    #text.close()
    with open("demo_data/3138838-TAT10.txt", "r") as f:
        transcript = f.read()
    graph1 = speech_graph(transcript)
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

    #text2 = open("demo_data/3138838-TAT13.txt", "r")
    #transcript2 = text2.read()
    #text2.close()
    with open("demo_data/3138838-TAT13.txt", "r") as f:
        transcript = f.read()
    graph2 = speech_graph(transcript)
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

    #text = open("demo_data/3138838-TAT30.txt", "r")
    #transcript = text.read()
    #text.close()
    with open("demo_data/3138838-TAT30.txt", "r") as f:
        transcript = f.read()
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

    #text = open("demo_data/3138849-TAT10.txt", "r")
    #transcript = text.read()
    #text.close()
    with open("demo_data/3138849-TAT10.txt", "r") as f:
        transcript = f.read()
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

    expected_dict_graph4 = {
        "transcript": "This image is pretty boring. Kind of represents, um, olden times when wife and the child … When the wife and the child would just stay at home whilst the father is the bread earner. Um, it’s quite a sad photo but also in lighting because of the way that women have grown since this time and it has been able to portray development of women through time, which is obviously very good.\n",
        "sentences": 3,
        "tokens": 71,
        "unconnected_nodes": ["lighting", "way", "woman"],
    }

    expected_dict_node4: Dict[str, Dict[Any, Any]] = {
        "image": {},
        "pretty boring": {},
        "child": {},
        "home": {},
        "father": {},
        "bread": {},
        "wife": {},
        "time": {},
        "obviously": {},
        "it": {},
        "development": {},
        "women": {},
        "photo": {},
    }

    expected_dict_adj4 = {
        "image": {
            "pretty boring": {
                0: {
                    "relation": "is",
                    "confidence": 0.8132903905488816,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 0,
                    "node2_args": [],
                }
            }
        },
        "pretty boring": {},
        "child": {
            "home": {
                0: {
                    "relation": "would stay",
                    "confidence": 0.858772576540734,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            },
            "bread": {
                0: {
                    "relation": "is",
                    "confidence": 0.9728040566432826,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            },
        },
        "home": {},
        "father": {
            "bread": {
                0: {
                    "relation": "is",
                    "confidence": 0.9251282565798027,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            }
        },
        "bread": {},
        "wife": {
            "home": {
                0: {
                    "relation": "would stay",
                    "confidence": 0.858772576540734,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            },
            "bread": {
                0: {
                    "relation": "is",
                    "confidence": 0.9728040566432826,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            },
        },
        "time": {
            "obviously": {
                0: {
                    "relation": "is",
                    "confidence": 0.7697412098918558,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": ["very good"],
                }
            }
        },
        "obviously": {},
        "it": {
            "development": {
                0: {
                    "relation": "to portray",
                    "confidence": 0.41051436014453063,
                    "context": None,
                    "negated": False,
                    "passive": False,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": ["through time"],
                },
                1: {
                    "relation": "has been",
                    "confidence": 0.45170382506656653,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": [],
                },
            },
            "photo": {
                0: {
                    "relation": "is",
                    "confidence": 0.5222094630377523,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": ["because of the way"],
                }
            },
        },
        "development": {
            "women": {0: {"relation": "of", "extractor": "preposition", "sentence": 2}}
        },
        "women": {
            "time": {
                0: {
                    "relation": "have grown",
                    "confidence": 0.8942434158739456,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": [],
                }
            }
        },
        "photo": {},
    }

    expected_dict_pred4 = {
        "image": {},
        "pretty boring": {
            "image": {
                0: {
                    "relation": "is",
                    "confidence": 0.8132903905488816,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 0,
                    "node2_args": [],
                }
            }
        },
        "child": {},
        "home": {
            "child": {
                0: {
                    "relation": "would stay",
                    "confidence": 0.858772576540734,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            },
            "wife": {
                0: {
                    "relation": "would stay",
                    "confidence": 0.858772576540734,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            },
        },
        "father": {},
        "bread": {
            "father": {
                0: {
                    "relation": "is",
                    "confidence": 0.9251282565798027,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            },
            "child": {
                0: {
                    "relation": "is",
                    "confidence": 0.9728040566432826,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            },
            "wife": {
                0: {
                    "relation": "is",
                    "confidence": 0.9728040566432826,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            },
        },
        "wife": {},
        "time": {
            "women": {
                0: {
                    "relation": "have grown",
                    "confidence": 0.8942434158739456,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": [],
                }
            }
        },
        "obviously": {
            "time": {
                0: {
                    "relation": "is",
                    "confidence": 0.7697412098918558,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": ["very good"],
                }
            }
        },
        "it": {},
        "development": {
            "it": {
                0: {
                    "relation": "to portray",
                    "confidence": 0.41051436014453063,
                    "context": None,
                    "negated": False,
                    "passive": False,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": ["through time"],
                },
                1: {
                    "relation": "has been",
                    "confidence": 0.45170382506656653,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": [],
                },
            }
        },
        "women": {
            "development": {
                0: {"relation": "of", "extractor": "preposition", "sentence": 2}
            }
        },
        "photo": {
            "it": {
                0: {
                    "relation": "is",
                    "confidence": 0.5222094630377523,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": ["because of the way"],
                }
            }
        },
    }

    expected_dict_succ4 = {
        "image": {
            "pretty boring": {
                0: {
                    "relation": "is",
                    "confidence": 0.8132903905488816,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 0,
                    "node2_args": [],
                }
            }
        },
        "pretty boring": {},
        "child": {
            "home": {
                0: {
                    "relation": "would stay",
                    "confidence": 0.858772576540734,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            },
            "bread": {
                0: {
                    "relation": "is",
                    "confidence": 0.9728040566432826,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            },
        },
        "home": {},
        "father": {
            "bread": {
                0: {
                    "relation": "is",
                    "confidence": 0.9251282565798027,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            }
        },
        "bread": {},
        "wife": {
            "home": {
                0: {
                    "relation": "would stay",
                    "confidence": 0.858772576540734,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            },
            "bread": {
                0: {
                    "relation": "is",
                    "confidence": 0.9728040566432826,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 1,
                    "node2_args": [],
                }
            },
        },
        "time": {
            "obviously": {
                0: {
                    "relation": "is",
                    "confidence": 0.7697412098918558,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": ["very good"],
                }
            }
        },
        "obviously": {},
        "it": {
            "development": {
                0: {
                    "relation": "to portray",
                    "confidence": 0.41051436014453063,
                    "context": None,
                    "negated": False,
                    "passive": False,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": ["through time"],
                },
                1: {
                    "relation": "has been",
                    "confidence": 0.45170382506656653,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": [],
                },
            },
            "photo": {
                0: {
                    "relation": "is",
                    "confidence": 0.5222094630377523,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": ["because of the way"],
                }
            },
        },
        "development": {
            "women": {0: {"relation": "of", "extractor": "preposition", "sentence": 2}}
        },
        "women": {
            "time": {
                0: {
                    "relation": "have grown",
                    "confidence": 0.8942434158739456,
                    "context": None,
                    "negated": False,
                    "passive": True,
                    "extractor": "ollie",
                    "sentence": 2,
                    "node2_args": [],
                }
            }
        },
        "photo": {},
    }
    assert list(graph4.nodes()) == expected_node_list4
    assert list(graph4.edges()) == expected_edges4
    assert list(graph4.degree) == expected_degree4

    graph4_dict = graph4.__dict__

    assert graph4_dict.get("graph") == expected_dict_graph4
    assert graph4_dict.get("_node") == expected_dict_node4
    assert graph4_dict.get("_adj") == expected_dict_adj4
    assert graph4_dict.get("_pred") == expected_dict_pred4
    assert graph4_dict.get("_succ") == expected_dict_succ4
