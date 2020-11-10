import pandas as pd

# extract lemma


def extract_lemma(doc):
    parsed_text = {'word': [], 'lemma': []}
    for sent in doc.sentences:
        for wrd in sent.words:
            # extract text and lemma
            parsed_text['word'].append(wrd.text)
            parsed_text['lemma'].append(wrd.lemma)
    # return a dataframe
    return pd.DataFrame(parsed_text)


# Usage:
# extract_lemma(doc)
