from datetime import datetime
from pydantic_ai import Agent
from pydantic_ai_bedrock.bedrock import BedrockModel, BedrockAgentModel
from pydantic_ai.models.openai import OpenAIModel

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
import subprocess
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv
import os


models = {
    'bedrock-claude-35-haiku': 'us.anthropic.claude-3-5-haiku-20241022-v1:0',
    'bedrock-claude-35-sonnet-v2': 'us.anthropic.claude-3-5-sonnet-20241022-v2:0',
    'bedrock-nova-micro': 'us.amazon.nova-micro-v1:0', 
    'bedrock-nova-lite': 'us.amazon.nova-lite-v1:0',
    'bedrock-nova-pro': 'us.amazon.nova-pro-v1:0',
    'azure-gpt4o': 'new-gpt-4o'
}

def get_model(selected_model):
    if 'bedrock' in selected_model:
        model = BedrockModel(
        model_name=models['claude-35-haiku'],
        region_name='us-east-2'
    )
    elif 'azure' in selected_model:
        load_dotenv()
        api_key = os.getenv('AZURE_OPENAI_API_KEY')
        api_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        api_version = os.getenv('AZURE_OPENAI_API_VERSION')
        model = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        
        client = AsyncAzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=api_endpoint
        )
        model = OpenAIModel(   
            model_name=model,
            openai_client=client
        )
    return model

def setup_agent(model):
    agent = Agent(model=model,
                system_prompt='You are very helpful and answer questions concisely',
                )
    return agent


model = get_model('azure-gpt4o')
agent = setup_agent(model)

@agent.tool_plain
def tell_date():
    """Function to tell the current date"""
    return datetime.now().strftime("%Y-%m-%d")

# @agent.tool_plain
# def list_packages():
#     """Function to list installed packages on Ubuntu"""
#     import subprocess
#     try:
#         result = subprocess.run(['apt', 'list', '--installed'], 
#                               capture_output=True, 
#                               text=True, 
#                               check=True)
#         return result.stdout
#     except subprocess.CalledProcessError as e:
#         return f"Error listing packages: {str(e)}"

@agent.tool_plain
def get_os_info():
    """Function to determine the operating system and version"""
    import platform
    
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()
    
    return {
        "system": os_name,
        "version": os_version, 
        "release": os_release,
        "full": f"{os_name} {os_release} ({os_version})"
    }

@agent.tool_plain
def run_os_command(command):
    """Execute a non-interactive OS command and return its output.  
        Ensure the command is appropriate for the operating system.
       If the comand requires sudo, attempt it before telling the user that they need sudo permissions.
       If the command output offers evidence for your answer, provide the evidence in your response.
       ie. if the question is "Is there a c compiler installed on my machine?", and the command output is "gcc is installed", then provide the evidence in your response.
       """
    try:
        # Run command and capture output
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30  # Timeout after 30 seconds
        )
        
        # Combine stdout and stderr
        output = result.stdout
        if result.stderr:
            output += "\nErrors:\n" + result.stderr
            
        return {
            "output": output,
            "return_code": result.returncode,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            "output": "Command timed out after 30 seconds",
            "return_code": -1,
            "success": False
        }
    except Exception as e:
        return {
            "output": f"Error executing command: {str(e)}",
            "return_code": -1,
            "success": False
        }

@agent.tool_plain
def format_command_output(command, result):
    """Format command and its output using ASCII color codes and formatting"""
    # ANSI color codes
    BLUE = '\033[94m'
    GREEN = '\033[92m' 
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'
    
    # Format the command
    formatted_output = f"\n{BOLD}$ {command}{END}\n"
    
    # Add a divider
    formatted_output += "─" * 80 + "\n"
    
    if result["success"]:
        # Command succeeded
        if result["output"].strip():
            # Add some indentation to the output
            indented_output = "\n".join(f"  {line}" for line in result["output"].splitlines())
            formatted_output += f"{GREEN}{indented_output}{END}\n"
        else:
            formatted_output += f"{GREEN}Command completed successfully with no output{END}\n"
    else:
        # Command failed
        formatted_output += f"{RED}Command failed with return code {result['return_code']}{END}\n"
        if result["output"].strip():
            # Add some indentation to the output
            indented_output = "\n".join(f"  {line}" for line in result["output"].splitlines())
            formatted_output += f"{RED}{indented_output}{END}\n"
            
    # Add a final divider
    formatted_output += "─" * 80 + "\n"
    
    return formatted_output


user_msg = 'Hello!'
result = agent.run_sync(user_msg)
print(f'\n\n{result.data}\n\n')

while True:
    user_msg = input("Enter your message: ")
    result = agent.run_sync(user_msg, message_history=result.all_messages())
    print(result.data)


# response = agent.run_sync(" Is there a c compiler installed on my machine?")
# print(response.data)
