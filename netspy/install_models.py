"""Install NTLK Punkt tokenizer and Standford CoreNLP language models"""

from pathlib import Path
from typing import Optional, Union

import nltk
import stanza

from netspy.config import get_settings


def install_nltk_punk(netspy_dir: Optional[Union[str, Path]] = None) -> None:

    settings = get_settings(netspy_dir)
    settings.mk_netspy_dir()
    nltk.download("punkt", download_dir=settings.nltk_dir)


def install_corenlp(netspy_dir: Optional[Union[str, Path]] = None) -> None:

    settings = get_settings(netspy_dir)
    settings.mk_netspy_dir()

    stanza.install_corenlp(dir=settings.core_nlp_dir)


def install_models(
    netspy_dir: Optional[Union[str, Path]] = None,
) -> None:

    install_nltk_punk(netspy_dir)
    install_corenlp(netspy_dir)
