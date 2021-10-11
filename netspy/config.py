import os
from pathlib import Path
from typing import TYPE_CHECKING, Optional

import nltk
from pydantic import BaseSettings, ValidationError, validator

import netspy.config_file as config_file

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
    # You can pass a Path or str to the config file and the validator will load it as config_file.Config
    netspy_config: Optional[config_file.Config]

    @property
    def nltk_dir(self) -> Path:
        return self.netspy_dir / "nltk_data"

    @property
    def core_nlp_dir(self) -> Path:
        return self.netspy_dir / "stanza_corenlp"

    @property
    def openie_dir(self) -> Path:
        return self.netspy_dir / "openie"

    @property
    def openie(self) -> Path:
        return self.openie_dir / "openie-assembly-5.0-SNAPSHOT.jar"

    @property
    def openie_data(self) -> Path:

        return self.openie_dir / "data"

    @property
    def openie_language_model(self) -> Path:
        return self.openie_data / "languageModel"

    def mk_netspy_dir(self, mode: int = 0o777) -> None:
        """Create the netspy directory"""
        self.netspy_dir.mkdir(mode=mode, exist_ok=True)

    @validator("netspy_dir", pre=True)
    def validate_netspy_dir(cls, v: str) -> Path:
        direc = Path(v) / "stanza_corenlp"
        os.environ["CORENLP_HOME"] = str(direc)

        nltk_dir = Path(v) / "nltk_data"
        nltk.data.path.append(str(nltk_dir))
        return v

    @validator("netspy_config", pre=True)
    def load_config_from_file(cls, v):

        if not v:
            return config_file.Config()

        config_file_path = Path(v)
        default_file_path = Path("netspy.toml")

        if not config_file_path.exists() or not default_file_path.exists():
            raise ValidationError("Could not fine config_file")

        return (
            config_file.Config.load(config_file_path)
            if config_file_path.exists()
            else config_file.Config.load(default_file_path)
        )

    class Config:
        # pylint: disable=R0903
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:

    settings = Settings()
    return settings
