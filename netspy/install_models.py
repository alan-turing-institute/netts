"""Install NTLK Punkt tokenizer and Standford CoreNLP language models"""

from pathlib import Path
from typing import Optional, Union

import nltk
import stanza

from netspy.config import get_settings
from netspy.logger import logger


def install_nltk_punk(netspy_dir: Optional[Union[str, Path]] = None) -> None:

    settings = get_settings(netspy_dir)
    settings.mk_netspy_dir()

    logger.info("Downloading: NLTK punkt library to: %s", settings.nltk_dir)

    if settings.nltk_dir.exists():
        logger.warning("NLTK directory already exists: %s", settings.nltk_dir)
        return
    nltk.download("punkt", download_dir=settings.nltk_dir, quiet=True)


def install_corenlp(netspy_dir: Optional[Union[str, Path]] = None) -> None:

    settings = get_settings(netspy_dir)
    settings.mk_netspy_dir()

    logger.info("Downloading: Stanza CoreNLP library to: %s", settings.core_nlp_dir)

    if settings.core_nlp_dir.exists():
        logger.warning(
            "Stanza CoreNLP directory already exists: %s", settings.core_nlp_dir
        )
        return
    stanza.install_corenlp(dir=settings.core_nlp_dir)


def install_models(
    netspy_dir: Optional[Union[str, Path]] = None,
) -> None:

    install_nltk_punk(netspy_dir)
    install_corenlp(netspy_dir)
