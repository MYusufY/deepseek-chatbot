import os
import time
from pathlib import Path

from markdownify import markdownify as md
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.common.exceptions import TimeoutException
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class DeepSeekChatBot:
    """
    A Selenium-based chatbot for interacting with DeepSeek Chat.

    This class handles logging in, selecting a chat session, sending prompts,
    and retrieving responses from the DeepSeek Chat web interface.
    """

    APP_URL = "https://chat.deepseek.com/"
    LOGIN_URL = "https://chat.deepseek.com/sign_in"
    USER_DATA_PATH = Path(os.environ.get("LOCALAPPDATA")) / r'Microsoft\Edge\User Data\Default'

    def __init__(self, session_to_attach):
        """
        Initializes the chatbot with a specific chat session.

        :param session_to_attach: The name of the chat session to attach to.
        """
        options = webdriver.EdgeOptions()
        options.add_argument(f"user-data-dir={self.USER_DATA_PATH}")
        self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        self.login()
        self.is_our_first_chat = False
        self.select_chat_session(session_to_attach)

    def login(self):
        """
        Logs into DeepSeek Chat. If manual login is required, waits for user input.
        """
        self.driver.get(self.APP_URL)
        try:
            WebDriverWait(self.driver, 5).until(EC.url_to_be(self.APP_URL))
        except TimeoutException:
            print("Please login manually in 10 mins.")
            WebDriverWait(self.driver, 600).until(EC.url_to_be(self.APP_URL))
        print("Login succeeded.")

    def select_chat_session(self, session_to_attach):
        """
        Selects the chat session to interact with.

        :param session_to_attach: The name of the session to attach to. If None, starts a new chat.
        """
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ds-icon-button"))
        ).click()
        time.sleep(1)
        if session_to_attach is not None:
            self.driver.find_elements(By.XPATH,
                f"//*[starts-with(text(), '{session_to_attach}')]"
            )[0].click()
        else:
            self.driver.find_element(By.XPATH,
                '//*[text()="New chat" or text()="开启新对话"]'
            ).click()
            self.is_our_first_chat = True

    def send_prompt(self, prompt):
        """
        Sends a prompt to the chat and retrieves the latest reply.

        :param prompt: The message to send.
        :return: The latest response in markdown format.
        """
        if self.is_our_first_chat:
            num_history_replies = 0
        else:
            history_replies = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "ds-markdown"))
            )
            num_history_replies = len(history_replies)

        time.sleep(1)
        prompt_escaped = prompt.replace("\n", Keys.SHIFT + Keys.ENTER + Keys.SHIFT)
        prompt_input = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "chat-input"))
        )
        prompt_input.clear()
        prompt_input.send_keys(prompt_escaped)
        time.sleep(1)
        prompt_input.send_keys(Keys.ENTER)

        return self._get_latest_reply(num_history_replies)

    def _get_latest_reply(self, num_history_replies):
        """
        Retrieves the latest reply from the chat after sending a prompt.

        :param num_history_replies: The number of replies before sending the prompt.
        :return: The latest reply in markdown format.
        :raises TimeoutException: If no reply is received within the allowed retries.
        """
        latest_reply = None
        maximum_trials = 600
        for _ in range(maximum_trials):
            all_replies = WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "ds-markdown"))
            )
            if len(all_replies) >= (num_history_replies + 1):
                latest_reply = all_replies[num_history_replies]
                self.is_our_first_chat = False
                break
            time.sleep(1)

        if latest_reply is None:
            raise TimeoutException(f"Failed to get the latest reply from DeepSeek.")

        # wait until the reply no longer changes
        previous_html = ""
        stable_count = 0
        stability_threshold = 4
        for _ in range(maximum_trials):
            latest_html = latest_reply.get_attribute('innerHTML')
            if latest_html == previous_html:
                stable_count += 1
                if stable_count >= stability_threshold:
                    return md(latest_html).strip()
            else:
                stable_count = 0
            previous_html = latest_html
            time.sleep(1)

        raise TimeoutException("WARNING: Failed to get the reply HTML.")

    def close(self):
        """
        Closes the Selenium WebDriver session.
        """
        self.driver.quit()

if __name__ == "__main__":
    bot = DeepSeekChatBot(session_to_attach=None)

    test_prompts = [
        "Hello from Selenium!",
        "What's the weather like today?",
        "Generate a short poem about space exploration.",
        "Tell me a joke.\nMake it about programming!",
        "List three key principles of good software design:\n1.\n2.\n3."
    ]

    for prompt in test_prompts:
        print(f"Prompt: {prompt}")
        response = bot.send_prompt(prompt)
        print(f"Response: {response}\n")
        time.sleep(5)

    bot.close()
