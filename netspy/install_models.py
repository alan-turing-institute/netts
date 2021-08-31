"""Install NTLK Punkt tokenizer and Standford CoreNLP language models"""

from pathlib import Path
from typing import Optional, Union

import nltk
import requests
from requests.sessions import session
import stanza
import tqdm
from requests.models import ChunkedEncodingError, stream_decode_response_unicode

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


def install_openie5(netspy_dir) -> None:

    def _get_confirmation_token(resp):

        # Check for warning in cookie
        for key, value in resp.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None
        
    settings = get_settings(netspy_dir)
    settings.mk_netspy_dir()

    url = "https://drive.google.com/uc?export=download"
    params = {"id": "19z8LO-CYOfJfV5agm82PZ2JNWNUPIB6D"}

    resp = requests.get(
        url, params=params, stream=True
    )
    token = _get_confirmation_token(resp)


    params.update({'confirm': token})
    resp = requests.get(url, params, stream=True)
    token = _get_confirmation_token(resp)

    print(resp.headers)
    print(resp.content)
    return
    # print( _get_confirmation_token(resp))
    # # Check for confirmation token in cookie
    # token = _get_confirmation_token(resp)
    # if token:
    #     params.update({'confirm': token})
    #     resp = requests.get(url, params, stream=True)
    # print( _get_confirmation_token(resp))

    # print( resp.cookies.keys())

    settings.openie5_dir.mkdir(exist_ok=True)
    openie5_file = settings.openie5_dir / "openie-assembly-5.0-SNAPSHOT.jar"
    openie5_file.touch()
    
    logger.info("Downloading: OpenIE5 to: %s", settings.openie5_dir)
    with open(openie5_file, "wb") as f:
        
        file_size = int(resp.headers.get("content-length"))
        chunk_size = 131072
        desc = "Downloading " + url
        with tqdm.tqdm(unit="B", unit_scale=True, desc=desc) as pbar:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    pbar.update(len(chunk))

    resp.raise_for_status()

    return resp.status_code


def install_models(
    netspy_dir: Optional[Union[str, Path]] = None,
) -> None:

    install_nltk_punk(netspy_dir)
    install_corenlp(netspy_dir)
    install_openie5(netspy_dir)
