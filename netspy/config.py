import os
from functools import lru_cache

# from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Union

import nltk
from pydantic import BaseSettings, validator

if TYPE_CHECKING:
    HttpUrl = str
else:
    from pydantic import HttpUrl

HOME_DIR = Path.home()
NETSPY_DIR = HOME_DIR / "netspy"


class Settings(BaseSettings):

    netspy_dir: Path = NETSPY_DIR
    openie_url: HttpUrl = (
        "https://netspy.blob.core.windows.net/netspy/openie-assembly-5.0-SNAPSHOT.jar"
        + "?sv=2020-04-08&st=2021-09-01T14%3A49%3A27Z&se=2022-08-31T14%3A49%3A00Z&sr=c&sp=rl&sig=eODqh0aLqLO5gVrgehkRRa498JytTT9qFh6ptOwbzBc%3D"
    )
    openie_language_url: HttpUrl = (
        "https://netspy.blob.core.windows.net/netspy/languageModel.zip"
        + "?sv=2020-04-08&st=2021-09-01T14%3A49%3A27Z&se=2022-08-31T14%3A49%3A00Z&sr=c&sp=rl&sig=eODqh0aLqLO5gVrgehkRRa498JytTT9qFh6ptOwbzBc%3D"
    )
    config_file: Optional[Path] = None

    nltk_dir: Path = netspy_dir / "nltk_data"
    core_nlp_dir: Path = netspy_dir / "stanza_corenlp"
    openie_dir: Path = netspy_dir / "openie"
    openie: Path = openie_dir / "openie-assembly-5.0-SNAPSHOT.jar"
    openie_data: Path = openie_dir / "data"
    openie_language_model: Path = openie_data / "languageModel"

    # @property
    # def nltk_dir(cls) -> Path:
    #     return cls.netspy_dir / "nltk_data"

    # @property
    # def core_nlp_dir(cls) -> Path:
    #     return cls.netspy_dir / "stanza_corenlp"

    # @property
    # def openie_dir(cls) -> Path:
    #     return cls.netspy_dir / "openie"

    # @property
    # def openie(cls) -> Path:
    #     return cls.openie_dir / "openie-assembly-5.0-SNAPSHOT.jar"

    # @property
    # def openie_data(cls) -> Path:

    #     return cls.openie_dir / "data"

    # @property
    # def openie_language_model(cls) -> Path:
    #     return cls.openie_data / "languageModel"

    def mk_netspy_dir(self, mode: int = 0o777) -> None:
        """Create the netspy directory"""
        self.netspy_dir.mkdir(mode=mode, exist_ok=True)

    @validator("core_nlp_dir")
    def set_env_vars(cls, v) -> None:

        os.environ["CORENLP_HOME"] = str(v)

    @validator("nltk_dir")
    def set_nltk_dir(cls, v):
        nltk.data.path.append(str(v))
        return v

    def clear_corenlp_env(self) -> None:

        del os.environ["CORENLP_HOME"]

    class Config:
        # pylint: disable=R0903
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:

    settings = Settings()
    return settings
