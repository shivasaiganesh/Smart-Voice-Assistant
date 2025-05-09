import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import subprocess
import tkinter as tk
from tkinter import Label, Button, Text, Scrollbar, Frame, PhotoImage  
from tkinter import ttk  
import yfinance as yf  
import requests  
from bs4 import BeautifulSoup  
import wikipedia 
import pyjokes
import smtplib
from googletrans import Translator
import threading
from PIL import Image, ImageTk 
import pyautogui  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import psutil  
import time 
import cv2 
def log_message(message):
    log_text.config(state="normal")
    log_text.insert("end", message + "\n")
    log_text.see("end")
    log_text.config(state="disabled")


def vibrate_mic():
    def resize_image(scale):
        resized_image = mic_image_original.resize((int(100 * scale), int(100 * scale)), Image.Resampling.LANCZOS)
        mic_image_resized = ImageTk.PhotoImage(resized_image)
        mic_label.config(image=mic_image_resized)
        mic_label.image = mic_image_resized  

    def animate():
        for scale in [1.0, 1.1, 1.0]: 
            resize_image(scale)
            root.update()
            root.after(100)  # Delay - 100ms

    threading.Thread(target=animate, daemon=True).start()


def speak(text):
    vibrate_mic()  
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    log_message(f"Assistant: {text}")

def listen_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening for wake word...")
        while True:
            try:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                if "python" in command or "hello" in command or "hi" in command or "hi chitti" in command:  # Wake word 
                    status_label.config(text="Wake word detected! Listening for commands...")
                    speak("Yes, how can I assist you?")
                    listen_for_command() 
            except sr.UnknownValueError:
                continue  
            except sr.RequestError:
                status_label.config(text="Could not request results, check internet connection.")
                log_message("Assistant: Could not request results, check internet connection.")
                break


def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening for a command...") 
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            command = recognizer.recognize_google(audio).lower()
            log_message(f"You: {command}")
            status_label.config(text=f"You said: {command}")
            execute_command(command)
        except sr.UnknownValueError:
            status_label.config(text="Sorry, I could not understand. Please try again.")
            log_message("Assistant: Sorry, I could not understand. Please try again.")
            listen_for_command()  
        except sr.RequestError:
            status_label.config(text="Could not request results, check internet connection.")
            log_message("Assistant: Could not request results, check internet connection.")

def get_weather(city):
    api_key = "fb8cc09db67e3035321c3bf8dcfcca24"  
    base_url = "https://openweathermap.org/"
    params = {"q": city, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"The current temperature in {city} is {temp}°C with {description}."
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return "Sorry, I couldn't fetch the weather. Please try again."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I couldn't fetch the weather. Please try again."


def get_latest_news():
    url = "https://www.bbc.com/news"  
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        headlines = soup.select(".gs-c-promo-heading__title")  
        news_list = [headline.get_text() for headline in headlines[:5]]  
        
        if not news_list:
            return "Sorry, I couldn't fetch the news. Please try again later."
        
        return "Here are the latest news headlines:\n" + "\n".join(news_list)
    except Exception as e:
        return "Sorry, I couldn't fetch the news. Please try again."

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)
    status_label.config(text=joke)

def send_email():
    try:
        speak("Who should I send the email to?")
        recipient = input("Enter recipient email: ").strip()
        speak("What should I say?")
        content = input("Enter email content: ").strip()
        sender_email = "abkbhanukiran@gmail.com"  
        sender_password = "xgys hkth ryrn lwnp"  

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)  
            server.sendmail(sender_email, recipient, content)  
        speak("Email sent successfully.")
        status_label.config(text="Email sent successfully.")
    except Exception as e:
        speak("Sorry, I couldn't send the email. Please try again.")
        print(f"Error: {e}")

def translate_text(text, target_language):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=target_language)
        speak(f"The translation is: {translation.text}")
        status_label.config(text=f"Translation: {translation.text}")
    except Exception as e:
        speak("Sorry, I couldn't translate the text.")
        print(f"Error: {e}")

def take_screenshot():
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")  
        speak("Screenshot taken and saved as screenshot.png.")
        status_label.config(text="Screenshot saved as screenshot.png.")
    except Exception as e:
        speak("Sorry, I couldn't take the screenshot.")
        print(f"Error: {e}")

