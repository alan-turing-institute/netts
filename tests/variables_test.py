# pylint: disable=C0301, C0302
from typing import Any, Dict

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
expected_dict_graph1 = {
    "transcript": "There are two… There is a young girl and who and seems to be maid, sitting on a couch. The little girl seems to be upset, she’s looking away and she looks very dismissive. She has something on her hands which I’m not sure what it is exactly, seems like, like a baby doll or yes, something, something looks familiar, like a toy. And the maid seems to convince her of, of something, but her eyes are closed and her mouth is shut. Oh and it seems to… She seems to be holding the book, maybe so she’s reading, but and the girl is not interested at all.\n",  # noqa: E501
    "sentences": 5,
    "tokens": 112,
    "unconnected_nodes": ["couch", "baby", "doll", "toy"],
}
expected_dict_node1: Dict[Any, Any] = {
    "girl": {},
    "maid": {},
    "very dismissive": {},
    "away": {},
    "upset": {},
    "it": {},
    "exactly": {},
    "i": {},
    "eyes": {},
    "closed": {},
    "interested at all": {},
    "book": {},
    "something": {},
    "hands": {},
    "mouth": {},
    "young": {},
}
expected_dict_adj1 = {
    "girl": {
        "maid": {
            0: {
                "relation": "to be",
                "confidence": 0.896604430840561,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": ["sitting on a couch"],
            }
        },
        "very dismissive": {
            0: {
                "relation": "looks",
                "confidence": 0.22506131975927415,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        },
        "away": {
            0: {
                "relation": "is looking",
                "confidence": 0.22506131975927415,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        },
        "upset": {
            0: {
                "relation": "to be",
                "confidence": 0.7535117993595638,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        },
        "it": {
            0: {
                "relation": "has",
                "confidence": 0.4875515567406569,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        },
        "interested at all": {
            0: {
                "relation": "is not",
                "confidence": 0.7665350501724939,
                "context": None,
                "negated": True,
                "passive": True,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
        "book": {
            0: {
                "relation": "to be holding",
                "confidence": 0.41051436014453063,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
        "girl": {
            0: {
                "relation": "to be holding",
                "confidence": 0.2743125465364158,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
        "young": {0: {"relation": "(is)", "extractor": "adjective", "sentence": 0}},
    },
    "maid": {
        "girl": {
            0: {
                "relation": "to convince",
                "confidence": 0.8103687806061152,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": ["of"],
            }
        }
    },
    "very dismissive": {},
    "away": {},
    "upset": {},
    "it": {
        "exactly": {
            0: {
                "relation": "is",
                "confidence": 0.27813615858960106,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        }
    },
    "exactly": {},
    "i": {
        "it": {
            0: {
                "relation": "am not",
                "confidence": 0.30899953469486874,
                "context": None,
                "negated": True,
                "passive": True,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        }
    },
    "eyes": {
        "closed": {
            0: {
                "relation": "are",
                "confidence": 0.3833177039030785,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": [],
            }
        },
        "girl": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 3}
        },
    },
    "closed": {},
    "interested at all": {},
    "book": {
        "girl": {
            0: {
                "relation": "is reading",
                "confidence": 0.8841701665203853,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        }
    },
    "something": {
        "hands": {0: {"relation": "on", "extractor": "preposition", "sentence": 2}}
    },
    "hands": {
        "girl": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 2}
        }
    },
    "mouth": {
        "girl": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 3}
        }
    },
    "young": {},
}
expected_dict_pred1 = {
    "girl": {
        "maid": {
            0: {
                "relation": "to convince",
                "confidence": 0.8103687806061152,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": ["of"],
            }
        },
        "book": {
            0: {
                "relation": "is reading",
                "confidence": 0.8841701665203853,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
        "girl": {
            0: {
                "relation": "to be holding",
                "confidence": 0.2743125465364158,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
        "hands": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 2}
        },
        "eyes": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 3}
        },
        "mouth": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 3}
        },
    },
    "maid": {
        "girl": {
            0: {
                "relation": "to be",
                "confidence": 0.896604430840561,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": ["sitting on a couch"],
            }
        }
    },
    "very dismissive": {
        "girl": {
            0: {
                "relation": "looks",
                "confidence": 0.22506131975927415,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        }
    },
    "away": {
        "girl": {
            0: {
                "relation": "is looking",
                "confidence": 0.22506131975927415,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        }
    },
    "upset": {
        "girl": {
            0: {
                "relation": "to be",
                "confidence": 0.7535117993595638,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        }
    },
    "it": {
        "i": {
            0: {
                "relation": "am not",
                "confidence": 0.30899953469486874,
                "context": None,
                "negated": True,
                "passive": True,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        },
        "girl": {
            0: {
                "relation": "has",
                "confidence": 0.4875515567406569,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        },
    },
    "exactly": {
        "it": {
            0: {
                "relation": "is",
                "confidence": 0.27813615858960106,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        }
    },
    "i": {},
    "eyes": {},
    "closed": {
        "eyes": {
            0: {
                "relation": "are",
                "confidence": 0.3833177039030785,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": [],
            }
        }
    },
    "interested at all": {
        "girl": {
            0: {
                "relation": "is not",
                "confidence": 0.7665350501724939,
                "context": None,
                "negated": True,
                "passive": True,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        }
    },
    "book": {
        "girl": {
            0: {
                "relation": "to be holding",
                "confidence": 0.41051436014453063,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        }
    },
    "something": {},
    "hands": {
        "something": {0: {"relation": "on", "extractor": "preposition", "sentence": 2}}
    },
    "mouth": {},
    "young": {
        "girl": {0: {"relation": "(is)", "extractor": "adjective", "sentence": 0}}
    },
}
expected_dict_succ1 = {
    "girl": {
        "maid": {
            0: {
                "relation": "to be",
                "confidence": 0.896604430840561,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": ["sitting on a couch"],
            }
        },
        "very dismissive": {
            0: {
                "relation": "looks",
                "confidence": 0.22506131975927415,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        },
        "away": {
            0: {
                "relation": "is looking",
                "confidence": 0.22506131975927415,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        },
        "upset": {
            0: {
                "relation": "to be",
                "confidence": 0.7535117993595638,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        },
        "it": {
            0: {
                "relation": "has",
                "confidence": 0.4875515567406569,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        },
        "interested at all": {
            0: {
                "relation": "is not",
                "confidence": 0.7665350501724939,
                "context": None,
                "negated": True,
                "passive": True,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
        "book": {
            0: {
                "relation": "to be holding",
                "confidence": 0.41051436014453063,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
        "girl": {
            0: {
                "relation": "to be holding",
                "confidence": 0.2743125465364158,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
        "young": {0: {"relation": "(is)", "extractor": "adjective", "sentence": 0}},
    },
    "maid": {
        "girl": {
            0: {
                "relation": "to convince",
                "confidence": 0.8103687806061152,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": ["of"],
            }
        }
    },
    "very dismissive": {},
    "away": {},
    "upset": {},
    "it": {
        "exactly": {
            0: {
                "relation": "is",
                "confidence": 0.27813615858960106,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        }
    },
    "exactly": {},
    "i": {
        "it": {
            0: {
                "relation": "am not",
                "confidence": 0.30899953469486874,
                "context": None,
                "negated": True,
                "passive": True,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        }
    },
    "eyes": {
        "closed": {
            0: {
                "relation": "are",
                "confidence": 0.3833177039030785,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": [],
            }
        },
        "girl": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 3}
        },
    },
    "closed": {},
    "interested at all": {},
    "book": {
        "girl": {
            0: {
                "relation": "is reading",
                "confidence": 0.8841701665203853,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        }
    },
    "something": {
        "hands": {0: {"relation": "on", "extractor": "preposition", "sentence": 2}}
    },
    "hands": {
        "girl": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 2}
        }
    },
    "mouth": {
        "girl": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 3}
        }
    },
    "young": {},
}
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
expected_dict_graph2 = {
    "transcript": "Well, on the picture I see four men lying on the field, they seem to be some sort of workers and they seem to be tired and presumably, maybe it’s during midday, because their hats are covering their heads. One of the men seems to be standing up, who doesn’t have a hat on and he’s leaning towards the other three men that are lying on the floor. They seem to be tired, one of the men has… Seems to be in pain.\nAnd the, the…I cannot see this, the face of the third person, but another man is lying next to him, resting, so probably he is asleep or very tired as well. And the fourth man is lying towards all of them.\n",  # noqa: E501
    "sentences": 5,
    "tokens": 129,
    "unconnected_nodes": [],
}
expected_dict_node2: Dict[Any, Any] = {
    "it": {},
    "midday": {},
    "hats": {},
    "heads": {},
    "the men": {},
    "presumably": {},
    "tired": {},
    "i": {},
    "sort": {},
    "picture": {},
    "floor": {},
    "one of the men": {},
    "pain": {},
    "he": {},
    "asleep or very tired": {},
    "man": {},
    "this": {},
    "one": {},
    "men": {},
    "face": {},
    "person": {},
    "all": {},
}
expected_dict_adj2 = {
    "it": {
        "midday": {
            0: {
                "relation": "is",
                "confidence": 0.3135276058215937,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": ["because their hats are covering their heads"],
            }
        }
    },
    "midday": {},
    "hats": {
        "heads": {
            0: {
                "relation": "are covering",
                "confidence": 0.48903187625367955,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "the men": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 0}
        },
    },
    "heads": {
        "the men": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 0}
        }
    },
    "the men": {
        "presumably": {
            0: {
                "relation": "to be",
                "confidence": 0.3229663126973359,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "tired": {
            0: {
                "relation": "to be",
                "confidence": 0.3229663126973359,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "the men": {
            0: {
                "relation": "lying",
                "confidence": 0.8817598924294554,
                "context": "I see",
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "sort": {
            0: {
                "relation": "to be",
                "confidence": 0.5750411108691293,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "picture": {
            0: {
                "relation": "seem",
                "confidence": 0.7044291000807404,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "floor": {
            0: {
                "relation": "are lying",
                "confidence": 0.9052256377408016,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        },
    },
    "presumably": {},
    "tired": {},
    "i": {
        "the men": {
            0: {
                "relation": "see",
                "confidence": 0.39746064682094406,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "this": {
            0: {
                "relation": "can not see",
                "confidence": 0.22506131975927415,
                "context": None,
                "negated": True,
                "passive": False,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": [],
            }
        },
    },
    "sort": {},
    "picture": {},
    "floor": {},
    "one of the men": {
        "pain": {
            0: {
                "relation": "to be",
                "confidence": 0.9052256377408016,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        }
    },
    "pain": {},
    "he": {
        "asleep or very tired": {
            0: {
                "relation": "is",
                "confidence": 0.27813615858960106,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": ["as well"],
            }
        }
    },
    "asleep or very tired": {},
    "man": {
        "he": {
            0: {
                "relation": "is lying",
                "confidence": 0.8348583869532935,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": ["resting , so"],
            }
        },
        "the men": {
            0: {
                "relation": "is lying",
                "confidence": 0.8477538091726738,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
    },
    "this": {},
    "one": {
        "the men": {0: {"relation": "of", "extractor": "preposition", "sentence": 1}},
        "men": {0: {"relation": "of", "extractor": "preposition", "sentence": 2}},
    },
    "men": {},
    "face": {
        "person": {0: {"relation": "of", "extractor": "preposition", "sentence": 3}}
    },
    "person": {},
    "all": {
        "the men": {0: {"relation": "of", "extractor": "preposition", "sentence": 4}}
    },
}
expected_dict_pred2 = {
    "it": {},
    "midday": {
        "it": {
            0: {
                "relation": "is",
                "confidence": 0.3135276058215937,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": ["because their hats are covering their heads"],
            }
        }
    },
    "hats": {},
    "heads": {
        "hats": {
            0: {
                "relation": "are covering",
                "confidence": 0.48903187625367955,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        }
    },
    "the men": {
        "the men": {
            0: {
                "relation": "lying",
                "confidence": 0.8817598924294554,
                "context": "I see",
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "i": {
            0: {
                "relation": "see",
                "confidence": 0.39746064682094406,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "man": {
            0: {
                "relation": "is lying",
                "confidence": 0.8477538091726738,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
        "hats": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 0}
        },
        "heads": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 0}
        },
        "one": {0: {"relation": "of", "extractor": "preposition", "sentence": 1}},
        "all": {0: {"relation": "of", "extractor": "preposition", "sentence": 4}},
    },
    "presumably": {
        "the men": {
            0: {
                "relation": "to be",
                "confidence": 0.3229663126973359,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        }
    },
    "tired": {
        "the men": {
            0: {
                "relation": "to be",
                "confidence": 0.3229663126973359,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        }
    },
    "i": {},
    "sort": {
        "the men": {
            0: {
                "relation": "to be",
                "confidence": 0.5750411108691293,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        }
    },
    "picture": {
        "the men": {
            0: {
                "relation": "seem",
                "confidence": 0.7044291000807404,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        }
    },
    "floor": {
        "the men": {
            0: {
                "relation": "are lying",
                "confidence": 0.9052256377408016,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        }
    },
    "one of the men": {},
    "pain": {
        "one of the men": {
            0: {
                "relation": "to be",
                "confidence": 0.9052256377408016,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        }
    },
    "he": {
        "man": {
            0: {
                "relation": "is lying",
                "confidence": 0.8348583869532935,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": ["resting , so"],
            }
        }
    },
    "asleep or very tired": {
        "he": {
            0: {
                "relation": "is",
                "confidence": 0.27813615858960106,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": ["as well"],
            }
        }
    },
    "man": {},
    "this": {
        "i": {
            0: {
                "relation": "can not see",
                "confidence": 0.22506131975927415,
                "context": None,
                "negated": True,
                "passive": False,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": [],
            }
        }
    },
    "one": {},
    "men": {"one": {0: {"relation": "of", "extractor": "preposition", "sentence": 2}}},
    "face": {},
    "person": {
        "face": {0: {"relation": "of", "extractor": "preposition", "sentence": 3}}
    },
    "all": {},
}
expected_dict_succ2 = {
    "it": {
        "midday": {
            0: {
                "relation": "is",
                "confidence": 0.3135276058215937,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": ["because their hats are covering their heads"],
            }
        }
    },
    "midday": {},
    "hats": {
        "heads": {
            0: {
                "relation": "are covering",
                "confidence": 0.48903187625367955,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "the men": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 0}
        },
    },
    "heads": {
        "the men": {
            0: {"relation": "(of) [poss]", "extractor": "possession", "sentence": 0}
        }
    },
    "the men": {
        "presumably": {
            0: {
                "relation": "to be",
                "confidence": 0.3229663126973359,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "tired": {
            0: {
                "relation": "to be",
                "confidence": 0.3229663126973359,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "the men": {
            0: {
                "relation": "lying",
                "confidence": 0.8817598924294554,
                "context": "I see",
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "sort": {
            0: {
                "relation": "to be",
                "confidence": 0.5750411108691293,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "picture": {
            0: {
                "relation": "seem",
                "confidence": 0.7044291000807404,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "floor": {
            0: {
                "relation": "are lying",
                "confidence": 0.9052256377408016,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        },
    },
    "presumably": {},
    "tired": {},
    "i": {
        "the men": {
            0: {
                "relation": "see",
                "confidence": 0.39746064682094406,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "this": {
            0: {
                "relation": "can not see",
                "confidence": 0.22506131975927415,
                "context": None,
                "negated": True,
                "passive": False,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": [],
            }
        },
    },
    "sort": {},
    "picture": {},
    "floor": {},
    "one of the men": {
        "pain": {
            0: {
                "relation": "to be",
                "confidence": 0.9052256377408016,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        }
    },
    "pain": {},
    "he": {
        "asleep or very tired": {
            0: {
                "relation": "is",
                "confidence": 0.27813615858960106,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": ["as well"],
            }
        }
    },
    "asleep or very tired": {},
    "man": {
        "he": {
            0: {
                "relation": "is lying",
                "confidence": 0.8348583869532935,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": ["resting , so"],
            }
        },
        "the men": {
            0: {
                "relation": "is lying",
                "confidence": 0.8477538091726738,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
    },
    "this": {},
    "one": {
        "the men": {0: {"relation": "of", "extractor": "preposition", "sentence": 1}},
        "men": {0: {"relation": "of", "extractor": "preposition", "sentence": 2}},
    },
    "men": {},
    "face": {
        "person": {0: {"relation": "of", "extractor": "preposition", "sentence": 3}}
    },
    "person": {},
    "all": {
        "the men": {0: {"relation": "of", "extractor": "preposition", "sentence": 4}}
    },
}
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
expected_dict_graph3 = {
    "transcript": "I see a man in the dark standing against a light post. It seems to be in the middle of the night; I think because the lightbulb is working. On the picture there seems to be like a park and... Or trees but in those trees there are little balls of light reflections as well. I cannot see the… Anything else because it’s very dark. But the man on the picture seems to wear a hat and, and has a jacket on and he seems to have a hoodie on as well. The picture is very, very mysterious, which I like about it, but for me I would like to understand more concept, context of the picture.\n",  # noqa: E501
    "sentences": 6,
    "tokens": 119,
    "unconnected_nodes": ["park", "tree"],
}
expected_dict_node3: Dict[Any, Any] = {
    "i": {},
    "man": {},
    "lightbulb": {},
    "it": {},
    "middle": {},
    "there": {},
    "picture": {},
    "dark": {},
    "anything": {},
    "hoodie": {},
    "jacket": {},
    "hat": {},
    "concept": {},
    "very , very mysterious": {},
    "standing": {},
    "post": {},
    "night": {},
    "balls": {},
    "reflections": {},
    "context": {},
    "light": {},
}
expected_dict_adj3 = {
    "i": {
        "man": {
            0: {
                "relation": "see",
                "confidence": 0.5691839633287576,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "lightbulb": {
            0: {
                "relation": "think",
                "confidence": 0.4667063855863067,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        },
        "anything": {
            0: {
                "relation": "can not see",
                "confidence": 0.30899953469486874,
                "context": None,
                "negated": True,
                "passive": False,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": ["because it is very dark"],
            }
        },
        "concept": {
            0: {
                "relation": "would like to understand",
                "confidence": 0.3880890333449538,
                "context": "I would like",
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 5,
                "node2_args": [],
            }
        },
        "picture": {
            0: {
                "relation": "like",
                "confidence": 0.30899953469486874,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 5,
                "node2_args": [],
            }
        },
    },
    "man": {
        "hoodie": {
            0: {
                "relation": "to have",
                "confidence": 0.41051436014453063,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": ["as well"],
            }
        },
        "jacket": {
            0: {
                "relation": "has on",
                "confidence": 0.9005286127300474,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
        "hat": {
            0: {
                "relation": "to wear",
                "confidence": 0.913197594301744,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
        "picture": {0: {"relation": "on", "extractor": "preposition", "sentence": 4}},
        "standing": {0: {"relation": "in", "extractor": "preposition", "sentence": 0}},
        "post": {0: {"relation": "against", "extractor": "preposition", "sentence": 0}},
    },
    "lightbulb": {},
    "it": {
        "middle": {
            0: {
                "relation": "to be",
                "confidence": 0.41051436014453063,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        },
        "dark": {
            0: {
                "relation": "is",
                "confidence": 0.27813615858960106,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": [],
            }
        },
    },
    "middle": {
        "night": {0: {"relation": "of", "extractor": "preposition", "sentence": 1}}
    },
    "there": {
        "picture": {
            0: {
                "relation": "seems",
                "confidence": 0.25194713813498654,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        }
    },
    "picture": {
        "very , very mysterious": {
            0: {
                "relation": "is",
                "confidence": 0.8132903905488816,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 5,
                "node2_args": [],
            }
        }
    },
    "dark": {},
    "anything": {},
    "hoodie": {},
    "jacket": {},
    "hat": {},
    "concept": {},
    "very , very mysterious": {},
    "standing": {
        "dark": {0: {"relation": "(is)", "extractor": "adjective", "sentence": 0}}
    },
    "post": {
        "light": {0: {"relation": "(is)", "extractor": "adjective", "sentence": 0}}
    },
    "night": {},
    "balls": {
        "reflections": {
            0: {"relation": "of", "extractor": "preposition", "sentence": 2}
        }
    },
    "reflections": {},
    "context": {
        "picture": {0: {"relation": "of", "extractor": "preposition", "sentence": 5}}
    },
    "light": {},
}
expected_dict_pred3 = {
    "i": {},
    "man": {
        "i": {
            0: {
                "relation": "see",
                "confidence": 0.5691839633287576,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        }
    },
    "lightbulb": {
        "i": {
            0: {
                "relation": "think",
                "confidence": 0.4667063855863067,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        }
    },
    "it": {},
    "middle": {
        "it": {
            0: {
                "relation": "to be",
                "confidence": 0.41051436014453063,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        }
    },
    "there": {},
    "picture": {
        "there": {
            0: {
                "relation": "seems",
                "confidence": 0.25194713813498654,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        },
        "i": {
            0: {
                "relation": "like",
                "confidence": 0.30899953469486874,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 5,
                "node2_args": [],
            }
        },
        "man": {0: {"relation": "on", "extractor": "preposition", "sentence": 4}},
        "context": {0: {"relation": "of", "extractor": "preposition", "sentence": 5}},
    },
    "dark": {
        "it": {
            0: {
                "relation": "is",
                "confidence": 0.27813615858960106,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": [],
            }
        },
        "standing": {0: {"relation": "(is)", "extractor": "adjective", "sentence": 0}},
    },
    "anything": {
        "i": {
            0: {
                "relation": "can not see",
                "confidence": 0.30899953469486874,
                "context": None,
                "negated": True,
                "passive": False,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": ["because it is very dark"],
            }
        }
    },
    "hoodie": {
        "man": {
            0: {
                "relation": "to have",
                "confidence": 0.41051436014453063,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": ["as well"],
            }
        }
    },
    "jacket": {
        "man": {
            0: {
                "relation": "has on",
                "confidence": 0.9005286127300474,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        }
    },
    "hat": {
        "man": {
            0: {
                "relation": "to wear",
                "confidence": 0.913197594301744,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        }
    },
    "concept": {
        "i": {
            0: {
                "relation": "would like to understand",
                "confidence": 0.3880890333449538,
                "context": "I would like",
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 5,
                "node2_args": [],
            }
        }
    },
    "very , very mysterious": {
        "picture": {
            0: {
                "relation": "is",
                "confidence": 0.8132903905488816,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 5,
                "node2_args": [],
            }
        }
    },
    "standing": {
        "man": {0: {"relation": "in", "extractor": "preposition", "sentence": 0}}
    },
    "post": {
        "man": {0: {"relation": "against", "extractor": "preposition", "sentence": 0}}
    },
    "night": {
        "middle": {0: {"relation": "of", "extractor": "preposition", "sentence": 1}}
    },
    "balls": {},
    "reflections": {
        "balls": {0: {"relation": "of", "extractor": "preposition", "sentence": 2}}
    },
    "context": {},
    "light": {
        "post": {0: {"relation": "(is)", "extractor": "adjective", "sentence": 0}}
    },
}
expected_dict_succ3 = {
    "i": {
        "man": {
            0: {
                "relation": "see",
                "confidence": 0.5691839633287576,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 0,
                "node2_args": [],
            }
        },
        "lightbulb": {
            0: {
                "relation": "think",
                "confidence": 0.4667063855863067,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        },
        "anything": {
            0: {
                "relation": "can not see",
                "confidence": 0.30899953469486874,
                "context": None,
                "negated": True,
                "passive": False,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": ["because it is very dark"],
            }
        },
        "concept": {
            0: {
                "relation": "would like to understand",
                "confidence": 0.3880890333449538,
                "context": "I would like",
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 5,
                "node2_args": [],
            }
        },
        "picture": {
            0: {
                "relation": "like",
                "confidence": 0.30899953469486874,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 5,
                "node2_args": [],
            }
        },
    },
    "man": {
        "hoodie": {
            0: {
                "relation": "to have",
                "confidence": 0.41051436014453063,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": ["as well"],
            }
        },
        "jacket": {
            0: {
                "relation": "has on",
                "confidence": 0.9005286127300474,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
        "hat": {
            0: {
                "relation": "to wear",
                "confidence": 0.913197594301744,
                "context": None,
                "negated": False,
                "passive": False,
                "extractor": "ollie",
                "sentence": 4,
                "node2_args": [],
            }
        },
        "picture": {0: {"relation": "on", "extractor": "preposition", "sentence": 4}},
        "standing": {0: {"relation": "in", "extractor": "preposition", "sentence": 0}},
        "post": {0: {"relation": "against", "extractor": "preposition", "sentence": 0}},
    },
    "lightbulb": {},
    "it": {
        "middle": {
            0: {
                "relation": "to be",
                "confidence": 0.41051436014453063,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 1,
                "node2_args": [],
            }
        },
        "dark": {
            0: {
                "relation": "is",
                "confidence": 0.27813615858960106,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 3,
                "node2_args": [],
            }
        },
    },
    "middle": {
        "night": {0: {"relation": "of", "extractor": "preposition", "sentence": 1}}
    },
    "there": {
        "picture": {
            0: {
                "relation": "seems",
                "confidence": 0.25194713813498654,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 2,
                "node2_args": [],
            }
        }
    },
    "picture": {
        "very , very mysterious": {
            0: {
                "relation": "is",
                "confidence": 0.8132903905488816,
                "context": None,
                "negated": False,
                "passive": True,
                "extractor": "ollie",
                "sentence": 5,
                "node2_args": [],
            }
        }
    },
    "dark": {},
    "anything": {},
    "hoodie": {},
    "jacket": {},
    "hat": {},
    "concept": {},
    "very , very mysterious": {},
    "standing": {
        "dark": {0: {"relation": "(is)", "extractor": "adjective", "sentence": 0}}
    },
    "post": {
        "light": {0: {"relation": "(is)", "extractor": "adjective", "sentence": 0}}
    },
    "night": {},
    "balls": {
        "reflections": {
            0: {"relation": "of", "extractor": "preposition", "sentence": 2}
        }
    },
    "reflections": {},
    "context": {
        "picture": {0: {"relation": "of", "extractor": "preposition", "sentence": 5}}
    },
    "light": {},
}
expected_dict_graph4 = {
    "transcript": "This image is pretty boring. Kind of represents, um, olden times when wife and the child … When the wife and the child would just stay at home whilst the father is the bread earner. Um, it’s quite a sad photo but also in lighting because of the way that women have grown since this time and it has been able to portray development of women through time, which is obviously very good.\n",  # noqa: E501
    "sentences": 3,
    "tokens": 71,
    "unconnected_nodes": ["lighting", "way", "woman"],
}
expected_dict_node4: Dict[Any, Any] = {
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
