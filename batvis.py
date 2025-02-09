import pyttsx3
import datetime 
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import requests
from newsapi import NewsApiClient
import pywhatkit
import random
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice', voices[0].id)
OPENWEATHERMAP_API_KEY = '6c303c3c28a6e04f0916ac2fda5c3def'
WEATHER_API_URL = 'https://openweathermap.org/'
NEWS_API_KEY = '3e55f5c4a7d047cb91c87b30a12bc53a'

def speak(audio):
       engine.say(audio)
       engine.runAndWait()  
def wishMe():
       hour = int(datetime.datetime.now().hour)
       if hour>=0 and hour<12:
              speak("Good Morning!")

       elif hour>=12 and hour<18:
              speak("Good Afternoon!")

       else:
              speak("Good Evening!")

       speak("Hello sir i am batvis , how may i help you?")

def takeCommand():
       r = sr.Recognizer()
       with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
       try:
             print("Recognizing...") 
             query = r.recognize_google(audio,language='en-in')
             print(f"User said: {query}\n")
       except Exception as e:
             #print(e)

             print("Say that again please...")   
             return"None"
       return query

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        weather_data = response.json()
        if not weather_data:
            return f"No weather information available for {city}."

        main_weather = weather_data['weather'][0]['main']
        temperature = weather_data['main']['temp']
        return f"The weather in {city} is {main_weather} with a temperature of {temperature}°C."
    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"Error: {err}"
def tell_joke():
    joke_api_url = 'https://official-joke-api.appspot.com/random_joke'

    try:
        response = requests.get(joke_api_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        joke_data = response.json()

        if 'setup' in joke_data and 'punchline' in joke_data:
            setup = joke_data['setup']
            punchline = joke_data['punchline']
            return f"Here's a joke for you: {setup}... {punchline}"

        return "Oops! Something went wrong. I can't fetch a joke right now."

    except requests.exceptions.HTTPError as errh:
        return f"HTTP Error: {errh}"
    except requests.exceptions.ConnectionError as errc:
        return f"Error Connecting: {errc}"
    except requests.exceptions.Timeout as errt:
        return f"Timeout Error: {errt}"
    except requests.exceptions.RequestException as err:
        return f"Error: {err}"     

def get_news_headlines():
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)

    try:
        headlines = newsapi.get_top_headlines(language='en', country='us')
        articles = headlines['articles']

        if articles:
            speak("Here are the latest news headlines:")
            for article in articles:
                title = article['title']
                speak(title)
        else:
            speak("I couldn't fetch the latest news headlines at the moment.")

    except Exception as e:
        speak(f"An error occurred while fetching the news: {str(e)}")
def play_youtube_song(song_name):
    pywhatkit.playonyt(song_name)
    speak(f"Now playing {song_name} on YouTube.")
def trivia():
    questions = {
        "What is the capital of France?": "Paris",
        "Which planet is known as the Red Planet?": "Mars",
        "What is the largest mammal in the world?": "Blue Whale",
        "How many continents are there?": "Seven",
        "Who wrote 'Romeo and Juliet'?": "William Shakespeare",
    }

    question = random.choice(list(questions.keys()))
    correct_answer = questions[question]

    speak(question)
    user_answer = takeCommand()

    if user_answer.lower() == correct_answer.lower():
        speak("Correct! Well done.")
    else:
        speak(f"Sorry, the correct answer is {correct_answer}.")
                    
if __name__ == "__main__":
       while True:
       #if 1:
             query = takeCommand().lower()
             # Logic for executing tasks based on query
             if 'wikipedia' in query:
                   speak('Searching wikipedia...')
                   query = query.replace('wikipedia', "")
                   results = wikipedia.summary(query, sentences=2)
                   speak('According to wikipedia')
                   speak(results)
                   print(results)
             elif 'weather' in query:
                   speak("Sure, could you please specify the city?")
                   city = takeCommand()
                   weather_response = get_weather(city)
                   speak(weather_response)
                   print(weather_response)
                        
             elif 'open youtube' in query:
                   webbrowser.open('youtube.com')
             elif 'open google' in query:
                   webbrowser.open('google.com')   
             elif 'play downloaded songs' in query:
                   music = 'C:\songs'
                   songs = os.listdir(music)
                   os.startfile(os.path.join(music,songs[0]))
             elif 'the time' in query:
                   strTime = datetime.datetime.now().strftime("%H:%M:%S")
                   speak(f"Sir, the time is {strTime}")
                   print(strTime)
             elif 'open vs code' in query:
                   path = "C:\\Users\\lavan\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                   os.startfile(path)   
             elif 'tell a joke' in query:                        
                        joke_response = tell_joke()
                        speak(joke_response)  
                        print(joke_response)                       
             elif 'read news' in query or 'latest news' in query:                           
                            get_news_headlines()                     
             elif 'play song' in query or 'play music' in query:

                  speak("Sure, what song would you like to play?")
                  song_name = takeCommand()
                  play_youtube_song(song_name)    
             elif 'trivia' in query:
                  trivia()   
