from netspy.config import get_settings, Settings
import shutil

def test_config_dir(tmp_path):

    settings = get_settings()

    # If netspy_dir exists then use a tmp directory
    if settings.netspy_dir.exists():
        settings = Settings(netspy_dir = tmp_path)

    # Create directory and clean up after
    try:
        settings.mk_netspy_dir()
        assert settings.netspy_dir.exists()
    finally:
        settings.netspy_dir.rmdir()
        assert not settings.netspy_dir.exists()