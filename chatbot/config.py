from typing import Dict, Any
from pathlib import Path
import yaml
from dotenv import load_dotenv
import os
from pprint import pprint
# Get the package root directory
PACKAGE_ROOT = Path(__file__).parent
CONFIG_DIR = PACKAGE_ROOT / "config"

def load_yaml_config(filename: str) -> Dict[str, Any]:
    """Load a YAML configuration file"""
    config_path = CONFIG_DIR / filename
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# Load configurations
MODEL_CONFIG = load_yaml_config("models.yaml")
PROMPT_CONFIG = load_yaml_config("prompts.yaml")
pprint(MODEL_CONFIG)

# Command execution settings
COMMAND_TIMEOUT = 30

# Load environment variables
load_dotenv()

# Azure configurations
AZURE_CONFIG = {
    'api_key': os.getenv('AZURE_OPENAI_API_KEY'),
    'api_endpoint': os.getenv('AZURE_OPENAI_ENDPOINT'),
    'api_version': os.getenv('AZURE_OPENAI_API_VERSION'),
    'deployment': os.getenv('AZURE_OPENAI_DEPLOYMENT')
}

# Export commonly used configurations
MODELS = MODEL_CONFIG['models']
pprint(MODELS)
SYSTEM_PROMPTS = PROMPT_CONFIG['system_prompts']
TOOL_DESCRIPTIONS = PROMPT_CONFIG['tool_descriptions'] 