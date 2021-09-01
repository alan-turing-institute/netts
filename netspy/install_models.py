"""Install NTLK Punkt tokenizer and Standford CoreNLP language models"""

from pathlib import Path
from typing import Optional, Union

import requests
import nltk
import stanza
import tqdm

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


def install_openie5(netspy_dir: Optional[Union[str, Path]] = None) -> int:

    settings = get_settings(netspy_dir)
    settings.mk_netspy_dir()

    if not settings.open_ie_dir.exists():
        settings.open_ie_dir.mkdir()

    logger.info("Downloading: OpenIE 5.1 binary to: %s", settings.open_ie_dir)

    url = "https://netspy.blob.core.windows.net/netspy/openie-assembly-5.0-SNAPSHOT.jar"
    sas = "?sv=2020-04-08&st=2021-09-01T14%3A49%3A27Z&se=2022-08-31T14%3A49%3A00Z&sr=c&sp=rl&sig=eODqh0aLqLO5gVrgehkRRa498JytTT9qFh6ptOwbzBc%3D"

    fname = settings.open_ie_dir / "openie-assembly-5.0-SNAPSHOT.jar"

    if fname.exists():
        logger.info("OpenIE 5.1 binary to already exits")
        return

    resp = requests.get(url = url +  sas, stream=True)

    file_size = int(resp.headers.get("content-length"))
    chunk_size = 131072
    description = "Downloading OpenIE5"
    with fname.open(mode = "wb") as f:
        with tqdm.tqdm(total=file_size, unit='B', unit_scale=True, desc = description) as pbar:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    
    resp.raise_for_status()

    return resp.status_code

def install_language_model(netspy_dir: Optional[Union[str, Path]] = None) -> int:

    settings = get_settings(netspy_dir)
    settings.mk_netspy_dir()

    if not settings.open_ie_dir.exists():
        settings.open_ie_dir.mkdir()

    logger.info("Downloading: LanguageModel: %s", settings.open_ie_dir)

    url = "https://netspy.blob.core.windows.net/netspy/languageModel.zip"
    sas = "?sv=2020-04-08&st=2021-09-01T14%3A49%3A27Z&se=2022-08-31T14%3A49%3A00Z&sr=c&sp=rl&sig=eODqh0aLqLO5gVrgehkRRa498JytTT9qFh6ptOwbzBc%3D"

    fname = settings.open_ie_dir / "languageModel"

    if fname.exists():
        logger.info("OpenIE 5.1 binary to already exits")
        return

    resp = requests.get(url = url +  sas, stream=True)

    file_size = int(resp.headers.get("content-length"))
    chunk_size = 131072
    description = "Downloading OpenIE5"
    with fname.open(mode = "wb") as f:
        with tqdm.tqdm(total=file_size, unit='B', unit_scale=True, desc = description) as pbar:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    
    resp.raise_for_status()

    return resp.status_code



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
