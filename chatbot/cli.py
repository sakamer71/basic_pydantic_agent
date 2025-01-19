from typing import Optional
from chatbot.models import get_model
from chatbot.agent import ChatAgent
from chatbot.config import MODEL_CONFIG

class ChatCLI:
    def __init__(self, model_name: str = None):
        # Use the default model if none specified
        model_name = model_name or MODEL_CONFIG['default_model']
        model = get_model(model_name)
        self.agent = ChatAgent(model)
        self.context = None

    def start(self):
        """Start the CLI chat interface"""
        print("Chat initialized. Type 'exit' to quit.")
        self.context = self.agent.chat("Hello!")
        print(f"\n{self.context.data}\n")

        while True:
            try:
                user_msg = input("-----------------------------------\n\nEnter your message: ").strip()
                if user_msg.lower() in ['exit', 'quit']:
                    break
                    
                self.context = self.agent.chat(user_msg, self.context)
                print(self.context.data)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")

def main():
    cli = ChatCLI()
    cli.start()

if __name__ == "__main__":
    main() 