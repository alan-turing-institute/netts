"""Install NTLK Punkt tokenizer and Standford CoreNLP language models"""

from pathlib import Path
from typing import Optional, Union

import nltk
import stanza
from click import core

from netspy.config import NETSPY_DIR, get_settings

settings = get_settings()


def install_nltk_punk(nltk_download_dir: Optional[Union[str, Path]] = None) -> None:
    """Install nltk punk

    Args:
        nlt_download_dir (Optional[Union[str, Path]], optional): Directory to install nltk data. Defaults to None.
    """

    if not nltk_download_dir:
        # Ensure netspy directory exists
        settings.mk_netspy_dir()
        nltk_download_dir = get_settings().nltk_dir

    if isinstance(nltk_download_dir, Path):
        nltk_download_dir = str(nltk_download_dir)

    nltk.download("punkt", download_dir=nltk_download_dir)


def install_corenlp(corenlp_dir: Optional[Union[str, Path]] = None) -> None:
    """Install CoreNLP server

    Args:
        corenlp_dir (Optional[Union[str, Path]], optional): Directory to install corenlp data. Defaults to None.
    """

    if not corenlp_dir:
        # Ensure netspy directory exists
        settings.mk_netspy_dir()
        corenlp_dir = get_settings().core_nlp_dir

    if isinstance(corenlp_dir, Path):
        corenlp_dir = str(corenlp_dir)

    stanza.install_corenlp(dir=corenlp_dir)


def install_models(
    nltk_download_dir: Optional[Union[str, Path]] = None,
    corenlp_download_dir: Optional[Union[str, Path]] = None,
) -> None:
    """Install all files required by nltk and Stanford CoreNLP

    Args:
        nlt_download_dir (Optional[Union[str, Path]], optional): Directory to download ntlk files to. Defaults to None.
            If None will download to nltk_default_download_dir()

    Raises:
        IOError: Directory parents of nlt_download_dir or corenlp_download_dir do not exist
    """

    install_nltk_punk(nltk_download_dir)
    install_corenlp(corenlp_download_dir)