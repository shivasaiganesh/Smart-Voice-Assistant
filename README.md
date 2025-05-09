# 🎙️ Chitti - Python Voice Assistant GUI

**Chitti** is an AI-powered personal voice assistant with a sleek GUI built using Python. It can perform various tasks such as telling jokes, fetching news, translating text, playing music, searching the web, sending emails, giving weather updates, and more — all through your voice commands.

## 🚀 Features

- 🎤 Wake word activation: "hello", "hi", "python", "hi chitti"
- 🗣️ Voice recognition & text-to-speech using `speech_recognition` & `pyttsx3`
- 🔍 Google search, Wikipedia summary, Google Maps directions
- ⏰ Timer setup via natural language
- 📷 Take screenshots and capture camera photos
- ✉️ Send emails using SMTP (Gmail)
- 💹 Check stock prices with `yfinance`
- 🌦️ Real-time weather updates from OpenWeatherMap
- 📰 News scraping from BBC
- 🎵 Play songs on YouTube using Selenium
- 😂 Tell jokes using `pyjokes`
- 🔋 Check battery level using `psutil`
- 🌍 Translate text to other languages
- 💻 Restart or shutdown the system
- 🖼️ GUI interface with animated mic and status logs using `tkinter` and `PIL`

## 🖥️ GUI Preview

- 🎛️ Mic icon activates when Chitti is listening
- 🗒️ Scrollable text area shows conversation logs
- 🔄 Status label indicates what the assistant is doing

Libraries Used
speechrecognition

pyttsx3

pyjokes

pyautogui

opencv-python

requests

beautifulsoup4

googletrans==4.0.0-rc1

pillow

selenium

webdriver-manager

yfinance

wikipedia

psutil

tkinter (comes with Python)

⚙️ How to Use
Clone this repository.

Speak any of the wake words like “hi chitti” to activate it.

Ask questions or give commands such as:

“What’s the weather in Chennai?”

“Tell me a joke”

“Open Google”

“Translate hello to Spanish”

“Play Shape of You on YouTube”

🔐 Email Configuration
To enable email functionality:

Use Gmail App Passwords (2FA must be enabled).

Replace your email credentials in the script (temporarily).

Never hardcode your password in production — use .env or keyring.

📌 TODO
Replace input() with GUI input for translation and email

Background wake word detection (non-blocking)

Add smart assistant (ChatGPT / LLM integration)

Better error handling & modularize code

🧠 Credits
Developed by Shiva Sai Ganesh
🔗 Project Name: Chitti - The Python Voice Assistant

© 2025 Shiva Sai Ganesh. All rights reserved.
