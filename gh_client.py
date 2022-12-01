from __future__ import annotations

import concurrent.futures
import contextlib
from typing import AsyncGenerator

import httpx
from httpx import Response

STARTUP_WAIT = 15
SHUTDOWN_WAIT = 15


class GhClient:
    """Client for gh API."""

    def __init__(
        self,
        httpx_client: httpx.AsyncClient,
        worker_executor: concurrent.futures.ThreadPoolExecutor,
        owner: str,
        repo: str,
    ) -> None:
        """Initialize the client."""
        self.base_url: str = f"https://api.github.com/repos/{owner}/{repo}"
        self.httpx_client: httpx.AsyncClient = httpx_client
        self.worker_executor: concurrent.futures.ThreadPoolExecutor = worker_executor

    @staticmethod
    @contextlib.asynccontextmanager
    async def make(
        owner: str, repo: str, token: str
    ) -> AsyncGenerator[GhClient, None]:
        with concurrent.futures.ThreadPoolExecutor() as worker_executor:
            async with httpx.AsyncClient(
                headers={
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"token {token}",
                }
            ) as httpx_client:
                yield GhClient(
                    httpx_client=httpx_client,
                    worker_executor=worker_executor,
                    owner=owner,
                    repo=repo,
                )

    async def get_runs(self, branch: str, per_page: int = 100) -> Response:
        """GET /actions/runs"""
        response = await self.httpx_client.get(
            url=f"{self.base_url}/actions/runs",
            params={
                "exclude_pull_requests": True,
                "per_page": per_page,
                "branch": branch,
            },
        )
        return response
