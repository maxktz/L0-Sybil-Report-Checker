import re
from pathlib import Path
from src.cache.serialization import JSONSerializer
from src.core.loader import github_client, redis_client
from src.logger import logger
from cachetools import TTLCache, cached


SybilAddresses = dict[str, list[int]]
"""[Address: IssueNumber]"""
addresses_cache = TTLCache(maxsize=10_000, ttl=60)  # 1 minute memory cache


async def get_addresses_on_page(page: int) -> SybilAddresses:
    cache_time = 60 * 60  # one hour
    key = f"sybil_checker/get_addresses_on_page:{page}"
    cached = await redis_client.get(key)
    if cached is not None:
        return JSONSerializer.deserialize(cached)

    logger.info(f"getting issues on page {page}")
    issues, last_page = await github_client.get_issues(
        repository="LayerZero-Labs/sybil-report",
        page=page,
        per_page=100,
        direction="asc",
        filter_="all",
    )
    logger.info(f"got {len(issues)} issues on page {page}")
    addresses: SybilAddresses = {}
    for issue_number, issue in issues.items():
        if not issue.get("body"):
            continue

        # find block with address in issue body
        block = issue["body"].lower().split("description", 1)[0]

        # find all ethereum addresses in the block
        addrs: str[str] = set(re.findall(r"\b0x[a-fA-F0-9]{40}\b", block))

        # add to addresses with issue number it's from
        logger.success(f"got {len(addrs)} addresses from issue #{issue_number} on page {page}")
        for addr in addrs:
            addresses[addr] = addresses.get(addr, []) + [issue_number]
    if len(issues) == 100:
        value = JSONSerializer.serialize(addresses)
        await redis_client.set(key, value, ex=cache_time)
    return addresses


@cached(addresses_cache)
async def get_all_sybil_addresses() -> SybilAddresses:
    logger.info("getting all sybil addresses")
    all_adderesses: SybilAddresses = {}
    next_page = 1
    while True:
        addresess = await get_addresses_on_page(page=next_page)
        if not addresess:
            break
        for addr, issue_numbers in addresess.items():
            all_adderesses[addr] = all_adderesses.get(addr, []) + issue_numbers
            all_adderesses[addr] = list(sorted(all_adderesses[addr], reverse=True))
        next_page += 1
    logger.info(f"got all sybil addresses: {len(all_adderesses)}")
    all_adderesses = dict(sorted(all_adderesses.items(), key=lambda x: x[1], reverse=True))
    return all_adderesses
