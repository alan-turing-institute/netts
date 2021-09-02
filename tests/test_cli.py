from typer.testing import CliRunner

from netspy.cli import app

runner = CliRunner()


# def test_install() -> None:
#     result = runner.invoke(app, ["install"])
#     assert result.exit_code == 0
