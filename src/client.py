import re
import orjson

from curl_cffi.requests import AsyncSession, Response
from yarl import URL

from .types import Issue, IssuesFilter


class GithubClient:

    def __init__(self, user_agent: str, auth_token: str):
        self.headers = {
            "User-Agent": user_agent,
            "Authorization": "Bearer " + auth_token.strip(),
            "X-GitHub-Api-Version": "2022-11-28",
        }

    async def _get_request(self, url: str | URL) -> Response:
        async with AsyncSession() as session:
            return await session.get(str(url), headers=self.headers)

    async def get_issues(
        self,
        repository: str,
        filter_: IssuesFilter = "all",
        page: int = 1,
        per_page: int = 30,
        **kwargs,
    ) -> tuple[dict[int, Issue], int]:
        """does not contain all available parameters, see
        https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28

        Args:
            repository (str) example: "LayerZero-Labs/sybil-report"
            filter_ (str): Defaults to "all".
            page (int, optional): Defaults to 1.
            per_page (int, optional): <=100, Defaults to 30, max is 100.

        Returns:
            tuple[dict[int, Issue], int]
        """
        url = URL(f"https://api.github.com/repos/{repository}/issues").with_query(
            {
                **kwargs,
                "filter": filter_,
                "page": page,
                "per_page": per_page,
            }
        )
        response = await self._get_request(url)
        results = orjson.loads(response.text)
        issues = {r["number"]: Issue(r) for r in results}
        page_nums = {
            re.search(r'rel="(.+?)"', s).group(1): int(re.search(r"page=(\d+)", s).group(1))
            for s in response.headers["Link"].split(",")
        }
        last_page = page_nums.get("last", page)
        return issues, last_page

    async def get_all_issues(
        self,
        repository: str,
        filter_: IssuesFilter = "all",
    ) -> dict[int, Issue]:
        all_issues = {}
        next_page = 1
        while True:
            issues, last_page = await self.get_issues(
                repository=repository,
                page=next_page,
                filter_=filter_,
                per_page=100,
            )
            next_page += 1
            if next_page > last_page:
                break
            all_issues.update(issues)
        return all_issues
