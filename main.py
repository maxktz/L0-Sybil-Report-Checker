import asyncio
import datetime
from src.sybil_checker import get_all_sybil_addresses
from src.utils import write_sybil_addresses_to_file
from src.core.config import settings
from src.core.loader import telegram_client
from src.logger import logger


DELAY = 5 * 60  # 5 minutes


async def main():
    async with telegram_client:
        pass

    while True:
        addrs = await get_all_sybil_addresses()

        issue_numbers = []
        for nums in addrs.values():
            for num in nums:
                if num not in issue_numbers:
                    issue_numbers.append(num)
        highest_issue_number = issue_numbers[0]
        non_empty_issues = len(issue_numbers)

        path_to_file = write_sybil_addresses_to_file(addrs)

        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        text = f"""<b>{now} UTC</b>
        
Unique addresses: {len(addrs)}
Issues: {highest_issue_number}
Non-empty issues: {non_empty_issues}"""

        logger.info("Sending file to chat")
        async with telegram_client:
            await telegram_client.send_file(
                entity=settings.CHAT_ID_TO_SEND,
                file=path_to_file,
                caption=text,
                parse_mode="HTML",
            )
        logger.success("Sent message, sleeping delay")
        await asyncio.sleep(DELAY)


if __name__ == "__main__":
    asyncio.run(main())
