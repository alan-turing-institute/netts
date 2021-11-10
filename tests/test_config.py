# pylint: disable=redefined-outer-name
import os
from pathlib import Path

import pytest
import rtoml
from devtools import debug

import netts
from netts.config import Settings, get_settings
from netts.config_file import ServerInfo, Servers

ALT_OPENIE_PORT = 9999
ALT_CORENLP_PORT = 1111


def test_config_dir(tmp_path: Path) -> None:

    settings = get_settings()

    # If netts_dir exists then use a tmp directory
    if settings.netts_dir.exists():
        settings = Settings(netts_dir=tmp_path)

    # Create directory and clean up after
    try:
        settings.mk_netts_dir()
        assert settings.netts_dir.exists()
    finally:
        settings.netts_dir.rmdir()
        assert not settings.netts_dir.exists()


# pylint: disable=unused-argument
@pytest.mark.parametrize("x", range(10))
def test_set_netts_home(tmp_path: Path, x: int) -> None:

    expected_dir = tmp_path
    os.environ["netts_dir"] = str(expected_dir)

    settings = get_settings()
    assert settings.netts_dir == expected_dir
    assert settings.nltk_dir == expected_dir / "nltk_data"
    assert settings.core_nlp_dir == expected_dir / "stanza_corenlp"
    assert settings.openie_dir == expected_dir / "openie"
    assert (
        settings.openie == expected_dir / "openie" / "openie-assembly-5.0-SNAPSHOT.jar"
    )
    assert settings.openie_data == expected_dir / "openie" / "data"
    assert (
        settings.openie_language_model
        == expected_dir / "openie" / "data" / "languageModel"
    )
    assert os.environ["CORENLP_HOME"] == str(expected_dir / "stanza_corenlp")


@pytest.fixture()
def local_config(tmp_path: Path) -> Path:

    config_file = tmp_path / "netts.toml"
    config_file.write_text(netts.Config.default())

    return config_file


@pytest.fixture()
def alt_local_config(tmp_path: Path) -> Path:

    alt_config_file = tmp_path / "netts_alt.toml"

    alt_config = netts.Config(
        server=Servers(
            openie=ServerInfo(port=ALT_OPENIE_PORT),
            corenlp=ServerInfo(port=ALT_CORENLP_PORT),
        )
    )

    alt_config_file.write_text(rtoml.dumps(alt_config.dict()))

    return alt_config_file


class TestNettsConfig:
    def test_default(self) -> None:

        settings = Settings()

        assert isinstance(settings.netts_config, netts.Config)
        assert vars(settings.netts_config) == vars(netts.Config())

    def test_file(self, local_config: Path) -> None:

        settings = Settings()
        assert isinstance(settings.netts_config, netts.Config)
        assert vars(settings.netts_config) == vars(netts.Config())

    def test_file_arg(self, local_config: Path) -> None:

        settings = Settings(netts_config=local_config)
        assert isinstance(settings.netts_config, netts.Config)
        assert vars(settings.netts_config) == vars(netts.Config())

    def test_file_str_arg(self, local_config: Path) -> None:

        settings = Settings(netts_config=str(local_config))
        assert isinstance(settings.netts_config, netts.Config)
        assert vars(settings.netts_config) == vars(netts.Config())

    def test_alt_file(self, local_config: Path, alt_local_config: Path) -> None:

        settings = Settings(netts_config=alt_local_config)
        assert isinstance(settings.netts_config, netts.Config)
        assert vars(settings.netts_config) != vars(netts.Config())

        debug(settings.netts_config.server)
        assert settings.netts_config.server.openie.port == ALT_OPENIE_PORT
        assert settings.netts_config.server.corenlp.port == ALT_CORENLP_PORT