def take_picture():
    try:
        speak("Opening the camera. Please smile!")
        
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            speak("Sorry, I couldn't access the camera.")
            return

        
        ret, frame = cam.read()
        if ret:
            
            image_path = "captured_image.jpg"
            cv2.imwrite(image_path, frame)
            speak(f"Picture taken and saved as {image_path}.")
            status_label.config(text=f"Picture saved as {image_path}.")
        else:
            speak("Sorry, I couldn't capture the image.")
        
        
        cam.release()
        cv2.destroyAllWindows()
    except Exception as e:
        speak("Sorry, I couldn't take the picture.")
        print(f"Error: {e}")

def play_song_on_youtube(song_name):
    try:
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        query = song_name.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={query}"
        driver.get(url)
        

        video = driver.find_element(By.XPATH, '//a[@id="video-title"]')
        video_url = video.get_attribute("href")
        
        if video_url:
            webbrowser.open(video_url)  
            speak(f"Playing {song_name} on YouTube.")
        else:
            speak("Sorry, I couldn't find the song on YouTube.")
    except Exception as e:
        speak("Sorry, I couldn't play the song. Please try again.")
        print(f"Error: {e}")
    finally:
        driver.quit()  

def set_timer(duration):
    try:
        speak(f"Timer set for {duration} seconds.")
        time.sleep(duration)  
        speak("Time's up!")
        status_label.config(text="Time's up!")
    except Exception as e:
        speak("Sorry, I couldn't set the timer.")
        print(f"Error: {e}")

def execute_command(command):
    if "open calculator" in command:
        speak("Opening Calculator.")
        subprocess.Popen("calc.exe")  
        listen_for_command()  
    elif "restart" in command:
        speak("Restarting the PC. Please wait.")
        os.system("shutdown /r /t 1") 
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        status_label.config(text=f"Time: {now}")
        listen_for_command()  
    elif "battery percentage" in command or "battery status" in command:
        battery = psutil.sensors_battery()
        if battery:
            percentage = battery.percent
            speak(f"The battery is at {percentage} percent.")
            status_label.config(text=f"Battery: {percentage}%")
        else:
            speak("Sorry, I couldn't retrieve the battery status.")
        listen_for_command()  
    elif "open google" in command:
        search_query = command.replace("open google", "").strip()
        if search_query:
            speak(f"Searching for {search_query} on Google")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        else:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        listen_for_command()  
    elif "shutdown" in command:
        speak("Shutting down the PC. Goodbye!")
        os.system("shutdown /s /t 1")  
    elif "joke" in command:
        tell_joke()  
        listen_for_command()  
    elif "navigate to" in command or "directions to" in command:
        location = command.replace("navigate to", "").replace("directions to", "").strip()
        if location:
            speak(f"Getting directions to {location}")
            webbrowser.open(f"https://www.google.com/maps/dir/?api=1&destination={location}")
        else:
            speak("Please specify a location to navigate to.")
        listen_for_command()  
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        status_label.config(text="YouTube opened. Waiting for the next command...")
        root.after(5000, listen_for_command)  
    elif "play" in command or "song" in command:
        speak("Playing song")
        song_name = command.replace("play", "").strip()
        song_name = command.replace("song", "").strip()
        if song_name:
            play_song_on_youtube(song_name)  
        else:
            speak("Please specify the song name.")
        listen_for_command()  
    elif "open notepad" in command:
        speak("Opening Notepad")
        subprocess.Popen(["notepad.exe"])  
        listen_for_command()  
    elif "weather" in command:
        city = command.replace("weather", "").strip()
        if city:
            weather_info = get_weather(city)
            speak(weather_info)
            status_label.config(text=weather_info)
        else:
            speak("Please specify a city to get the weather information.")
        listen_for_command()  
    elif "take screenshot" in command or "screenshot" in command:
        take_screenshot()  
        listen_for_command()  
    elif "take a pic" in command or "take a picture" in command:
        take_picture()  
        listen_for_command()  
    elif "translate" in command:
        try:
            matter = command.replace("translate", "").strip()
            text_to_translate =matter
            target_language = 'hi'
            
            if text_to_translate and target_language:
                translate_text(text_to_translate, target_language)  
            else:
                speak("Please provide both the text and the target language.")
        except Exception as e:
            speak("Sorry, I couldn't process the translation command.")
            print(f"Error: {e}")
        listen_for_command()  
    elif "send email" in command:
        try:
            send_email()  
        except Exception as e:
            speak("Sorry, I couldn't send the email. Please try again.")
            print(f"Error: {e}")
        listen_for_command()  
    elif "take note" in command:
        speak("What would you like me to note down?")
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                note = recognizer.recognize_google(audio)
                speak("Noted. Opening Notepad.")
                with open("note.txt", "w") as file:
                    file.write(note)
                subprocess.Popen(["notepad.exe", "note.txt"])  
            except sr.UnknownValueError:
                speak("Sorry, I couldn't understand. Please try again.")
            except sr.RequestError:
                speak("Could not request results, please check your internet connection.")
        listen_for_command()  
    elif "set timer" in command:
        try:
            duration = int(command.replace("set timer", "").strip())
            threading.Thread(target=set_timer, args=(duration,), daemon=True).start()
        except ValueError:
            speak("Please specify the timer duration in seconds.")
        listen_for_command()  
    elif "news" in command:
        news_info = get_latest_news()
        speak(news_info)
        status_label.config(text=news_info)
        listen_for_command()
    elif "wikipedia" in command:    
        query = command.replace("wikipedia", "").strip()
        if query:
            result = wikipedia.summary(query, sentences=2)
            speak(result)
            status_label.config(text=result)
        else:
            speak("Please specify a topic to search on Wikipedia.")
        listen_for_command()
    elif "stock price" in command:
        stock_symbol = command.replace("stock price", "").strip()
        if stock_symbol:
            try:
                stock = yf.Ticker(stock_symbol)
                price = stock.history(period="1d")["Close"][0]
                speak(f"The current price of {stock_symbol} is {price}")
                status_label.config(text=f"Stock Price: {price}")
            except Exception as e:
                speak("Sorry, I couldn't fetch the stock price.")
                print(f"Error: {e}")
        else:
            speak("Please specify a stock symbol.")
        listen_for_command()
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        status_label.config(text="Goodbye!")
        root.quit() 
    else:
        listen_for_command   

