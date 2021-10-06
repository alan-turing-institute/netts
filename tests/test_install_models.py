import hashlib
import logging
import os
import shutil
import zipfile
from pathlib import Path
from typing import Any, Generator, Optional

import pytest
import requests

from netspy.config import Settings, get_settings
from netspy.install_models import install_corenlp, install_nltk_punk, set_netspy_home
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


def mock_zip_file(_: str, path: Path, __: Optional[str] = None) -> requests.Response:
    """Mock netspy.install_models.download_file and zip contents

    Write an empty file to `path` and return a `requests.Response` with
    status code 200
    """

    file_path = path.parent / path.stem

    LOGGER.warning("Mock zip: Write to %s", path)
    with file_path.open("w") as f:
        f.write("")

    with zipfile.ZipFile(path, "w") as z:
        z.write(file_path, file_path.stem)

    file_path.unlink()
    resp = requests.Response()
    resp.status_code = 200
    return resp


class TestNLTK:
    def _test_dowload_nltk(
        self, download_path: Path, expected_status: DownloadStatus
    ) -> None:

        set_netspy_home(download_path)
        settings = get_settings()

        assert install_nltk_punk() == expected_status
        assert settings.netspy_dir.exists()
        assert settings.nltk_dir.exists()

        # Verify we downloaded folder if we're expecting it to be there
        if expected_status == DownloadStatus.SUCCESS:
            expected_directory_subdir = list(settings.nltk_dir.iterdir())[0]
            assert "tokenizers" in expected_directory_subdir.parts[-1]

        # Ensure the environment variable is reset
        settings.clear_corenlp_env()

    def test_download_tmp(self, tmp_path: Path) -> None:

        netspy_directory = tmp_path / "netspy"
        self._test_dowload_nltk(
            netspy_directory, expected_status=DownloadStatus.SUCCESS
        )

    def test_download_tmp_exists(self, tmp_path: Path) -> None:

        set_netspy_home(tmp_path / "netspy")
        settings = get_settings()
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
    @pytest.mark.ci_only
    @pytest.mark.slow
    def test_download_corenlp(self, tmp_path: Path) -> None:
        set_netspy_home(tmp_path / "netspy")
        settings = get_settings()
        install_corenlp()

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

        set_netspy_home(netspy_dir)
        settings = get_settings()

        # Download and ensure file exists
        assert install_openie5(md5=expected_hash) == DownloadStatus.SUCCESS
        assert settings.openie.exists()

        # Check we don't download when it already exists
        assert install_openie5(md5=expected_hash) == DownloadStatus.ALREADY_EXISTS

        # Pass the wrong hash and raise IncorrectHash exception
        with pytest.raises(IncorrectHash):
            install_openie5(md5=hash_text("adfasd"))

        # Ensure the environment variable is reset
        settings.clear_corenlp_env()

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

    @pytest.mark.ci_only
    @pytest.mark.slow
    @pytest.mark.without_cache
    @pytest.mark.skipif(
        get_settings().netspy_dir.exists(),
        reason="netspy dir already exists. Remove to run this test",
    )
    def test_download_real(self, mocker: Any, netspy_home_dir: Settings) -> None:
        """Download without mocking"""

        self._test_download_openie5(
            netspy_home_dir.netspy_dir, mocker, False, hash_text("")
        )


class TestLanguageMode:
    def _test_download_language_model(
        self, download_path: Path, mocker: Any, mock: bool, expected_hash: str
    ) -> None:

        netspy_dir = download_path

        # Mock the download_file function to keep it fast
        if mock:
            mocker.patch(
                "netspy.install_models.download_file", side_effect=mock_zip_file
            )
        # pylint: disable=import-outside-toplevel
        from netspy.install_models import install_language_model

        set_netspy_home(netspy_dir)
        settings = get_settings()

        # Download and ensure file exists
        assert install_language_model(md5=expected_hash) == DownloadStatus.SUCCESS
        assert settings.openie_data.exists()
        LOGGER.warning(
            "Dir %s, contents: %s",
            settings.openie_data,
            os.listdir(settings.openie_data),
        )

        assert settings.openie_language_model.exists()

        # Check we don't download when it already exists
        assert (
            install_language_model(md5=expected_hash) == DownloadStatus.ALREADY_EXISTS
        )

        # Pass the wrong hash and raise IncorrectHash exception
        with pytest.raises(IncorrectHash):
            install_language_model(md5=hash_text("adfasd"))

        # Ensure the environment variable is reset
        settings.clear_corenlp_env()

    def test_download_tmp(self, tmp_path: Path, mocker: Any) -> None:

        self._test_download_language_model(
            tmp_path / "netspy", mocker, True, hash_text("")
        )

    @pytest.mark.skipif(
        get_settings().netspy_dir.exists(),
        reason="netspy dir already exists. Remove to run this test",
    )
    def test_download_home(self, mocker: Any, netspy_home_dir: Settings) -> None:

        self._test_download_language_model(
            netspy_home_dir.netspy_dir, mocker, True, hash_text("")
        )

    @pytest.mark.ci_only
    @pytest.mark.slow
    @pytest.mark.without_cache
    @pytest.mark.skipif(
        get_settings().netspy_dir.exists(),
        reason="netspy dir already exists. Remove to run this test",
    )
    def test_download_real(self, mocker: Any, netspy_home_dir: Settings) -> None:
        """Download without mocking"""

        self._test_download_language_model(
            netspy_home_dir.netspy_dir, mocker, False, hash_text("")
        )
