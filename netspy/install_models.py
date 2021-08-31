"""Install NTLK Punkt tokenizer and Standford CoreNLP language models"""

from pathlib import Path
from typing import Optional, Union

import gdown
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


def install_openie5(netspy_dir: Optional[Union[str, Path]]) -> None:

    settings = get_settings(netspy_dir)
    settings.mk_netspy_dir()

    if not settings.open_ie_dir.exists():
        settings.open_ie_dir.mkdir()

    logger.info("Downloading: OpenIE 5.1 binary to: %s", settings.open_ie_dir)

    url = "https://drive.google.com/u/0/uc?id=19z8LO-CYOfJfV5agm82PZ2JNWNUPIB6D"
    fname = settings.open_ie_dir / "openie-assembly-5.0-SNAPSHOT.jar"

    if fname.exists():
        logger.info("OpenIE 5.1 binary to already exits")
        return

    gdown.download(url, output=str(fname))


def install_language_model(netspy_dir: Optional[Union[str, Path]]) -> None:

    settings = get_settings(netspy_dir)
    settings.mk_netspy_dir()

    if not settings.open_ie_dir.exists():
        settings.open_ie_dir.mkdir()

    logger.info("Downloading: Language model to: %s", settings.open_ie_dir / "data")

    url = "https://drive.google.com/u/0/uc?id=0B-5EkZMOlIt2cFdjYUJZdGxSREU"
    fname = settings.open_ie_dir / "data" / "languageModel"

    if fname.exists():
        logger.info("OpenIE 5.1 binary to already exits")
        return

    # Create parent directory if required
    fname.parents[0].mkdir(exist_ok=True)
    gdown.download(url, output=str(fname))


def install_models(
    netspy_dir: Optional[Union[str, Path]] = None,
) -> None:

    install_nltk_punk(netspy_dir)
    install_corenlp(netspy_dir)
    install_openie5(netspy_dir)
    install_language_model(netspy_dir)
