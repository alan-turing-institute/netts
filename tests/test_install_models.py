import shutil
from pathlib import Path
import pytest
from netspy.config import HOME_DIR, Settings, get_settings
from netspy.install_models import install_nltk_punk, install_corenlp, install_language_model
import hashlib
import requests 

from netspy.types import IncorrectHash, DownloadStatus

def hash_text(text: str) -> str:
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()





def mock_download_file(url: str, path: Path) -> requests.Response:
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
    def test_download_with_path(self, tmp_path: Path) -> None:

        netspy_directory = tmp_path / "netspy"
        install_nltk_punk(netspy_directory)

        assert netspy_directory.exists()
        nltk_directory = get_settings().nltk_dir
        assert nltk_directory.exists()

        # Verify we downloaded folder
        expected_directory_subdir = list(nltk_directory.iterdir())[0]
        assert "tokenizers" in expected_directory_subdir.parts[-1]

    def test_download_with_path_exists(self, tmp_path: Path) -> None:

        netspy_directory = tmp_path / "netspy"
        netspy_directory.mkdir()
        install_nltk_punk(netspy_directory)

        # Verify we got tokenizer directory
        nltk_directory = get_settings().nltk_dir
        expected_directory_subdir = list(nltk_directory.iterdir())[0]
        assert "tokenizers" in expected_directory_subdir.parts[-1]

    def test_download_without_path(self) -> None:

        settings = Settings()

        # If directory already exists then set a new directory
        if settings.nltk_dir.exists():
            print("NLTK directory exists, using a new netspy directory")
            settings = Settings(netspy_dir=HOME_DIR / "tmp_netspy")
        try:
            install_nltk_punk(settings.netspy_dir)
            # Verify we got tokenizer directory
            expected_directory = list(settings.nltk_dir.iterdir())[0]
            assert "tokenizers" in expected_directory.parts[-1]
        finally:
            # Clean up
            shutil.rmtree(settings.nltk_dir)
            assert not settings.nltk_dir.exists()

            # If netspy dir is empty remove it
            if not next(settings.netspy_dir.iterdir(), None):
                print("Removeing netspy_dir")
                settings.netspy_dir.rmdir()

# class TestCoreNLP:
#     @pytest.mark.release
#     def test_core_nlp(self, tmp_path: Path) -> None:

#         print("Running CORENLP")  
#         netspy_directory = tmp_path / "netspy"
#         install_corenlp(netspy_directory)

#         assert netspy_directory.exists()

class TestOpenIE:

    
    def test_download_openie5(self, mocker, tmp_path):

        # Mock the download_file function to keep it fast
        mock = mocker.patch('netspy.install_models.download_file', side_effect = mock_download_file)
        from netspy.install_models import install_openie5

        settings = get_settings(tmp_path / "netspy")

        # Download and ensure file exists
        assert install_openie5(settings.netspy_dir) == DownloadStatus.SUCCESS
        assert settings.openie.exists()


        assert install_openie5(settings.netspy_dir, md5 = hash_text("")) == DownloadStatus.ALREADY_EXISTS
        
        # Pass the wrong hash and raise IncorrectHash exception
        with pytest.raises(IncorrectHash):
            install_openie5(settings.netspy_dir, md5 = hash_text("adfasd"))



    def test_install_language_model(self):

        install_language_model()

