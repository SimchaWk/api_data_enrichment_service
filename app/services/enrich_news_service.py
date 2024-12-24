from datetime import datetime
from typing import List, Dict, Optional, Any

from app.config.kafka_config.producer import produce_batch
from app.models.terror_event import TerrorEvent
from app.services.news_classifier_service import classify_text
from app.services.geocode_location_service import get_coordinates
from app.api.fetch_news_api import fetch_news_data




def process_single_article(article: Dict[str, Any]) -> Optional[TerrorEvent]:
    try:
        body = article.get('body', '')
        date_time = article.get('dateTime', '')

        if not all([body, date_time]):
            return None

        classification = classify_text(body)
        if not classification['is_terrorism']:
            return None

        location_data = get_coordinates(body)

        return TerrorEvent(
            event_date=datetime.fromisoformat(date_time.replace('Z', '+00:00')),
            country=location_data['address'].split(',')[-1].strip() if location_data else None,
            city=location_data['address'].split(',')[0].strip() if location_data else None,
            latitude=location_data['lat'] if location_data else None,
            longitude=location_data['lon'] if location_data else None,
            description=body,
            data_source='NewsAPI'
        )

    except Exception as e:
        print(f"Error processing article: {e}")
        return None


def process_news_batch(page: int) -> List[TerrorEvent]:
    articles = fetch_news_data(page)
    return [event for article in articles
            if (event := process_single_article(article)) is not None]


def publish_terror_events(events: List[TerrorEvent]) -> None:
    if not events:
        return

    event_dicts = [
        {
            **event.model_dump(),
            'event_date': event.event_date.isoformat()
        }
        for event in events
    ]
    produce_batch(messages=event_dicts)
