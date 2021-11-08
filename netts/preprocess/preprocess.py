"""Preprocess transcripts"""

import re
from typing import Dict, List

import nltk


def replace_problematic_characters(text: str, character_map: Dict[str, str]) -> str:
    """Replace characters in a string

    Args:
        text: String to replace characters in
        character_map: A dictionary where the key is the character to replace and the value is the new value

    Returns:
        String with problematic characters replaced
    """

    for symbol in character_map.keys():
        text = text.replace(symbol, character_map[symbol])

    return text


def expand_contractions(text: str, contraction_map: Dict[str, str]) -> str:

    map_keys = list(contraction_map.keys())

    # Sort keys by length in descending order
    map_keys.sort(key=len, reverse=True)

    return re.sub(
        f"({'|'.join(map_keys)})", lambda x: contraction_map[x.group(0)], text
    )


def remove_interjections(
    text: str, interjections: List[str], contraction_map: Dict[str, str]
) -> str:
    """Remove interjections and contractions

    Args:
        text: Text to remove interjections from
        interjections: List of interjections to remove

    Returns:
        text with intejections removed
    """

    text_no_contractions = expand_contractions(text, contraction_map)
    tokens = nltk.word_tokenize(text_no_contractions)
    tokens_no_interjections = [w for w in tokens if w not in interjections]

    # ToDo: This places spaces between tokens, which may have not existed before
    return " ".join(tokens_no_interjections)


# ToDO: Refactor this and figure out exactly what functionality is required
def remove_irrelevant_text(text: str, be_quiet: bool = True) -> str:
    #
    # ---- Remove double-bracketed speech ----
    # Some transcribers marked irrelevant speech by putting it between double brackets.
    # Remove Anything between two (()), specifically between "( (" and ") )",
    #  since initial cleaning steps put a single whitespace between punctuation symbols
    match = re.match(r"^.*\(\s\((.*)\)\s\).*$", text)
    if match:
        if not be_quiet:
            print(match.group(1))
        match_text = "( (" + match.group(1) + ") )"
        text = text.replace(match_text, "")
    #
    #
    # ---- Remove speaker stamp ('Unknown Speaker  0:01')----
    speakerstamp = re.findall(r"\bUnknown Speaker\b\s\d{1}:\d{2}", text)
    if speakerstamp != []:
        for stamp in speakerstamp:
            if not be_quiet:
                print(stamp)
            text = text.replace(stamp, "")
    #
    # ---- Remove time stamp ('00:01:00')----
    timestamp = re.findall(r"[0-9]{2}:[0-9]{2}:[0-9]{2}", text)
    if timestamp != []:
        for stamp in timestamp:
            if not be_quiet:
                print(stamp)
            text = text.replace(stamp, "")
    #
    #
    # ---- Remove other irrelevant text ----
    # For all other irrelevant text, I searched for specific words in the transcriptions ("recording", "prolific", "describe")
    # and copied the irrelevant speech excerpts manually.
    irrelevant_text = [
        "Please describe what you see in the image . Please speak for a full minute . We are recording .",
        "Okay, this is where we see this bits please speak to the for full minute that we are recording .",
        "Please describe what you see in this image . Please speak for the full minute . We are recording .",
        "Okay please describe for what you see in this image please speak for the full minute we are recording .",
        "Okay, please describe what you see this image, please . Please speak for the four minute we are recording . ",
        "Please describe what you in this image, please speak for four minutes . We are recording . ",
        "Please describe a scene that is pleased to be recording . ",
        "we are recording . ",
        "Studies available on prolific... ",
        "[ ]",
        "[ ? ]",
        "( unclear )",
        "( unclear . )",
        "Transcribed by https : //otter.ai",
    ]
    #
    for irr in irrelevant_text:
        if irr in text and not be_quiet:
            # print('Removing "{0}" from \n"{1}"'.format(irr, text))
            print(f'Removing "{irr}"')
        text = text.replace(irr, "")
    return text
