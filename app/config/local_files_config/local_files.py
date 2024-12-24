from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent

load_dotenv(PROJECT_ROOT / '.env')

LOGS_DIR = PROJECT_ROOT / 'data' / 'fetch_logs'

if __name__ == '__main__':
    print(LOGS_DIR)
