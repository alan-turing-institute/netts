"""Preprocess transcripts"""

import re
from typing import Dict

def replace_problematic_characters(text: str, character_map: Dict[str, str]) -> str:
    """Replace characters in a string

    Args:
        text (str): String to replace characters in
        character_map (Dict[str, str]): A dictionary where the key is the character to replace and the value is the new value

    Returns:
        str: String with problematic characters replaced
    """

    for symbol in character_map.keys():
        text = text.replace(symbol, character_map[symbol])
    
    return text

# def expand_contractions(text: str, contraction_mapping=CONTRACTION_MAP):
#     contractions_pattern = re.compile(
#         "({})".format("|".join(contraction_mapping.keys())),
#         flags=re.IGNORECASE | re.DOTALL,
#     )

#     def expand_match(contraction):
#         match = contraction.group(0)
#         first_char = match[0]
#         expanded_contraction = (
#             contraction_mapping.get(match)
#             if contraction_mapping.get(match)
#             else contraction_mapping.get(match.lower())
#         )
#         expanded_contraction = first_char + expanded_contraction[1:]
#         return expanded_contraction

#     expanded_text = contractions_pattern.sub(expand_match, text)
#     expanded_text = re.sub("'", "", expanded_text)
#     return expanded_text


# def remove_interjections(text):
#     """
#     @author: by Dr. Caro Nettekoven, 2020
#     Note: The interjections removed by this funciton are specific for English. Applying this to other languages may cause problems (For example in German "um" is a presposition)
#     """
#     english_interjections = [
#         "Um",
#         "um",
#         "Uh",
#         "uh",
#         "Eh",
#         "eh",
#         "Ehm",
#         "Em",
#         "em",
#         "Erm",
#         "erm",
#         "Ehhm",
#         "ehhm",
#         "Ehm",
#         "ehm",
#         "Mmm",
#         "mmm",
#         "Yeah",
#         "yeah",
#         "ah",
#         "Ah",
#         "Aah",
#         "aah",
#         "hmm",
#         "hmmm",
#         "Hmm",
#         "Hmmm",
#         "inaudible",
#         "Inaudible",
#     ]
#     #
#     sent2 = expand_contractions(text)  # expand contractions
#     tokens = nltk.word_tokenize(sent2)
#     # remove interjections
#     tokens = [w for w in tokens if not w in english_interjections]
#     sent3 = " ".join(tokens)
#     return sent3

# def remove_irrelevant_text(text, be_quiet=True):
#     """
#     @author: by Dr. Caro Nettekoven, 2021

#     Removes irrelevant text from the transcript.
#     Irrelevant text was either added by the transcription program (example: 'Transcribed by https://otter.ai')
#     or by the transcriber (examples: '[ ]', '[ ? ]', '( unclear )')
#     or was genuine speech but recording of the participants reading out instructions (example:  'Please describe a scene that is pleased to be recording', 'we are recording').
#     Since the last class of irrelevant speech can vary, I made a list of frequent read out instructions occurring in the dataset. These will have to be ammended for other task instructions.

#     """
#     #
#     # ---- Remove double-bracketed speech ----
#     # Some transcribers marked irrelevant speech by putting it between double brackets.
#     # Remove Anything between two (()), specifically between "( (" and ") )", since initial cleaning steps put a single whitespace between punctuation symbols
#     match = re.match(r"^.*\(\s\((.*)\)\s\).*$", text)
#     if match:
#         if not be_quiet:
#             print(match.group(1))
#         match_text = "( (" + match.group(1) + ") )"
#         text = text.replace(match_text, "")
#     #
#     #
#     # ---- Remove speaker stamp ('Unknown Speaker  0:01')----
#     speakerstamp = re.findall(r"\bUnknown Speaker\b\s\d{1}:\d{2}", text)
#     if speakerstamp != []:
#         for stamp in speakerstamp:
#             if not be_quiet:
#                 print(stamp)
#             text = text.replace(stamp, "")
#     #
#     # ---- Remove time stamp ('00:01:00')----
#     timestamp = re.findall(r"[0-9]{2}:[0-9]{2}:[0-9]{2}", text)
#     if timestamp != []:
#         for stamp in timestamp:
#             if not be_quiet:
#                 print(stamp)
#             text = text.replace(stamp, "")
#     #
#     #
#     # ---- Remove other irrelevant text ----
#     # For all other irrelevant text, I searched for specific words in the transcriptions ("recording", "prolific", "describe") and copied the irrelevant speech excerpts manually.
#     irrelevant_text = [
#         "Please describe what you see in the image . Please speak for a full minute . We are recording .",
#         "Okay, this is where we see this bits please speak to the for full minute that we are recording .",
#         "Please describe what you see in this image . Please speak for the full minute . We are recording .",
#         "Okay please describe for what you see in this image please speak for the full minute we are recording .",
#         "Okay, please describe what you see this image, please . Please speak for the four minute we are recording . ",
#         "Please describe what you in this image, please speak for four minutes . We are recording . ",
#         "Please describe a scene that is pleased to be recording . ",
#         "we are recording . ",
#         "Studies available on prolific... ",
#         "[ ]",
#         "[ ? ]",
#         "( unclear )",
#         "( unclear . )",
#         "Transcribed by https : //otter.ai",
#     ]
#     #
#     for irr in irrelevant_text:
#         if irr in text and not be_quiet:
#             # print('Removing "{0}" from \n"{1}"'.format(irr, text))
#             print('Removing "{0}" "'.format(irr))
#         text = text.replace(irr, "")
#     return text
