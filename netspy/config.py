from typing import Optional
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings

HOME_DIR = Path.home()
NETSPY_DIR = HOME_DIR / "netspy"


class Settings(BaseSettings):

    netspy_dir: Path = NETSPY_DIR

    @property
    def nltk_dir(self):
        return self.netspy_dir / "nltk_data"

    @property
    def core_nlp_dir(self):
        return self.netspy_dir / "stanza_corenlp"

    def mk_netspy_dir(self):
        """Create the netspy directory"""
        self.netspy_dir.mkdir(mode=0o777, exist_ok=True)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings(netspy_dir: Optional[Path] = None) -> Settings:
    if netspy_dir:
        return Settings(netspy_dir = netspy_dir)
    return Settings()