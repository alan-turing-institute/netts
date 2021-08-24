import shutil
from pathlib import Path

from netspy.config import HOME_DIR, Settings
from netspy.install_models import install_corenlp, install_nltk_punk


class TestNLTK:
    def test_download_with_path(self, tmp_path):

        expected_directory = tmp_path / "nltk"
        install_nltk_punk(expected_directory)

        # Verify we got tokenizer directory
        expected_directory_subdir = list(expected_directory.iterdir())[0]
        assert "tokenizers" in expected_directory_subdir.parts[-1]

    def test_download_with_path_exists(self, tmp_path):

        expected_directory = tmp_path / "nltk"
        expected_directory.mkdir(0o777)
        install_nltk_punk(expected_directory)

        # Verify we got tokenizer directory
        expected_directory_subdir = list(expected_directory.iterdir())[0]
        assert "tokenizers" in expected_directory_subdir.parts[-1]

    def test_download_without_path(self):

        settings = Settings()

        # If directory already exists then set a new directory
        if settings.nltk_dir.exists():
            print("NLTK directory exists, using a new netspy directory")
            settings = Settings(netspy_dir=HOME_DIR / "tmp_netspy")
        try:
            install_nltk_punk()
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


# # class TestCoreNLP:
# #     def test_download_with_path(self, tmp_path):

# #         expected_directory = tmp_path / "corenlp"

# #         assert not expected_directory.exists()


# #         # Need to use a directory that doesn't already exist
# #         install_corenlp(expected_directory)

# #         # Verify the directory exists
# #         assert expected_directory.exists()

# #     def test_download_without_path(self):

# #         expected_directory = Path.home() /'stanza_corenlp'

# #         if expected_directory.exists():
#             raise IOError(f"Stanza CoreNLP dir exists. Can't run test until deleted. Run 'rm -r {expected_directory}'")

#         try:
#             install_corenlp()
#             assert expected_directory.exists()

#         finally:
#             # Clean up
#             shutil.rmtree(expected_directory)
