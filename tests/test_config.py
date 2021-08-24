import shutil

from netspy.config import NETSPY_DIR, Settings, get_settings


def test_show_home_dir():

    if not NETSPY_DIR.exists():
        NETSPY_DIR.mkdir(mode=0o777)
        assert NETSPY_DIR.exists()
        print(f"Pytest created Netspy directory: {NETSPY_DIR}")
        NETSPY_DIR.rmdir()
        assert not NETSPY_DIR.exists()


def test_config_dir(tmp_path):

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
