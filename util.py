
import json

import time

from anyio import to_thread
from httpx import Response
from rich.console import Console

LOG_FILE_PATH = "responses.log"

async def log_response(response: Response, print_timing: bool = False, console: Console = Console()) -> None:
    """Log the response status, url, timing, and json response."""
    endpoint = f"\nstatus_code = {response.status_code}\n{response.request.method} {response.url}"  # noqa: E501
    formatted_response_body = json.dumps(response.json(), indent=4)
    elapsed = response.elapsed.total_seconds()
    elapsed_output = str(elapsed)
    if elapsed > 1:
        elapsed_output = f"{str(elapsed)} *LONG*"
    if print_timing:
        console.print(endpoint)
        console.print(elapsed_output)
        # console.print(formatted_response_body) # too big to do in console usefully
    with open(LOG_FILE_PATH, "a") as log:
        log.write(str(time.time_ns()))
        log.write(endpoint)
        log.write("\n")
        log.write(elapsed_output)
        log.write(formatted_response_body)
        log.write("\n____________________________________\n")
