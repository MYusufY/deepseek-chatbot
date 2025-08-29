# DeepSeek ChatBot

A Selenium-based Python module that automates interactions with the DeepSeek Chat web interface.

![Demo](https://github.com/user-attachments/assets/eaafe14f-0afc-4085-af70-14c2fb87a389)

## Requirements
- Python 3.7+
- One of the following browsers:
  - Microsoft Edge
  - Google Chrome

**NOTE:** Selenium uses The `Default` profile of Microsoft Edge, which is located at `"$Env:LOCALAPPDATA\Microsoft\Edge\User Data\Default"` on Windows 11. In chrome version, you can specify your profile path.

## Installation
Install the required dependencies
```bash
pip install -r requirements.txt
```

Run the built-in test (for edge)
```bash
python deepseek_edge.py
```
**NOTE:** During the first run, you may need to manually log in to DeepSeek inside the broswer opened by Selenium.

## Usage

### Microsoft Edge
Import `deepseek_edge` module to your script
```python
from deepseek_edge import DeepSeekChatBot
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

### Google Chrome
Import `deepseek_chrome` module to your script
```python
from deepseek_chrome import DeepSeek
```

Start a new chatting session (with example Chrome path for macOS)
```python
bot = DeepSeek(session_name=None, profile_path="deepseek-profile", chrome_path="/Applications/Chrome.app/Contents/MacOS/Google Chrome") # Please customize your Chrome path by your system!
```

or provide a session name to continue an existing chat
```python
# it's also acceptable to only provide the beginning of the session name
bot = DeepSeek(session_name="Some existing session", profile_path="deepseek-profile", chrome_path="/Applications/Chrome.app/Contents/MacOS/Google Chrome")
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
