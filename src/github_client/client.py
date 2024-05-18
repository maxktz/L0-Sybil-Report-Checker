import re

import msgspec
from curl_cffi.requests import AsyncSession, Response
from yarl import URL

from .types import Issue, IssuesFilter, PageNumbers


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
        username: str,
        repository: str,
        filter_: IssuesFilter = "all",
        page: int = 1,
        per_page: int = 30,
        **kwargs,
    ) -> tuple[dict[int, Issue], PageNumbers]:
        """does not contain all available parameters, see
        https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28

        Args:
            username (str)
            repository (str)
            filter_ (str): Defaults to "all".
            page (int, optional): Defaults to 1.
            per_page (int, optional): <=100, Defaults to 30, max is 100.

        Returns:
            tuple[dict[int, Issue], PageNumbers]
        """
        url = URL(f"https://api.github.com/repos/{username}/{repository}/issues")
        url.update_query(
            {
                **kwargs,
                "filter": filter_,
                "page": page,
                "per_page": per_page,
            }
        )
        response = await self._get_request(url)
        results = msgspec.json.decode(response.text)
        issues = {r["number"]: Issue(r) for r in results}
        page_nums = {
            re.search(r'rel="(.+?)"', s).group(1): int(re.search(r"page=(\d+)", s).group(1))
            for s in response.headers["Link"].split(",")
        }
        page_nums["next"] = page + 1 if page_nums.get("last") else None
        page_nums["last"] = page_nums.get("last", page)
        return issues, PageNumbers(page_nums)

    async def get_all_issues(
        self,
        username: str,
        repository: str,
        filter_: IssuesFilter = "all",
    ) -> dict[int, Issue]:
        all_issues = {}
        next_page = 1
        while next_page is not None:
            issues, pages = await self.get_issues(
                username=username,
                repository=repository,
                page=next_page,
                filter_=filter_,
                per_page=100,
            )
            all_issues.update(issues)
            next_page = pages.get("next")
        return all_issues
