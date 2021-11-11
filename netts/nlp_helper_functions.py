# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:07:59 2019

@author: Dr Sarah E Morgan, with input from Dr Bo Wang
modified by Dr. Caro Nettekoven, 2020
"""
import re
from itertools import compress

import nltk
import pandas as pd

from netts.contractions import CONTRACTION_MAP
from netts.logger import logger


def expand_contractions(text: str, contraction_mapping=None):
    if contraction_mapping is None:
        contraction_mapping = CONTRACTION_MAP

    contractions_pattern = re.compile(
        "({})".format("|".join(contraction_mapping.keys())),
        flags=re.IGNORECASE | re.DOTALL,
    )

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = (
            contraction_mapping.get(match)
            if contraction_mapping.get(match)
            else contraction_mapping.get(match.lower())
        )
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


def remove_interjections(text: str) -> str:
    """
    Removes interjections (e.g. Um, Mmm, yeah)

    Note: The interjections removed by this funciton are specific for English.
    Applying this to other languages may cause problems (For example in German "um" is a presposition)
    """
    english_interjections = {
        "Um",
        "um",
        "Uh",
        "uh",
        "Eh",
        "eh",
        "Ehm",
        "Em",
        "em",
        "Erm",
        "erm",
        "Ehhm",
        "ehhm",
        "Ehm",
        "ehm",
        "Mmm",
        "mmm",
        "Yeah",
        "yeah",
        "ah",
        "Ah",
        "Aah",
        "aah",
        "hmm",
        "hmmm",
        "Hmm",
        "Hmmm",
        "inaudible",
        "Inaudible",
    }

    text = expand_contractions(text)
    tokens = nltk.word_tokenize(text)

    # remove interjections
    tokens = [w for w in tokens if w not in english_interjections]

    return " ".join(tokens)


def remove_irrelevant_text(text):
    """
    Removes irrelevant text from the transcript.

    Irrelevant text was either added by the transcription program (example: 'Transcribed by https://otter.ai')
    or by the transcriber (examples: '[ ]', '[ ? ]', '( unclear )')
    or was genuine speech but recording of the participants reading out instructions
    (example:  'Please describe a scene that is pleased to be recording', 'we are recording').
    Since the last class of irrelevant speech can vary, I made a list of frequent read out instructions occurring in the dataset.
    These will have to be ammended for other task instructions.

    """

    # ---- Remove double-bracketed speech ----
    # Some transcribers marked irrelevant speech by putting it between double brackets.
    # Remove Anything between two (()), specifically between "( (" and ") )", since initial cleaning steps put a single whitespace between punctuation symbols
    match = re.match(r"^.*\(\s\((.*)\)\s\).*$", text)
    if match:
        logger.debug(match.group(1))
        match_text = "( (" + match.group(1) + ") )"
        text = text.replace(match_text, "")

    # ---- Remove speaker stamp ('Unknown Speaker  0:01')----
    speakerstamp = re.findall(r"\bUnknown Speaker\b\s\d{1}:\d{2}", text)
    if speakerstamp != []:
        for stamp in speakerstamp:
            logger.debug(stamp)
            text = text.replace(stamp, "")

    # ---- Remove time stamp ('00:01:00')----
    timestamp = re.findall(r"[0-9]{2}:[0-9]{2}:[0-9]{2}", text)
    if timestamp != []:
        for stamp in timestamp:
            logger.debug(stamp)
            text = text.replace(stamp, "")

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

    for irr in irrelevant_text:
        if irr in text:
            logger.debug('Removing "%s"', irr)
        text = text.replace(irr, "")
    return text


def replace_problematic_symbols(text: str) -> str:
    # key is problematic symbol, value is replacement symbol
    problematic_symbols = {
        "’": "'",
        "“": "",
        "”": "",
        # '..': " ",
        # '...': " ",
        # '....': " ",
        "…": "...",
        "‘": "'",
        "–": "-",
        "\n": " ",
    }

    for old, new in problematic_symbols.items():
        text = text.replace(old, new)

    return text


def get_transcript_properties(ex_stanza):
    punctuation_pos_tags = ["SENT", ".", ":", ",", "(", ")", '"', "'", "`", "$", "#"]

    # Count number of tokens that are not punctuation
    total_tokens = 0
    total_punctuations = 0

    for sent in ex_stanza.sentence:
        no_tokens_in_sentence = len(sent.token)
        total_tokens += no_tokens_in_sentence

        for token in sent.token:

            if token.pos in punctuation_pos_tags:

                total_punctuations += 1

    n_tokens = total_tokens - total_punctuations

    n_sentences = len(ex_stanza.sentence)

    return n_tokens, n_sentences, total_punctuations


# Setting up word2vec:
# Step 1: pip install word2vec
# https://pypi.org/project/word2vec/
# Step 2: Follow instructions in this tutorial notebook: https://nbviewer.jupyter.org/github/danielfrg/word2vec/blob/master/examples/word2vec.ipynb
# (follow instructions until the beginning of the second section, 'predictions'. So only set up the mode)
# w2v.word2phrase('word2vec_data/text8',
#                 'word2vec_data/text8-phrases', verbose=True)
# w2v.word2vec('word2vec_data/text8-phrases', 'word2vec_data/text8.bin',
#              size=100, binary=True, verbose=True)


def remove_duplicates(tats):
    """
    Removes duplicate transcripts from input list.

    Sometimes, different versions of the same transcript (same subject and same tat stimulus) exists,
    due to the transcriptions being generated by different transcribing programs.
    This function removes duplicate transcripts. Currently, the function keeps the first transcript.
    """
    tat_properties = []
    for tat_info in tats:
        tat = re.search(r"(?<=TAT)\w+", tat_info.name)[0]
        if len(tat) > 2:
            tat = tat.split("_")[0]
        # find subject id (7 digit combination before word "TAT")
        subj = tat_info.name.split("-TAT")[0][-7:]
        tat_properties.append(
            [
                subj,
                tat,
                tat_info.name.strip(".txt"),
                str(tat_info).split("Kings/")[1],
            ]
        )

    #  Make dataframe
    df = pd.DataFrame(tat_properties, columns=["subj", "tat", "filename", "fullpath"])

    dupl = df.duplicated(subset=["subj", "tat"], keep="first")
    tats = list(compress(tats, ~dupl))
    return tats


# df[df.duplicated(subset=['subj', 'tat'])]
# df.query('subj == "6376314" & tat == "13"')
# df.query('subj == "6377597" & tat == "10"')
# df.query('subj == "6378273" & tat == "8"')
# df.query('subj == "6376314" & tat == "13"')
# df.query('subj == "6376314" & tat == "13"')


def remove_bad_transcripts(tats, bad_transcripts_list):
    """
    Removes bad transcripts from input list.

    Bad transcripts are identified by the transcribers and provided as a .csv file with the file name in the column "Filenames".

    Parameters
    ----------
    bad_transcripts_list: path pointing to csv file
        The file names of bad transcripts should be provided in a column labelled "Filenames" in the csv file.
    tats: list of pathlib objects
        List of pathlib objects pointing to tats.

    Returns
    -------
    tats
        Cleaned input list.

    """
    bad_transcripts = pd.read_csv(bad_transcripts_list)
    bad_transcripts.Filenames = bad_transcripts.Filenames.str.strip(".weba")

    exclude = []
    for transcript in bad_transcripts.Filenames.values:
        matching = [
            (t, tat.name) for t, tat in enumerate(tats) if transcript in tat.name
        ]
        if matching != []:
            if len(matching) == 1:
                exclude.append(matching[0][0])
                logger.debug("removed bad transcript %s", matching[0])
            elif len(matching) > 1:
                exclude.extend([match[0] for match in matching])
                logger.debug("More than one duplicate found: %s", matching)

    logger.debug(
        "Obtained %s transcripts. Excluded %s bad transcripts. Kept %s transcripts.",
        len(tats),
        len(exclude),
        len(tats) - len(exclude),
    )

    tats = [T for t, T in enumerate(tats) if t not in exclude]
    return tats
