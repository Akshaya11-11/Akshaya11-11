# Conversational Knowledge Bot with Memory

## What is this?

This is an AI chatbot that:
- Remembers everything you say (even after you close it)
- Learns from your conversations
- Answers questions about AI, Machine Learning, Python, Data Science
- Gets smarter as you talk to it more

Like a friend who remembers all your previous conversations!

---

## Features

**Memory System** - Bot remembers what you talked about before
**Smart Responses** - Uses tools to find information and think clearly
**Multiple Modes** - Chat interactively, see a demo, or process many messages at once
**Saves Everything** - All conversations saved automatically
**Statistics** - See how many messages you exchanged

---

## Setup (Step by Step)

### What You Need
- Python 3.9 or newer
- Your OpenAI API key (from https://platform.openai.com/api-keys)

### Installation Steps

**Step 1: Create a folder**
```
Create a new folder called "conversational-bot" on your desktop
```

**Step 2: Put files inside**
```
Put these 3 files in that folder:
- conversational_bot_clean.py
- requirements.txt
- README.md
```

**Step 3: Create .env file**
```
Open Notepad
Paste this: OPENAI_API_KEY=sk-your-actual-key-here
Replace sk-your-actual-key-here with your real API key
Save as ".env" in the same folder (File type: All Files)
```

**Step 4: Open Command Prompt in that folder**
```
Open your conversational-bot folder
Click address bar and type: cmd
Press Enter (black window opens)
```

**Step 5: Install packages**
```
In the black window, type:
pip install -r requirements.txt
Press Enter and wait (1-2 minutes)
```

**Step 6: Run the bot**
```
Type: python conversational_bot_clean.py
Press Enter
```

---

## How to Use

When you run the bot, you see:

```
CONVERSATIONAL BOT SYSTEM

Select mode:
1 - Interactive Chat (talk to bot)
2 - Demo Mode (see example conversation)
3 - Batch Mode (process multiple messages)

Your choice (1-3): 
```

### Option 1: Interactive Chat

Type "1" and press Enter

Now you can chat with the bot like texting:
```
You: Hello! Tell me about Python

Bot: Python is a programming language great for AI and data science. 
It's beginner-friendly and widely used in machine learning projects.

You: Can you relate this to AI?

Bot: Absolutely! Python is THE language for AI because...
[Bot remembers you asked about Python and connects it to AI]
```

Commands while chatting:
- Type normally to chat
- Type "stats" to see conversation statistics
- Type "clear" to start fresh
- Type "exit" to quit

### Option 2: Demo Mode

Type "2" and press Enter

The bot will run through 5 example conversations automatically. This shows you:
- How the bot works
- How it remembers previous topics
- What kind of questions it can answer

### Option 3: Batch Mode

Type "3" and press Enter

You can enter many messages at once:
```
Enter messages (type 'done' when finished):
Message: What is machine learning?
Message: How is it different from AI?
Message: What languages are used?
Message: done
```

The bot processes all of them while remembering context.

---

## What Gets Saved?

After each conversation, a JSON file is created:
```
memory_user_YYYYMMDD_HHMMSS.json
```

This file contains:
- Every message you sent
- Every response the bot gave
- When each message was sent
- User ID and session info

Next time you run it with the same user ID, it loads this file and remembers!

Example of saved data:
```json
[
  {
    "time": "2024-02-06T15:30:45",
    "role": "user",
    "text": "Tell me about Python"
  },
  {
    "time": "2024-02-06T15:30:46",
    "role": "assistant",
    "text": "Python is a programming language..."
  }
]
```

---

## Statistics Command

Type "stats" while chatting to see:
- Total messages exchanged
- How many you sent
- How many the bot sent
- How long you've been chatting

Example output:
```
CONVERSATION STATISTICS
Total Messages: 10
Your Messages: 5
Bot Responses: 5
Duration: 00:05:30
```

---

## The Bot Can Talk About

- Artificial Intelligence
- Machine Learning
- Python Programming
- Data Science
- LangChain
- OpenAI and AI models
- General technology topics

For other topics, the bot will try to help but might give general knowledge responses.

---

## How Memory Works

1. You send a message
2. Bot looks at previous messages for context
3. Bot thinks about what you're asking
4. Bot generates a smart response
5. Response is saved to the memory file

Next time you start with the same user ID:
1. Bot loads the memory file
2. Bot reads the last few messages
3. Bot uses this context to understand you better

This makes conversations more natural and personal!

---

## Troubleshooting

**Problem: "ModuleNotFoundError: No module named 'langchain'"**
Solution: Run this command:
```
pip install -r requirements.txt
```

**Problem: "OpenAI API key not found"**
Solution: 
- Check that .env file exists in your folder
- Check that it has: OPENAI_API_KEY=sk-[your-key]
- Make sure you replaced [your-key] with your actual key

**Problem: Bot is taking too long to respond**
Solution:
- Your internet connection might be slow
- OpenAI servers might be busy
- Just wait, it usually takes 5-15 seconds

**Problem: "api_request_failed" error**
Solution:
- Check your API key is correct
- Check your internet connection
- Go to https://status.openai.com to see if OpenAI has issues

**Problem: Bot doesn't remember previous conversations**
Solution:
- Check that memory_*.json files exist in your folder
- Make sure you use the same user ID when running
- Try restarting the bot

---

## Customization

### Change the AI Model

Open conversational_bot_clean.py

Find this line (around line 20):
```python
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
```

Change to:
```python
llm = ChatOpenAI(
    model="gpt-4",
```

This uses GPT-4 (better but more expensive).

### Change System Behavior

Find "self.system_prompt =" around line 110

You can change the personality and rules here.

For example, change:
```python
"Be friendly, clear, and helpful"
```

To:
```python
"Be professional and formal in tone"
```

---

## Cost Estimation

Using gpt-3.5-turbo (default):
- Small conversation (10 messages): $0.01
- Long conversation (100 messages): $0.10
- Regular daily use (1 month): $1-5

Using gpt-4:
- Small conversation: $0.05
- Long conversation: $0.50
- Regular daily use (1 month): $10-50

---

## Files Explained

**conversational_bot_clean.py**
- The main bot code
- Has the MemoryManager class (handles memory)
- Has the ConversationalBot class (does the chatting)
- Run this file to start the bot

**requirements.txt**
- List of Python packages needed
- pip uses this to download everything
- Don't edit this file

**.env**
- Your API key
- NEVER share this file
- NEVER put this on GitHub

**memory_*.json**
- Saved conversations
- You can look at it with Notepad
- You can delete it to clear history

**README.md**
- This file
- Instructions for using the bot

---

## Advanced Features

### Use Different User IDs

In the code, each bot is created with a user_id:
```python
bot = ConversationalBot(user_id="john_smith")
```

Different user IDs have separate memory files!

So:
- User "john" has their own memories
- User "sarah" has separate memories
- Great for multiple people using the same bot

### Save Important Learnings

The bot can save important facts from conversations:
```
Bot uses: save_important_fact("Machine Learning", "ML learns from data")
```

This gets saved and used in future responses.

### Analyze User Intent

The bot figures out what you want:
- Is it a question? (has ?)
- Do you need help? (says "help")
- Do you want to learn? (says "explain")

Then it responds appropriately!

---

## How It's Built

The bot uses LangChain (a popular AI framework) with OpenAI GPT.

Architecture:
```
User sends message
         |
    Memory Manager checks history
         |
    Bot analyzes intent and context
         |
    Tools search knowledge base
         |
    GPT generates response
         |
    Response is saved to memory
         |
    Bot shows response to user
```

---

## Support & Help

If something doesn't work:
1. Check the Troubleshooting section above
2. Make sure all files are in the same folder
3. Make sure API key is correct
4. Make sure internet connection works
5. Try restarting the Command Prompt

---

## License

This project is free to use and modify.

---

## Summary

This bot is a complete conversational AI system with:
✓ Memory that persists across sessions
✓ Smart responses using tools
✓ Multiple interaction modes
✓ Clean, professional interface
✓ Saves all conversations automatically
✓ Learn and improve over time

Perfect for demonstrating advanced LLM capabilities and conversational AI!

Start with Option 1 (Interactive Chat) for the best experience.

Enjoy!
