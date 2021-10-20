import datetime
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

import typer


# pylint: disable=C0103
@dataclass
class Color:
    text: str
    fg: Optional[str] = None
    bg: Optional[str] = None
    bold: bool = False
    underline: bool = False
    blink: bool = False

    def dict(self) -> Dict[Any, Any]:
        return self.__dict__


def cprint(*args: Union[Color, str, List[Union[Color, str]]]) -> None:

    all_text = args
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output = typer.style(f"{time} Netspy") + ": "

    for text in all_text:
        if isinstance(text, str):
            output += text
        elif isinstance(text, Color):
            output += typer.style(**text.dict())
        else:
            raise TypeError("Must be str of Color")

    typer.echo(output)
