"""Configuration for TA-GraphRAG experiments."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"

# DeepSeek API
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# Experiment defaults
TOP_K_RETRIEVAL = 5
TRUST_THRESHOLD = 0.7
MAX_ITERATIONS = 3
SAMPLE_SIZE = 500  # for full experiment
TEST_SIZE = 10     # for quick testing
