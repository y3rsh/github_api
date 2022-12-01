import asyncio
import os

from httpx import Response
from rich.console import Console
from rich.theme import Theme

from gh_client import GhClient
from util import log_response
from wizard import Wizard


async def stuff(owner: str, repo: str, token: str) -> None:
    """Do some stuff with the API client or whatever."""
    async with GhClient.make(owner=owner, repo=repo, token=token) as gh_client:
        head_branch = "edge"
        resp = await gh_client.get_runs(branch=head_branch)
        await log_response(resp, console=console)
        runs = resp.json()["workflow_runs"]
        just_builds = [
            run
            for run in runs
            if run["name"] == "App test, build, and deploy"
            and run["conclusion"] == "success"
            and run["event"] == "push"
            and run["head_branch"] == head_branch
            #and ["run_number"] == 10658
        ]
        #console.print(just_builds[:5])
        # responses are in latest first order, use 0
        console.print(just_builds[0])
        sha = just_builds[0]["head_sha"]  # what to checkout
        console.print(sha)
        run_number = just_builds[0][
            "run_number"
        ]  # 6.0 https://s3.amazonaws.com/opentrons-app/builds/Opentrons-v6.0.0-linux-b20264.AppImage  + 10000
        console.print(f"run number is {run_number}")
        link = f"https://s3.amazonaws.com/opentrons-app/builds/Opentrons-v6.1.0-win-b{int(run_number)+10000}-edge.exe"
        console.print(f"the link = {link}")


if __name__ == "__main__":
    custom_theme = Theme(
        {"info": "dim cyan", "warning": "magenta", "danger": "bold red"}
    )
    console = Console(theme=custom_theme)
    wizard = Wizard(console)
    owner = wizard.get_owner()
    repo = wizard.get_repo()
    token = wizard.get_token(os.getenv("GH_TOKEN", None))
    wizard.reset_log()
    asyncio.run(stuff(owner=owner, repo=repo, token=token))
