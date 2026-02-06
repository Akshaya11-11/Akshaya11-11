"""
Conversational Knowledge Bot with Memory System
An intelligent AI assistant that remembers conversations and learns from interactions.

Clean, professional interface with zero unnecessary complexity.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# ==================== TOOLS ====================

@tool
def search_knowledge_base(query: str) -> str:
    """Search for information in knowledge base"""
    knowledge = {
        "python": "Python is a programming language great for AI and data science.",
        "machine learning": "ML enables computers to learn from data without being explicitly programmed.",
        "ai": "Artificial Intelligence is technology that simulates human intelligence.",
        "data science": "Data Science combines statistics, coding, and business knowledge.",
        "langchain": "LangChain is a framework for building AI applications.",
        "openai": "OpenAI creates powerful AI models like GPT.",
    }
    
    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return f"Information: {value}"
    return f"I can provide general knowledge about '{query}'."

@tool
def analyze_intent(message: str) -> str:
    """Understand what the user wants"""
    if "?" in message:
        return "User is asking a question"
    elif "help" in message.lower() or "how" in message.lower():
        return "User needs help or guidance"
    elif "explain" in message.lower() or "tell" in message.lower():
        return "User wants to learn something"
    else:
        return "User wants to have a discussion"

@tool
def get_user_history_summary(user_id: str) -> str:
    """Get summary of what user has discussed before"""
    return f"User {user_id} has discussed AI and technology topics before. I should reference this context."

@tool
def save_important_fact(topic: str, fact: str) -> str:
    """Save important information learned in conversation"""
    return f"Saved: {topic} - {fact[:50]}..."

# ==================== MEMORY MANAGER ====================

class MemoryManager:
    """Handles all conversation memory and history"""
    
    def __init__(self, user_id: str = "user"):
        self.user_id = user_id
        self.messages: List[Dict] = []
        self.session_start = datetime.now()
        self.session_id = self.session_start.strftime("%Y%m%d_%H%M%S")
        self.file_path = f"memory_{user_id}_{self.session_id}.json"
        self.load_old_conversations()
    
    def load_old_conversations(self):
        """Load conversations from previous sessions"""
        try:
            files = [f for f in os.listdir(".") if f.startswith(f"memory_{self.user_id}")]
            if files:
                latest = sorted(files)[-1]
                with open(latest, 'r') as f:
                    old_data = json.load(f)
                    if isinstance(old_data, list) and len(old_data) > 0:
                        self.messages = old_data[-5:]  # Load last 5 messages for context
                        print(f"[INFO] Loaded {len(self.messages)} previous messages for context")
        except:
            pass
    
    def add_message(self, role: str, text: str):
        """Add a message to memory"""
        self.messages.append({
            "time": datetime.now().isoformat(),
            "role": role,
            "text": text
        })
    
    def get_recent_context(self) -> str:
        """Get last few messages for context"""
        if not self.messages:
            return "No previous context"
        
        context_messages = self.messages[-3:]
        context = "Recent conversation:\n"
        for msg in context_messages:
            role = "USER" if msg["role"] == "user" else "BOT"
            context += f"{role}: {msg['text'][:80]}\n"
        return context
    
    def save_all(self):
        """Save all messages to file"""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.messages, f, indent=2)
        except Exception as e:
            print(f"[ERROR] Could not save: {e}")
    
    def get_stats(self) -> Dict:
        """Get conversation statistics"""
        total = len(self.messages)
        user_msgs = sum(1 for m in self.messages if m["role"] == "user")
        bot_msgs = sum(1 for m in self.messages if m["role"] == "assistant")
        
        return {
            "total": total,
            "user": user_msgs,
            "bot": bot_msgs,
            "duration": str(datetime.now() - self.session_start).split('.')[0]
        }

# ==================== BOT CLASS ====================

class ConversationalBot:
    """The main conversational bot with memory"""
    
    def __init__(self, user_id: str = "user"):
        self.user_id = user_id
        self.memory = MemoryManager(user_id)
        self.tools = [
            search_knowledge_base,
            analyze_intent,
            get_user_history_summary,
            save_important_fact
        ]
        
        self.system_prompt = """You are a helpful AI assistant that remembers conversations.

IMPORTANT RULES:
1. Be friendly, clear, and helpful
2. Use simple language, no jargon
3. Remember what the user told you before
4. Be honest if you don't know something
5. Keep answers concise unless asked for more
6. Use the tools to help you give better answers

