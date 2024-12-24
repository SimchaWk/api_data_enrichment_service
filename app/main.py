import asyncio
from app.services.enrich_news_service import process_news_batch, publish_terror_events


async def run_news_processor(interval_seconds: int = 120) -> None:
    current_page = 1

    while True:
        try:
            events = process_news_batch(current_page)
            publish_terror_events(events)

            current_page = current_page + 1 if events else 1

        except Exception as e:
            print(f"Error in processing batch: {e}")
            current_page = 1

        await asyncio.sleep(interval_seconds)


if __name__ == "__main__":
    asyncio.run(
        run_news_processor(interval_seconds=120)
    )
