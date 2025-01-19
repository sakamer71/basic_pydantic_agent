from datetime import datetime
import subprocess
import platform
from typing import Dict, Any

class ChatTools:
    @staticmethod
    def tell_date() -> str:
        """Return the current date"""
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def get_os_info() -> Dict[str, str]:
        """Determine the operating system and version"""
        os_name = platform.system()
        os_version = platform.version()
        os_release = platform.release()
        
        return {
            "system": os_name,
            "version": os_version, 
            "release": os_release,
            "full": f"{os_name} {os_release} ({os_version})"
        }

    @staticmethod
    def run_os_command(command: str) -> Dict[str, Any]:
        """Execute a non-interactive OS command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
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

    @staticmethod
    def format_command_output(command: str, result: Dict[str, Any]) -> str:
        """Format command output with colors and formatting"""
        BLUE = '\033[94m'
        GREEN = '\033[92m' 
        RED = '\033[91m'
        BOLD = '\033[1m'
        END = '\033[0m'
        
        formatted_output = f"\n{BOLD}$ {command}{END}\n"
        formatted_output += "─" * 80 + "\n"
        
        if result["success"]:
            if result["output"].strip():
                indented_output = "\n".join(f"  {line}" for line in result["output"].splitlines())
                formatted_output += f"{GREEN}{indented_output}{END}\n"
            else:
                formatted_output += f"{GREEN}Command completed successfully with no output{END}\n"
        else:
            formatted_output += f"{RED}Command failed with return code {result['return_code']}{END}\n"
            if result["output"].strip():
                indented_output = "\n".join(f"  {line}" for line in result["output"].splitlines())
                formatted_output += f"{RED}{indented_output}{END}\n"
                
        formatted_output += "─" * 80 + "\n"
        return formatted_output 