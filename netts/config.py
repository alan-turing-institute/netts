import os
from pathlib import Path
from typing import TYPE_CHECKING, Union

import nltk
from pydantic import BaseSettings, validator

from netts import config_file

if TYPE_CHECKING:
    HttpUrl = str
else:
    from pydantic import HttpUrl

HOME_DIR = Path.home()
NETTS_DIR = HOME_DIR / "netts"


class Settings(BaseSettings):

    netts_dir: Path = NETTS_DIR
    openie_url: HttpUrl = (
        "https://drive.google.com/uc?id=19z8LO-CYOfJfV5agm82PZ2JNWNUPIB6D"
    )
    openie_language_url: HttpUrl = (
        "https://drive.google.com/uc?id=0B-5EkZMOlIt2cFdjYUJZdGxSREU&resourcekey=0-X_oNJ6r24s_anMGbKKRdQw"
    )
    # You can pass a Path or str to the config file and the validator will load it as config_file.Config
    netts_config: config_file.Config = config_file.Config()

    @property
    def nltk_dir(self) -> Path:
        return self.netts_dir / "nltk_data"

    @property
    def core_nlp_dir(self) -> Path:
        return self.netts_dir / "stanza_corenlp"

    @property
    def openie_dir(self) -> Path:
        return self.netts_dir / "openie"

    @property
    def openie(self) -> Path:
        return self.openie_dir / "openie-assembly-5.0-SNAPSHOT.jar"

    @property
    def openie_data(self) -> Path:

        return self.openie_dir / "data"

    @property
    def openie_language_model(self) -> Path:
        return self.openie_data / "languageModel"

    def mk_netts_dir(self, mode: int = 0o777) -> None:
        """Create the netts directory"""
        self.netts_dir.mkdir(mode=mode, exist_ok=True)

    @validator("netts_dir", pre=True)
    def validate_netts_dir(cls, v: str) -> Path:

        direc = Path(v) / "stanza_corenlp"
        os.environ["CORENLP_HOME"] = str(direc)

        nltk_dir = Path(v) / "nltk_data"
        nltk.data.path.append(str(nltk_dir))
        return Path(v)

    @validator("netts_config", pre=True)
    def load_config_from_file(
        cls, v: Union[str, Path, config_file.Config]
    ) -> config_file.Config:

        if isinstance(v, config_file.Config):
            return v

        config_file_path = Path(v)
        default_file_path = Path("netts.toml")

        if not (config_file_path.exists() or default_file_path.exists()):
            raise IOError("Could not find config_file")

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
