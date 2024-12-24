import os
import requests
import json
from typing import Dict, Any, List
from dotenv import load_dotenv

from app.config.local_files_config.local_files import LOGS_DIR
from app.utils.formatted_date_util import formatted_datetime
from app.utils.logs_util import save_response_to_log

load_dotenv(verbose=True)

API_KEY = os.environ['NEWSAPI_API_KEY']
BASE_URL = "https://eventregistry.org/api/v1/article/getArticles"
DEFAULT_PARAMS = {
    "action": "getArticles",
    "keyword": "terror attack",
    "ignoreSourceGroupUri": "paywall/paywalled_sources",
    "articlesPage": 1,
    "articlesCount": 2,
    "articlesSortBy": "socialScore",
    "articlesSortByAsc": False,
    "dataType": ["news", "pr"],
    "forceMaxDataTimeWindow": 31,
    "resultType": "articles",
    "apiKey": API_KEY,
}


def fetch_news_data(page: int) -> List[Dict[str, Any]]:
    params = DEFAULT_PARAMS.copy()
    params["articlesPage"] = page
    try:
        response = requests.post(BASE_URL, json=params)
        response.raise_for_status()
        response_data = response.json()
        save_response_to_log(response_data, page)
        return response_data.get("articles", {}).get("results", [])
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
