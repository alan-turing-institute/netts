import os
from pathlib import Path

import pytest
import rtoml
from devtools import debug

import netspy
from netspy.config import Settings, get_settings
from netspy.config_file import ServerInfo, Servers

ALT_OPENIE_PORT = 9999
ALT_CORENLP_PORT = 1111


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
def test_set_netspy_home(tmp_path_netspy: Path, x: int) -> None:

    expected_dir = tmp_path_netspy
    os.environ["netspy_dir"] = str(expected_dir)

    settings = get_settings()
    assert settings.netspy_dir == expected_dir
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
def local_config(tmp_path_netspy: Path) -> Path:

    config_file = tmp_path_netspy / "netspy.toml"
    config_file.write_text(netspy.Config.default())

    return config_file


@pytest.fixture()
def alt_local_config(tmp_path_netspy: Path) -> Path:

    alt_config_file = tmp_path_netspy / "netspy_alt.toml"

    alt_config = netspy.Config(
        server=Servers(
            openie=ServerInfo(port=ALT_OPENIE_PORT),
            corenlp=ServerInfo(port=ALT_CORENLP_PORT),
        )
    )

    alt_config_file.write_text(rtoml.dumps(alt_config.dict()))

    return alt_config_file


class TestNetspyConfig:
    def test_default(self) -> None:

        settings = Settings()

        assert isinstance(settings.netspy_config, netspy.Config)
        assert vars(settings.netspy_config) == vars(netspy.Config())

    def test_file(self, local_config: Path) -> None:

        settings = Settings()
        assert isinstance(settings.netspy_config, netspy.Config)
        assert vars(settings.netspy_config) == vars(netspy.Config())

    def test_file_arg(self, local_config: Path) -> None:

        settings = Settings(netspy_config=local_config)
        assert isinstance(settings.netspy_config, netspy.Config)
        assert vars(settings.netspy_config) == vars(netspy.Config())

    def test_file_str_arg(self, local_config: Path) -> None:

        settings = Settings(netspy_config=str(local_config))
        assert isinstance(settings.netspy_config, netspy.Config)
        assert vars(settings.netspy_config) == vars(netspy.Config())

    def test_alt_file(self, local_config: Path, alt_local_config: Path) -> None:

        settings = Settings(netspy_config=alt_local_config)
        assert isinstance(settings.netspy_config, netspy.Config)
        assert vars(settings.netspy_config) != vars(netspy.Config())

        debug(settings.netspy_config.server)
        assert settings.netspy_config.server.openie.port == ALT_OPENIE_PORT
        assert settings.netspy_config.server.corenlp.port == ALT_CORENLP_PORT
