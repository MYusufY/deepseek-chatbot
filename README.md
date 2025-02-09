# DeepSeek ChatBot

A Selenium-based Python module that automates interactions with the DeepSeek Chat web interface.

![Demo](https://github.com/user-attachments/assets/eaafe14f-0afc-4085-af70-14c2fb87a389)

## Requirements
- Python 3.7+
- Microsoft Edge browser

**NOTE:** Selenium uses The `Default` profile of Microsoft Edge, which is located at `"$Env:LOCALAPPDATA\Microsoft\Edge\User Data\Default"` on Windows 11.

## Installation
Install the required dependencies
```bash
pip install -r requirements.txt
```

Run the built-in test  
```bash
python deepseek_chatbot.py
```
**NOTE:** During the first run, you may need to manually log in to DeepSeek inside the broswer opened by Selenium.

## Usage
Import `deepseek_chatbot` module to your script
```python
from deepseek_chatbot import DeepSeekChatBot
```

Start a new chatting session
```python
bot = DeepSeekChatBot(session_to_attach=None)
```

or provide a session name to continue an existing chat
```python
# it's also acceptable to only provide the beginning of the session name
bot = DeepSeekChatBot(session_to_attach="Some existing session")
```

Send a prompt
```python
# the response will be in markdown format
response = bot.send_prompt("Hello, how are you?")
print(response)
```

Finish chatting
```python
bot.close()
```