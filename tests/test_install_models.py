import shutil
from pathlib import Path
import pytest
from netspy.config import HOME_DIR, Settings, get_settings
from netspy.install_models import install_nltk_punk, install_corenlp, install_openie5, install_language_model


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
    def test_download_openie5(self):

        install_openie5()

    def test_install_language_model(self):

        install_language_model()