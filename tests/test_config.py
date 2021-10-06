from pathlib import Path
import pytest
from netspy.config import Settings, get_settings
from netspy.install_models import set_netspy_home
import os

def test_config_dir(tmp_path: Path) -> None:

    settings = get_settings()

    # If netspy_dir exists then use a tmp directory
    if settings.netspy_dir.exists():
        settings = Settings(netspy_dir=tmp_path)

    # Create directory and clean up after
    try:
        settings.mk_netspy_dir()
        assert settings.netspy_dir.exists()
    finally:
        settings.netspy_dir.rmdir()
        assert not settings.netspy_dir.exists()


@pytest.mark.parametrize("x", range(10))
def test_set_netspy_home(tmp_path: Path, x):

    expected_dir = tmp_path / "netspy"
    set_netspy_home(expected_dir)

    settings = get_settings()
    assert settings.netspy_dir == expected_dir
    assert settings.nltk_dir == expected_dir / "nltk_data"
    assert settings.core_nlp_dir == expected_dir / "stanza_corenlp"
    assert settings.openie_dir== expected_dir / "openie"
    assert settings.openie == expected_dir / "openie" / "openie-assembly-5.0-SNAPSHOT.jar"
    assert settings.openie_data == expected_dir / "openie" / "data"
    assert settings.openie_language_model == expected_dir / "openie" / "data" / "languageModel"

    assert os.environ["CORENLP_HOME"] == str(expected_dir / "stanza_corenlp")

    settings.clear_corenlp_env()


    get_settings().netspy_dir
    print(get_settings().core_nlp_dir)