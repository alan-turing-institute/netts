"""Install NTLK Punkt tokenizer and Standford CoreNLP language models"""

from pathlib import Path
from typing import Optional, Union

import nltk
import stanza


def nltk_default_download_dir() -> Path:
    """Default directory that the nltk package will download data to

    Returns:
        Path: Default directory that the nltk package will download data to
    """

    return Path(nltk.downloader.Downloader().default_download_dir())


def create_install_directory(directory: Path) -> None:
    """Create a directory to download external package files to.
    Will create the directory if it does not exist. Parent directories
    must already exist.

    Args:
        directory (Path): Directory to download package files to
    Raise:
        IOError: If parent directory does not exist
    """
    # Check parents exist
    parent_directory = directory.parents[0]
    if not parent_directory.exists():
        raise IOError(f"Parent directory does not exist: {parent_directory}")

    if not directory.exists():
        directory.mkdir(mode=0o644)


def install_nltk_punk(nlt_download_dir: Optional[Union[str, Path]] = None) -> None:

    if nlt_download_dir:
        if isinstance(nlt_download_dir, str):
            nlt_download_dir = Path(nlt_download_dir)
        create_install_directory(nlt_download_dir)

    nltk.download("punkt", download_dir=nlt_download_dir)


def install_corenlp(corenlp_dir=Optional[Union[str, Path]]) -> None:

    if corenlp_dir:
        if isinstance(corenlp_dir, str):
            corenlp_dir = Path(corenlp_dir)
        create_install_directory(corenlp_dir)
        stanza.install_corenlp(corenlp_dir)
    else:
        stanza.install_corenlp()


def install_models(
    nlt_download_dir: Optional[Union[str, Path]] = None,
    corenlp_download_dir=Optional[Union[str, Path]],
) -> None:
    """Install all files required by nltk and Stanford CoreNLP

    Args:
        nlt_download_dir (Optional[Union[str, Path]], optional): Directory to download ntlk files to. Defaults to None.
            If None will download to nltk_default_download_dir()

    Raises:
        IOError: Directory parents of nlt_download_dir or corenlp_download_dir do not exist
    """

    install_nltk_punk(nlt_download_dir)
    install_corenlp(corenlp_download_dir)
