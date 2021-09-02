import hashlib
import logging
import shutil
from pathlib import Path
from typing import Any, Generator, Optional

import pytest
import requests

from netspy.config import Settings, get_settings
from netspy.install_models import install_corenlp, install_nltk_punk
from netspy.types import DownloadStatus, IncorrectHash

LOGGER = logging.getLogger(__name__)

# pylint: disable=redefined-outer-name


@pytest.fixture()
def netspy_home_dir() -> Generator[Settings, None, None]:
    "A home directory with cleanup"
    settings = get_settings()
    yield settings
    shutil.rmtree(settings.netspy_dir)


def hash_text(text: str) -> str:

    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def mock_download_file(
    _: str, path: Path, __: Optional[str] = None
) -> requests.Response:
    """Mock netspy.install_models.download_file

    Write an empty file to `path` and return a `requests.Response` with
    status code 200
    """

    with path.open("w") as f:
        f.write("")
    resp = requests.Response()
    resp.status_code = 200
    return resp


class TestNLTK:
    def _test_dowload_nltk(
        self, download_path: Path, expected_status: DownloadStatus
    ) -> None:

        settings = get_settings(download_path)

        assert install_nltk_punk(settings.netspy_dir) == expected_status
        assert settings.netspy_dir.exists()
        assert settings.nltk_dir.exists()

        # Verify we downloaded folder if we're expecting it to be there
        if expected_status == DownloadStatus.SUCCESS:
            expected_directory_subdir = list(settings.nltk_dir.iterdir())[0]
            assert "tokenizers" in expected_directory_subdir.parts[-1]

    def test_download_tmp(self, tmp_path: Path) -> None:

        netspy_directory = tmp_path / "netspy"
        self._test_dowload_nltk(
            netspy_directory, expected_status=DownloadStatus.SUCCESS
        )

    def test_download_tmp_exists(self, tmp_path: Path) -> None:

        settings = get_settings(tmp_path / "netspy")
        # Create nltk folder
        settings.nltk_dir.mkdir(parents=True)
        self._test_dowload_nltk(
            settings.netspy_dir, expected_status=DownloadStatus.ALREADY_EXISTS
        )

    @pytest.mark.skipif(
        get_settings().netspy_dir.exists(),
        reason="netspy dir already exists. Remove to run this test",
    )
    @pytest.mark.without_cache
    def test_download_home(self, netspy_home_dir: Settings) -> None:
        self._test_dowload_nltk(
            netspy_home_dir.netspy_dir, expected_status=DownloadStatus.SUCCESS
        )


class TestCoreNLP:
    @pytest.mark.slow
    def test_download_corenlp(self, tmp_path: Path) -> None:

        settings = get_settings(tmp_path / "netspy")
        install_corenlp(settings.netspy_dir)

        assert settings.core_nlp_dir.exists()


class TestOpenIE:
    def _test_download_openie5(
        self, download_path: Path, mocker: Any, mock: bool, expected_hash: str
    ) -> None:

        netspy_dir = download_path

        # Mock the download_file function to keep it fast
        if mock:
            mocker.patch(
                "netspy.install_models.download_file", side_effect=mock_download_file
            )
        # pylint: disable=import-outside-toplevel
        from netspy.install_models import install_openie5

        settings = get_settings(netspy_dir)

        # Download and ensure file exists
        assert (
            install_openie5(settings.netspy_dir, md5=expected_hash)
            == DownloadStatus.SUCCESS
        )
        assert settings.openie.exists()

        # Check we don't download when it already exists
        assert (
            install_openie5(settings.netspy_dir, md5=expected_hash)
            == DownloadStatus.ALREADY_EXISTS
        )

        # Pass the wrong hash and raise IncorrectHash exception
        with pytest.raises(IncorrectHash):
            install_openie5(settings.netspy_dir, md5=hash_text("adfasd"))

    def test_download_tmp(self, tmp_path: Path, mocker: Any) -> None:

        self._test_download_openie5(tmp_path / "netspy", mocker, True, hash_text(""))

    @pytest.mark.skipif(
        get_settings().netspy_dir.exists(),
        reason="netspy dir already exists. Remove to run this test",
    )
    def test_download_home(self, mocker: Any, netspy_home_dir: Settings) -> None:

        self._test_download_openie5(
            netspy_home_dir.netspy_dir, mocker, True, hash_text("")
        )

    @pytest.mark.slow
    @pytest.mark.skipif(
        get_settings().netspy_dir.exists(),
        reason="netspy dir already exists. Remove to run this test",
    )
    @pytest.mark.without_cache
    def test_download_real(self, mocker: Any, netspy_home_dir: Settings) -> None:
        """Download without mocking"""

        self._test_download_openie5(
            netspy_home_dir.netspy_dir, mocker, False, hash_text("")
        )
