from typing import Union
from openai import AsyncAzureOpenAI
from pydantic_ai_bedrock.bedrock import BedrockModel
from pydantic_ai.models.openai import OpenAIModel
from .config import MODEL_CONFIG, AZURE_CONFIG
from pprint import pprint
pprint(MODEL_CONFIG)

def get_model(selected_model: str) -> Union[BedrockModel, OpenAIModel]:
    """
    Factory function to create and return the appropriate model instance.
    
    Args:
        selected_model: String identifier for the model to use
        
    Returns:
        An instance of either BedrockModel or OpenAIModel
    """
    if 'bedrock' in selected_model:
        return BedrockModel(
            model_name=MODEL_CONFIG['models'][selected_model],
            region_name=MODEL_CONFIG['bedrock']['region']
        )
    elif 'azure' in selected_model:
        client = AsyncAzureOpenAI(
            api_key=AZURE_CONFIG['api_key'],
            api_version=AZURE_CONFIG['api_version'],
            azure_endpoint=AZURE_CONFIG['api_endpoint']
        )
        return OpenAIModel(   
            model_name=AZURE_CONFIG['deployment'],
            openai_client=client
        )
    raise ValueError(f"Unsupported model type: {selected_model}") 