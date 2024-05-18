import asyncio

from pymongo import ReplaceOne, UpdateOne
from src.github_client.client import GithubClient
from src.settings import settings
from src.database.init import database


async def main():
    g = GithubClient(
        user_agent=settings.GITHUB_USER_AGENT,
        auth_token=settings.GITHUB_ACCESS_TOKEN,
    )
    # await init_db()
    # res, pg = await g.get_issues("LayerZero-Labs", "sybil-report", per_page=1)
    page = 1
    while True:
        issues, pages = await g.get_issues(
            "LayerZero-Labs",
            "sybil-report",
            page=page,
            per_page=100,
        )

        for _, issue in issues.items():
            issue["_id"] = issue["id"]
            del issue["id"]
        operations = [
            ReplaceOne(
                {"_id": doc["_id"]},
                replacement=doc,
                upsert=True,
            )
            for _, doc in issues.items()
        ]

        await database.reports.bulk_write(operations)
        if pages["last"] <= page:
            break
        page += 1
    # return all_issues


if __name__ == "__main__":
    asyncio.run(main())
