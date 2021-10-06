"""Install NTLK Punkt tokenizer and Standford CoreNLP language models"""

import hashlib
import os
import zipfile
from pathlib import Path
from typing import Optional

import nltk
import requests
import stanza
import tqdm

from netspy.config import NETSPY_DIR, get_settings
from netspy.logger import logger
from netspy.types import DownloadStatus, IncorrectHash


def hash_file(file: Path) -> str:
    """Return the hash of a file

    Args:
        file (Path): File to hash

    Returns:
        str: hash hexdigest
    """
    md5 = hashlib.md5()
    block_size = 128 * md5.block_size * 10

    with file.open("rb") as f:

        chunk = f.read(block_size)

        while chunk:
            md5.update(chunk)
            chunk = f.read(block_size)

    return md5.hexdigest()


def file_exists(path: Path, file_hash: Optional[str] = None) -> bool:

    if not path.exists():
        return False

    real_hash = hash_file(path)
    if file_hash:
        if not real_hash == file_hash:
            raise IncorrectHash(
                f"Hash of {path}: {real_hash},  does not match `file_hash`: {file_hash}"
            )
    logger.info("File installed: %s , md5 hash: %s", path, real_hash)

    return True


def download_file(
    url: str, path: Path, description: Optional[str] = None
) -> requests.Response:

    logger.warning("Downloading from url: %s to %s", url, path)

    resp = requests.get(url=url, stream=True)
    file_size = int(resp.headers.get("content-length"))
    chunk_size = 131072
    with path.open(mode="wb") as f:
        with tqdm.tqdm(
            total=file_size, unit="B", unit_scale=True, desc=description
        ) as pbar:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

    return resp


def install_nltk_punk() -> DownloadStatus:

    settings = get_settings()

    logger.info("Downloading: NLTK punkt library to: %s", settings.nltk_dir)

    if settings.nltk_dir.exists():
        logger.warning("NLTK directory already exists: %s", settings.nltk_dir)
        return DownloadStatus.ALREADY_EXISTS

    settings.netspy_dir.mkdir(exist_ok=True)
    nltk.download("punkt", download_dir=settings.nltk_dir, quiet=True)

    return DownloadStatus.SUCCESS


def install_corenlp() -> DownloadStatus:

    settings = get_settings()

    logger.info("Downloading: Stanza CoreNLP library to: %s", settings.core_nlp_dir)

    if settings.core_nlp_dir.exists():
        logger.warning(
            "Stanza CoreNLP directory already exists: %s", settings.core_nlp_dir
        )
        return DownloadStatus.ALREADY_EXISTS

    settings.netspy_dir.mkdir(exist_ok=True)
    stanza.install_corenlp(dir=settings.core_nlp_dir)
    return DownloadStatus.SUCCESS


def install_openie5(md5: Optional[str] = None) -> DownloadStatus:

    settings = get_settings()
    fname = settings.openie

    if file_exists(fname, file_hash=md5):
        return DownloadStatus.ALREADY_EXISTS

    if not settings.openie_dir.exists():
        settings.openie_dir.mkdir(parents=True)

    logger.info("Downloading: OpenIE 5.1 binary to: %s", fname)
    resp = download_file(str(settings.openie_url), fname, "Installing Openie5")

    resp.raise_for_status()

    return DownloadStatus.SUCCESS


def install_language_model(md5: Optional[str] = None) -> DownloadStatus:

    settings = get_settings()
    fname = settings.openie_language_model
    fname_zip = Path(str(fname) + ".zip")

    if file_exists(fname, file_hash=md5):
        return DownloadStatus.ALREADY_EXISTS

    if not settings.openie_data.exists():
        logger.info("Creating dir %s", settings.openie_data)
        settings.openie_data.mkdir(parents=True)

    logger.info("Downloading: Language model to: %s", fname)
    resp = download_file(
        str(settings.openie_language_url), fname_zip, "Installing language model"
    )
    resp.raise_for_status()

    # unzip file
    with zipfile.ZipFile(fname_zip, "r") as z:
        z.extractall(settings.openie_data)

    # Remove zip file
    fname_zip.unlink()

    return DownloadStatus.SUCCESS


def install_dependencies() -> None:

    install_nltk_punk()
    install_corenlp()
    install_openie5(md5="5ffa7a69fc7a04c07451582c40da80d6")
    install_language_model(md5="5f79c2b84ded0a0fcfffe6444bfb9561")
