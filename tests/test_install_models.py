# pylint: disable=redefined-outer-name, unused-argument

import hashlib
import logging
import os
import shutil
import zipfile
from pathlib import Path
from typing import Any, Generator, Optional

import pytest
import pytest_mock
import requests

from netts.config import Settings, get_settings
from netts.install_models import download_file, install_corenlp, install_nltk_punk
from netts.netts_types import DownloadStatus, IncorrectHash

LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def netts_home_dir() -> Generator[Settings, None, None]:
    "A home directory with cleanup"

    settings = get_settings()
    yield settings
    shutil.rmtree(settings.netts_dir)


def hash_text(text: str) -> str:

    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def mock_download_file(
    _: str, path: Path, __: Optional[str] = None
) -> requests.Response:
    """Mock netts.install_models.download_file

    Write an empty file to `path` and return a `requests.Response` with
    status code 200
    """

    with path.open("w") as f:
        f.write("")
    resp = requests.Response()
    resp.status_code = 200
    return resp


def mock_zip_file(_: str, path: Path, __: Optional[str] = None) -> requests.Response:
    """Mock netts.install_models.download_file and zip contents

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

        settings = get_settings()

        assert install_nltk_punk() == expected_status
        assert settings.netts_dir.exists()
        assert settings.nltk_dir.exists()

        # Verify we downloaded folder if we're expecting it to be there
        if expected_status == DownloadStatus.SUCCESS:
            expected_directory_subdir = list(settings.nltk_dir.iterdir())[0]
            assert "tokenizers" in expected_directory_subdir.parts[-1]

    def test_download_tmp(self, tmp_path_netts: Path) -> None:

        self._test_dowload_nltk(tmp_path_netts, expected_status=DownloadStatus.SUCCESS)

    def test_download_tmp_exists(self, tmp_path_netts: Path) -> None:

        settings = get_settings()
        # Create nltk folder
        settings.nltk_dir.mkdir(parents=True)
        self._test_dowload_nltk(
            settings.netts_dir, expected_status=DownloadStatus.ALREADY_EXISTS
        )

    @pytest.mark.skipif(
        get_settings().netts_dir.exists(),
        reason="netts dir already exists. Remove to run this test",
    )
    @pytest.mark.without_cache
    def test_download_home(self, netts_home_dir: Settings) -> None:
        self._test_dowload_nltk(
            netts_home_dir.netts_dir, expected_status=DownloadStatus.SUCCESS
        )


class TestCoreNLP:
    @pytest.mark.ci_only
    @pytest.mark.slow
    def test_download_corenlp(self, tmp_path_netts: Path) -> None:

        settings = get_settings()
        install_corenlp()

        assert settings.core_nlp_dir.exists()


class TestOpenIE:
    def _test_download_openie5(
        self, download_path: Path, mocker: Any, mock: bool, expected_hash: str
    ) -> None:

        # Mock the download_file function to keep it fast
        if mock:
            mocker.patch(
                "netts.install_models.download_file", side_effect=mock_download_file
            )
        # pylint: disable=import-outside-toplevel
        from netts.install_models import install_openie5

        settings = get_settings()

        # Download and ensure file exists
        assert install_openie5(md5=expected_hash) == DownloadStatus.SUCCESS
        assert settings.openie.exists()

        # Check we don't download when it already exists
        assert install_openie5(md5=expected_hash) == DownloadStatus.ALREADY_EXISTS

        # Pass the wrong hash and raise IncorrectHash exception
        with pytest.raises(IncorrectHash):
            install_openie5(md5=hash_text("adfasd"))

    def test_download_tmp(self, tmp_path_netts: Path, mocker: Any) -> None:

        self._test_download_openie5(tmp_path_netts, mocker, True, hash_text(""))

    @pytest.mark.skipif(
        get_settings().netts_dir.exists(),
        reason="netts dir already exists. Remove to run this test",
    )
    def test_download_home(self, mocker: Any, netts_home_dir: Settings) -> None:

        self._test_download_openie5(
            netts_home_dir.netts_dir, mocker, True, hash_text("")
        )

    @pytest.mark.ci_only
    @pytest.mark.slow
    @pytest.mark.without_cache
    @pytest.mark.skipif(
        get_settings().netts_dir.exists(),
        reason="netts dir already exists. Remove to run this test",
    )
    def test_download_real(self, mocker: Any, netts_home_dir: Settings) -> None:
        """Download without mocking"""

        self._test_download_openie5(
            netts_home_dir.netts_dir, mocker, False, hash_text("")
        )


class TestLanguageMode:
    def _test_download_language_model(
        self, download_path: Path, mocker: Any, mock: bool, expected_hash: str
    ) -> None:

        # Mock the download_file function to keep it fast
        if mock:
            mocker.patch(
                "netts.install_models.download_file", side_effect=mock_zip_file
            )
        # pylint: disable=import-outside-toplevel
        from netts.install_models import install_language_model

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

    def test_download_tmp(self, tmp_path_netts: Path, mocker: Any) -> None:

        self._test_download_language_model(tmp_path_netts, mocker, True, hash_text(""))

    @pytest.mark.skipif(
        get_settings().netts_dir.exists(),
        reason="netts dir already exists. Remove to run this test",
    )
    def test_download_home(self, mocker: Any, netts_home_dir: Settings) -> None:

        self._test_download_language_model(
            netts_home_dir.netts_dir, mocker, True, hash_text("")
        )

    @pytest.mark.ci_only
    @pytest.mark.slow
    @pytest.mark.without_cache
    @pytest.mark.skipif(
        get_settings().netts_dir.exists(),
        reason="netts dir already exists. Remove to run this test",
    )
    def test_download_real(self, mocker: Any, netts_home_dir: Settings) -> None:
        """Download without mocking"""

        self._test_download_language_model(
            netts_home_dir.netts_dir, mocker, False, hash_text("")
        )


class TestDownloadFile:
    def test_tries_twice(self, mocker: pytest_mock.MockerFixture) -> None:
        mock_get = mocker.patch("requests.get")
        mock_get.side_effect = requests.exceptions.ChunkedEncodingError

        raised = False
        try:
            mock_path = mocker.MagicMock()
            download_file("my-url", mock_path)
        except requests.exceptions.ChunkedEncodingError:
            raised = True

        assert raised

        expected_call = mocker.call(url="my-url", stream=True)
        mock_get.assert_has_calls([expected_call, expected_call])
