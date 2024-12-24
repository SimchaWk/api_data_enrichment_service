import json
from typing import Dict, Any

from app.config.local_files_config.local_files import LOGS_DIR
from app.utils.formatted_date_util import formatted_datetime


def save_response_to_log(response: Dict[str, Any], page: int):
    """
    Saves the API response to a log file in JSON format.
    Each page will have its own log file.
    """
    log_file = LOGS_DIR / f"news_api_page_{page}_{formatted_datetime()}.json"
    try:
        with open(log_file, "w", encoding="utf-8") as file:
            json.dump(response, file, indent=4, ensure_ascii=False)
        print(f"Response saved to {log_file}")
    except Exception as e:
        print(f"Error saving response to log: {e}")