def start_wake_word_detection():
    threading.Thread(target=listen_for_wake_word, daemon=True).start()

start_wake_word_detection()

root = tk.Tk()
root.title("Smart Voice Assistant")
root.geometry("600x500")
root.configure(bg="#121212")  


header_frame = Frame(root, bg="#1F1F1F", height=60)  
header_frame.pack(fill="x")
header_label = Label(header_frame, text="Smart Voice Assistant", font=("Arial", 20, "bold"), bg="#1F1F1F", fg="#FFFFFF")  # White text
header_label.pack(pady=10)

status_label = Label(root, text="Listening for wake word...", font=("Arial", 14), bg="#121212", fg="#FFFFFF")  # White text
status_label.pack(pady=10)


mic_frame = Frame(root, bg="#121212")
mic_frame.pack(pady=20)


mic_image_original = Image.open("mic.png")  
mic_image_resized = mic_image_original.resize((100, 100), Image.Resampling.LANCZOS)  
mic_image = ImageTk.PhotoImage(mic_image_resized)


mic_label = Label(mic_frame, image=mic_image, bg="#121212")
mic_label.pack()


log_frame = Frame(root, bg="#1F1F1F")  
log_frame.pack(pady=10, padx=10, fill="both", expand=True)

scrollbar = Scrollbar(log_frame, bg="#1F1F1F", troughcolor="#333333", activebackground="#555555")  
scrollbar.pack(side="right", fill="y")

log_text = Text(log_frame, height=15, state="disabled", wrap="word", font=("Arial", 12), yscrollcommand=scrollbar.set, bg="#1F1F1F", fg="#FFFFFF", insertbackground="#FFFFFF")  # Dark background and white text
log_text.pack(side="left", fill="both", expand=True)
scrollbar.config(command=log_text.yview)




footer_label = Label(root, text="Developed by Group 1", font=("Arial", 10), bg="#121212", fg="#777777")  # Gray text
footer_label.pack(side="bottom", pady=10)

root.mainloop()