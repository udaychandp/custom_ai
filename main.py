import speech_recognition as sr
import pyttsx3
import pywhatkit
import pyjokes
import wikipedia
import datetime
import requests 
from bs4 import BeautifulSoup


def speak(text,rate=150):
    engine = pyttsx3.init()
    engine.setProperty('rate',rate)
    engine.say(text)
    engine.runAndWait()

def get_command():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command  
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that. Can you please repeat?")
        return get_command()
    except sr.RequestError as e:
        speak(f"Error connecting to the server. {e}")
        return None

def execute_command(command):
    if "play music" in command:
        speak("What song would you like to listen to?")
        song = get_command()
        pywhatkit.playonyt(song)

    elif "tell me a joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif "search" in command:
        person = command.replace('search','')
        info = wikipedia.summary(person,5)
        speak(info)

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}")

    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {current_date}")
    elif "class" in command:
        timetable = {"Monday": {"09:30 AM - 10:30 AM": "E m i", "10:30 AM - 11:30 AM": "i c v", "11:30 AM - 12:30 PM": "e r t o s",
                                "12:30 PM - 01:10 PM": "lunch", "01:10 PM - 02:10 PM": "s c", "02:10 PM - 03:10 PM": "V l s i",
                                "03:10 PM - 04:10 PM": "sports"},
                    "Tuesday": {"09:30 AM - 10:30 AM": "v l s i", "10:30 AM - 11:30 AM": "e r t o s", "11:30 AM - 12:30 PM": "s c",
                                 "12:30 PM - 01:10 PM": "lunch", "01:10 PM - 02:10 PM": "i c v",
                                 "02:10 PM - 03:10 PM": "t w and t b", "03:10 PM - 04:10 PM": "t w and t b"},
                    "Wednesday": { "09:30 AM - 10:30 AM": "e r t o s","10:30 AM - 11:30 AM": "i c v",
                                  "11:30 AM - 12:30 PM": "e m i","12:30 PM - 01:10 PM": "lunch","01:10 PM - 02:10 PM": "s c",
                                  "02:10 PM - 03:10 PM": "V l s i","03:10 PM - 04:10 PM": "t w and t b"},
                    "Thursday": {"09:30 AM - 10:30 AM": "V l s i lab","10:30 AM - 11:30 AM": "V l s i lab","11:30 AM - 12:30 PM": "V l s i lab",
                                 "12:30 PM - 01:10 PM": "lunch","01:10 PM - 02:10 PM": "project stage 1","02:10 PM - 03:10 PM": "project stage 1",
                                 "03:10 PM - 04:10 PM": "project stage 1"},
                    "Friday": {"09:30 AM - 10:30 AM": "e r t o s","10:30 AM - 11:30 AM": "e m i","11:30 AM - 12:30 PM": "i c v",
                                "12:30 PM - 01:10 PM": "lunch","01:10 PM - 02:10 PM": "s c","02:10 PM - 03:10 PM": "t w and t b",
                                "03:10 PM - 04:10 PM": "library"},
                    "Saturday": {"09:30 AM - 10:30 AM": "s c","10:30 AM - 11:30 AM": "v l s i","11:30 AM - 12:30 PM": "e m i",
                                  "12:30 PM - 01:10 PM": "lunch","01:10 PM - 02:10 PM": "v l s i lab","02:10 PM - 03:10 PM": "v l s i lab","03:10 PM - 04:10 PM": "v l s i lab" },
                    "Sunday" :{"09:30 AM - 04:10 PM":"no classes on sunday"}}
        def convert_to_24_hour(time_str):
            return datetime.datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")
        def get_current_period():
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            current_time_24h = convert_to_24_hour(current_time)
            current_day = datetime.datetime.now().strftime("%A")

            # Debugging: Print current day and time
            print(f"Current Day: {current_day}")
            print(f"Current Time: {current_time_24h}")

            if current_day in timetable:
                # Debugging: Print timetable for the current day
                print(f"Timetable for {current_day}: {timetable.get(current_day, 'No classes scheduled for this day')}")

                for period, subject in timetable[current_day].items():
                    start_time, end_time = period.split(" - ")
                    start_time_24h = convert_to_24_hour(start_time)
                    end_time_24h = convert_to_24_hour(end_time)

                    if start_time_24h <= current_time_24h <= end_time_24h:
                        return f"The current period is {subject} from {period}"
            return "There is no class scheduled for this time."
        speak(get_current_period())
    elif "who created you" in command:
        speak("Sindhura and Sahithi created me under the guidance of Dr. Salal Uddin for their Mini Project")
    elif "How is the weather" in command:
        def get_weather_():
            try:
                # search_query = command()
                google_search_url = f"https://www.google.com/search?q={command}"

                # Send a GET request to the Google search page
                response = requests.get(google_search_url)
                response.raise_for_status()

                # Parse the HTML content of the page
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find the weather information in the search results
                weather_info = soup.find("div", {"class": "BNeawe iBp4i AP7Wnd"})
                
                return weather_info.text if weather_info else None

            except requests.exceptions.RequestException as e:
                 print(f"Error: {e}")
                 return None
    
        if __name__ == "__main__":
                # Replace 'City' with the desired city name
                

            weather_info = get_weather_()

            if weather_info:
                speak(weather_info)
            else:
                speak("Unable to fetch weather data.")

    
    else:
        speak("Sorry, I don't understand that command.")

if __name__ == "__main__":
    speak("Hello! I am friend, your personal assistant . How can I assist you today?")
    
    while True:
        command = get_command()
        
        if command and "switch off friend" in command:
            speak("Goodbye!")
            break

        if command:
            execute_command(command)





























