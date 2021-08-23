from tqdm.std import TqdmMonitorWarning

from netspy.install_models import install_nltk_punk, nltk_default_download_dir


class TestNtl:
    def test_download_with_path(self, tmp_path):

        install_nltk_punk(tmp_path)

        # Verify we got tokenizer directory
        expected_directory = list(tmp_path.iterdir())[0]
        assert "tokenizers" in expected_directory.parts[-1]

    def test_download_without_path(self):

        install_nltk_punk(None)

        # Verify we got tokenizer directory
        expected_directory = list(nltk_default_download_dir().iterdir())[0]
        assert "tokenizers" in expected_directory.parts[-1]


# def test_install_models():

#     netspy.install_models(nlt_download_dir="~/")
#     netspy.install_models(
#         nlt_download_dir="/Users/ogiles/Documents/project_repos/netspy"
#     )

#     print("Done")
