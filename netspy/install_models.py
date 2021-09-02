"""Install NTLK Punkt tokenizer and Standford CoreNLP language models"""

import hashlib
import zipfile
from pathlib import Path
from typing import Optional, Union

import nltk
import requests
import stanza
import tqdm

from netspy.config import get_settings
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
    block_size = 128 * md5.block_size

    with file.open("rb") as f:

        chunk = f.read(block_size)

        while chunk:
            md5.update(chunk)
            chunk = f.read(block_size)

    return md5.hexdigest()


def file_exists(path: Path, file_hash: Optional[str] = None) -> bool:

    if not path.exists():
        return False

    if file_hash:
        # logger.warning("Hash of %s does not match `file_hash`", str(path))
        real_hash = hash_file(path)
        if not real_hash == file_hash:
            raise IncorrectHash(
                f"Hash of {path}: {real_hash},  does not match `file_hash`: {file_hash}"
            )
        logger.info("md5 check matches: %s", real_hash)
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


def install_nltk_punk(netspy_dir: Optional[Union[str, Path]] = None) -> DownloadStatus:

    settings = get_settings(netspy_dir)

    logger.info("Downloading: NLTK punkt library to: %s", settings.nltk_dir)

    if settings.nltk_dir.exists():
        logger.warning("NLTK directory already exists: %s", settings.nltk_dir)
        return DownloadStatus.ALREADY_EXISTS

    settings.netspy_dir.mkdir(exist_ok=True)
    nltk.download("punkt", download_dir=settings.nltk_dir, quiet=True)

    return DownloadStatus.SUCCESS


def install_corenlp(netspy_dir: Optional[Union[str, Path]] = None) -> DownloadStatus:

    settings = get_settings(netspy_dir)

    logger.info("Downloading: Stanza CoreNLP library to: %s", settings.core_nlp_dir)

    if settings.core_nlp_dir.exists():
        logger.warning(
            "Stanza CoreNLP directory already exists: %s", settings.core_nlp_dir
        )
        return DownloadStatus.ALREADY_EXISTS

    settings.netspy_dir.mkdir(exist_ok=True)
    stanza.install_corenlp(dir=settings.core_nlp_dir)
    return DownloadStatus.SUCCESS


def install_openie5(
    netspy_dir: Optional[Union[str, Path]] = None, md5: Optional[str] = None
) -> DownloadStatus:

    settings = get_settings(netspy_dir)
    fname = settings.openie

    if file_exists(fname, file_hash=md5):
        logger.info("OpenIE 5.1 binary already exits")
        return DownloadStatus.ALREADY_EXISTS

    if not settings.openie_dir.exists():
        settings.openie_dir.mkdir(parents=True)

    logger.info("Downloading: OpenIE 5.1 binary to: %s", fname)
    resp = download_file(str(settings.openie_url), fname, "Installing Openie5")

    resp.raise_for_status()

    return DownloadStatus.SUCCESS


def install_language_model(
    netspy_dir: Optional[Union[str, Path]] = None
) -> DownloadStatus:

    settings = get_settings(netspy_dir)
    fname = settings.openie_language_model
    fname_zip = Path(str(fname) + ".zip")

    if file_exists(fname, file_hash=None):
        logger.info("Language model already exists")
        return DownloadStatus.ALREADY_EXISTS

    if not settings.openie_dir.exists():
        settings.openie_dir.mkdir()

    if not settings.openie_data.exists():
        settings.openie_data.mkdir()

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


def install_dependencies(
    netspy_dir: Optional[Union[str, Path]] = None,
) -> None:

    install_nltk_punk(netspy_dir)
    install_corenlp(netspy_dir)
    install_openie5(netspy_dir)
    install_language_model(netspy_dir)
