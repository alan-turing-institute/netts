from pydantic import BaseSettings
from pathlib import Path

from functools import lru_cache

HOME_DIR = Path.home()
NETSPY_DIR = HOME_DIR / "netspy"

class Settings(BaseSettings):

    netspy_dir: Path = NETSPY_DIR

    @property
    def nltk_dir(self):
        return self.netspy_dir / "nltk_data"

    @property
    def core_nlp_dir(self):
        return self.core_nlp_dir / "stanza_corenlp"

    def mk_netspy_dir(self):
        """Create the netspy directory
        """
        self.netspy_dir.mkdir(mode = 0o777, exist_ok=True)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

@lru_cache()
def get_settings() -> Settings:

    return Settings()