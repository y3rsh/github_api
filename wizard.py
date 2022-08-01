""""""
import os
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from util import LOG_FILE_PATH


class Wizard:
    """Reusable CLI interactions"""

    def __init__(self, console: Optional[Console]) -> None:
        if console:
            self.console = console
        else:
            self.console = Console()

    def get_owner(self, owner: Optional[str] = None) -> str:
        if owner == "" or owner is None:
            owner = Prompt.ask(
                "What is [i]your[/i] [bold red]repo owner[/] (most likely it is Opentrons and you can just hit enter) ?",
                console=self.console,
                default="Opentrons",
                show_default=False,
            )
        return owner

    def get_repo(self, repo: Optional[str] = None) -> str:
        if repo == "" or repo is None:
            repo = Prompt.ask(
                "What is [i]your[/i] [bold red]repo[/] (most likely it is opentrons and you can just hit enter) ?",
                console=self.console,
                default="opentrons",
                show_default=False,
            )
        return repo

    def get_token(self, token: Optional[str] = None) -> str:
        if token == "" or token is None:
            token = Prompt.ask(
                "What is [i]your[/i] [bold red]Github personal access token[/] ?",
                console=self.console,
            )
        return token

    def reset_log(self) -> bool:
        """Reset the log file."""
        response = Confirm.ask(f"Would you like to reset the log file {LOG_FILE_PATH}?")
        if response:
            if os.path.exists(LOG_FILE_PATH):
                os.remove(LOG_FILE_PATH)
                self.console.print(
                    Panel(
                        f"Removed log file {LOG_FILE_PATH}",
                        style="bold magenta",
                    )
                )
            return True
        return False
