from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Union

from pydantic import BaseSettings

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

    class Config:
        # pylint: disable=R0903
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings(netspy_dir: Optional[Union[str, Path]] = None) -> Settings:

    if netspy_dir:
        settings = Settings(netspy_dir=netspy_dir)
    else:
        settings = Settings()
    return settings