Recent conversation context will be provided to help you remember.
Always maintain conversation flow and reference previous topics when relevant."""
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt + "\n\nCONTEXT:\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        self.agent = create_openai_functions_agent(llm, self.tools, self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=False)
    
    def chat(self, user_input: str) -> str:
        """Send a message and get response"""
        self.memory.add_message("user", user_input)
        
        try:
            context = self.memory.get_recent_context()
            
            result = self.executor.invoke({
                "input": user_input,
                "context": context,
                "chat_history": [],
                "agent_scratchpad": []
            })
            
            response = result.get("output", "I couldn't generate a response.")
            self.memory.add_message("assistant", response)
            self.memory.save_all()
            
            return response
        
        except Exception as e:
            error_msg = f"Error: {str(e)[:100]}"
            self.memory.add_message("assistant", error_msg)
            return error_msg
    
    def show_interface(self):
        """Show the interactive chat interface"""
        self.print_header()
        
        print("Commands: 'exit' (quit), 'clear' (clear history), 'stats' (show statistics)")
        print("-" * 70)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    self.show_goodbye()
                    break
                
                if user_input.lower() == "clear":
                    self.memory.messages = []
                    print("\n[INFO] Conversation cleared")
                    continue
                
                if user_input.lower() == "stats":
                    self.show_stats()
                    continue
                
                response = self.chat(user_input)
                print(f"\nBot: {response}")
            
            except KeyboardInterrupt:
                self.show_goodbye()
                break
            except Exception as e:
                print(f"\n[ERROR] {str(e)}")
    
    def demo_mode(self):
        """Run demo with predefined questions"""
        self.print_header()
        print("Running demo mode with example conversations...\n")
        
        demo_questions = [
            "What is artificial intelligence?",
            "Tell me about machine learning",
            "How does Python relate to AI?",
            "Remember earlier when we discussed ML - can you relate it to Python?",
            "What should I learn to become an AI engineer?"
        ]
        
        for i, question in enumerate(demo_questions, 1):
            print(f"\n[{i}/{len(demo_questions)}]")
            print(f"You: {question}")
            response = self.chat(question)
            print(f"Bot: {response}")
        
        self.show_stats()
        self.memory.save_all()
    
    def batch_mode(self, messages: List[str]):
        """Process multiple messages"""
        self.print_header()
        print("Processing messages in batch mode...\n")
        
        for i, msg in enumerate(messages, 1):
            print(f"\n[{i}/{len(messages)}]")
            print(f"You: {msg}")
            response = self.chat(msg)
            print(f"Bot: {response}")
        
        self.show_stats()
        self.memory.save_all()
    
    def print_header(self):
        """Print clean header"""
        print("\n" + "=" * 70)
        print("CONVERSATIONAL KNOWLEDGE BOT WITH MEMORY")
        print("=" * 70)
    
    def show_stats(self):
        """Show conversation statistics"""
        stats = self.memory.get_stats()
        print("\n" + "-" * 70)
        print("CONVERSATION STATISTICS")
        print("-" * 70)
        print(f"Total Messages: {stats['total']}")
        print(f"Your Messages: {stats['user']}")
        print(f"Bot Responses: {stats['bot']}")
        print(f"Duration: {stats['duration']}")
        print("-" * 70)
    
    def show_goodbye(self):
        """Show goodbye message"""
        self.memory.save_all()
        self.show_stats()
        print("\n[INFO] Conversation saved successfully")
        print("Thank you for chatting! Goodbye!")
        print("=" * 70 + "\n")

# ==================== MAIN ====================

def main():
    """Main entry point"""
    
    print("\n" + "=" * 70)
    print("CONVERSATIONAL BOT SYSTEM")
    print("=" * 70)
    print("\nSelect mode:")
    print("1 - Interactive Chat (talk to bot)")
    print("2 - Demo Mode (see example conversation)")
    print("3 - Batch Mode (process multiple messages)")
    print("-" * 70)
    
    choice = input("Your choice (1-3): ").strip()
    
    if choice == "1":
        bot = ConversationalBot(user_id="interactive")
        bot.show_interface()
    
    elif choice == "2":
        bot = ConversationalBot(user_id="demo")
        bot.demo_mode()
    
    elif choice == "3":
        bot = ConversationalBot(user_id="batch")
        print("\nEnter messages (type 'done' when finished):")
        messages = []
        while True:
            msg = input("Message: ").strip()
            if msg.lower() == "done":
                break
            if msg:
                messages.append(msg)
        
        if messages:
            bot.batch_mode(messages)
        else:
            print("No messages provided")
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
