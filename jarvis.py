from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import cv2
import speech_recognition as sr
import pyttsx3
import pytz
import subprocess
import webbrowser
from time import ctime
import requests, json
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from GoogleNews import GoogleNews
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
# import spotifywebapi
import os
import GroceryList

# If modifying these scopes, delete the file token.pickle.
SCOPES=['https://www.googleapis.com/auth/calendar.readonly']
MONTHS=["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
        "december"]
DAYS=["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENSIONS=["th", "st", "rd", "nd"]
HOURS=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
MINUTES=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
         31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
         59, 60]
SECONDS=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
         31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
         59, 60]
ALARM_PHRASE = ["a.m.","p.m."]
spotify_username=""
scope='user-read-private user-read-playback-state user-modify-playback-state'

now=datetime.datetime.now()
currentTime=now.strftime("%H:%M:%S")


def wishingMessage():
    goodMorningStart="00:00:00"
    goodMorningEnd="12:00:00"
    goodMorning="Good Morning"

    goodAfternoonStart="12:00:01"
    goodAfternoonEnd="17:00:00"
    goodAfternoon="Good Afternoon"

    goodEveningStart="17:00:01"
    goodEveningEnd="19:00:00"
    goodEvening="Good Evening"

    goodNightStart="19:00:01"
    goodNightEnd="23:00:59"
    goodNight="Good Night"

    if goodMorningStart <= currentTime <= goodMorningEnd:
        return goodMorning
    elif goodAfternoonStart <= currentTime <= goodAfternoonEnd:
        return goodAfternoon
    elif goodEveningStart <= currentTime <= goodEveningEnd:
        return goodEvening
    else:
        return goodEvening


def speak(text):
    # tts = gTTS(text=text, lang="en")
    # # filename = "jarvisSpeaks.mp3"
    # print(text)
    # tts.save(filename)
    # playsound.playsound(filename)
    engine=pyttsx3.init()
    engine.say(text)
    newVoiceRate=100
    engine.setProperty('rate', newVoiceRate)
    engine.runAndWait()


def get_audio():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        audio=r.listen(source)
        said=""

        try:
            said=r.recognize_google(audio)
            print(said)
        except sr.UnknownValueError:
            print("Sorry sir, I did not get that")
            speak("Sorry sir, I did not get that")
        except sr.RequestError:
            print("Sir it seems like my speech service is down")
            speak("Sir it seems like my speech service is down")
        except Exception as e:
            print("Exception" + str(e))
            speak("Exception" + str(e))

    return said.lower()


# textNew = wishingMessage()
# speak("Welcome sir, "+ textNew)
# speak("hey there")
#
# text = get_audio()
#
# if "hello" in text:
#     speak("hello sir, What shall i do for you", "new.mp3")
#     text=get_audio()
# elif "open browser" in text:
#     speak("opening, browser", "task.mp3")
#     text=get_audio()
# else:
#     speak("Sorry sir, you have not yet programmed me for doing that task", "standardMessage.mp3")

# textNew = wishingMessage()
# speak(textNew,"textNew.mp3")


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds=None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds=pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow=InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds=flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service=build('calendar', 'v3', credentials=creds)

    return service


def get_events(day, service):
    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print(f'Getting the upcoming {amount_of_events} events')
    date=datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date=datetime.datetime.combine(day, datetime.datetime.max.time())
    utc=pytz.UTC
    date=date.astimezone(utc)
    end_date=end_date.astimezone(utc)

    events_result=service.events().list(calendarId='primary', timeMin=date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events=events_result.get('items', [])

    if not events:
        speak('No upcoming events found sir')
    else:
        speak(f"You have {len(events)} events on this day.")

        for event in events:
            start=event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time=str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time=start_time + "am"
            else:
                start_time=str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
                start_time=start_time + "pm"

            speak(event["summary"] + " at " + start_time)


def get_date(text):
    text=text.lower()
    today=datetime.date.today()

    if text.count('today') > 0:
        return today

    day=-1
    day_of_week=-1
    month=-1
    year=today.year

    for word in text.split():
        if word in MONTHS:
            month=MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week=DAYS.index(word)
        elif word.isdigit():
            day=int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found=word.find(ext)
                if found > 0:
                    try:
                        day=int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year=year + 1

    if day < today.day and month == -1 and day != -1:
        month=month + 1

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week=today.weekday()
        difference=day_of_week - current_day_of_week

        if difference < 0:
            difference+=7
            if text.count("next") >= 1:
                difference+=7
        return today + datetime.timedelta(difference)
    if month == -1 or day == -1:
        return None
    return datetime.date(month=month, day=day, year=year)


def note(text):
    # date = datetime.datetime.now()
    # file_name = str(date).replace(":","-") + "-note.txt"
    speak("what should i name the file sir")
    filename=get_audio()
    with open(filename, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", filename])


def weather():
    weather_apiKey="78e0a2f3d9e39531add273acbf30c494"
    base_url="http://api.openweathermap.org/data/2.5/weather?"
    city=get_audio()
    complete_url=base_url + "appid=" + weather_apiKey + "&q=" + city

    # get method of requests module
    # return response object
    response=requests.get(complete_url)

    # json method of response object
    # convert json format data into python format data
    weather_json=response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if weather_json["cod"] != "404":
        # store the value of "main"
        # key in variable y
        y=weather_json["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature=y["temp"]
        celsius=current_temperature - 273.15

        # store the value corresponding
        # to the "pressure" key of y
        current_pressure=y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        current_humidiy=y["humidity"]

        # store the value of "weather"
        # key in variable z
        z=weather_json["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description=z[0]["description"]

        # print following values
        speak(" Temperature (in celsius unit) = " +
              str(celsius) +
              "\n atmospheric pressure (in hPa unit) = " +
              str(current_pressure) +
              "\n humidity (in percentage) = " +
              str(current_humidiy) +
              "\n description = " +
              str(weather_description))


def news():
    googlenews=GoogleNews(lang='en')
    speak("What would you like me to search the news for")
    search=get_audio()
    googlenews.search(search)
    result=googlenews.result()

    for search_result in result:
        speak(search_result)


def songs():
    speak("What would you like me to play")


def alarm(text):

    HOURS=-1
    MINUTES=-1
    SECONDS=-1

    currentTimeInHours=datetime.datetime.now().hour
    currentTimeInMinutes=datetime.datetime.now().minute

    # speak(text.split())

    alarm = [word for word in text.split() if word.isdigit()]

    print("printing alarm")
    print(str(*alarm))

    # alarmPhrase=text.find("p.m.")

    # if text.find("a.m."):
    #     print("a.m.")
    # elif text.find("p.m."):
    #     print("p.m.")
    # else:
    #     speak("Should I set it for am or pm?")
    #     text = get_audio()
    #     print(text)

def youtube():
    speak("what do you want to play on youtube, sir?")
    search=get_audio()
    driver = webdriver.Edge(executable_path="C:\\Users\\hshah\\Desktop\\personal folder\\edge  driver\\msedgedriver.exe")
    driver.get("https://youtube.com")
    searchbox = driver.find_element_by_xpath('//*[@id="search"]')
    searchboxNew = driver.find_element_by_id('search')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search"]'))).click()
    searchbox.send_keys(search)
    searchboxNew.send_keys(search)
    # searchbox.submit()

    searchbutton=driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')
    searchbutton.click()

def jarvis():
    WAKE="jarvis"

    EXIT="exit"

##    speak("Initiating JARVIS")
##    speak("Detecting Face")
##    import TrainingFaces


##    if TrainingFaces.confidence > 0:
##        # SERVICE=authenticate_google()

    textNew=wishingMessage()
    speak("Welcome sir, " + textNew)

    while True:

        print("Listening")
        text=get_audio()

        if text.count(WAKE) > 0:
            speak("Yes sir")
            text=get_audio()

            CALENDAR_STRINGS=["what do i have", "do i have plans", "am i busy", "what's my schedule like",
                              "can you list all the events on ", "list all the events on "]
            for phrase in CALENDAR_STRINGS:
                if phrase in text:
                    date=get_date(text)
                    if date:
                        get_events(date, SERVICE)
                    else:
                        speak("I don't understand sir in events")

            NOTE_STRINGS=["make a note", "write this down", "remember this", "open notepad"]
            for phrase in NOTE_STRINGS:
                if phrase in text:
                    speak("What would you like me to write down")
                    note_text=get_audio().lower()
                    note(note_text)
                    speak("I've made a note of that.")

            TIME_STRINGS=["what time is it", "can you please tell me the time"]
            for phrase in TIME_STRINGS:
                if phrase in text:
                    speak(ctime())

            SEARCH_STRINGS=["open search", "can you search"]
            for phrase in SEARCH_STRINGS:
                if phrase in text:
                    speak("what do you want to search for, sir")
                    text=get_audio()
                    search=text
                    url="https://google.com/search?q=" + search
                    webbrowser.get().open(url)
                    speak("here is what i found for" + search)

            LOCATION_STRINGS=["open maps", "can you find me " + "place", "can you find me " + "location",
                              "find the location for", "open map", "where is"]
            for phrase in LOCATION_STRINGS:
                if phrase in text:
                    speak("what do you want to locate for, sir")
                    text=get_audio()
                    location=text
                    url="https://google.nl/maps/place/=" + location + "/&amp;"
                    webbrowser.get().open(url)
                    speak("here is what i found for" + location)

            DESCRIPTION_STRINGS=["what is your name", "who is your programmer",
                                 "what is your name and who is your programmer",
                                 "who has created you"]  # still needs to be fixed
            for phrase in DESCRIPTION_STRINGS:
                if phrase in text:
                    speak("my name is jarvis and I have been programmed by Harshil Shah")
                break

            WEATHER_STRINGS=["what's the weather like"]
            for phrase in WEATHER_STRINGS:
                if phrase in text:
                    speak("Which city would you like me to look the weather for, sir")
                    weather()

            AUTHOR_WEBSITE=["open my website", "open my website will you"]
            for phrase in AUTHOR_WEBSITE:
                if phrase in text:
                    url="www.harshils.com"
                    webbrowser.get().open(url)
                    speak("opening your website sir")

            NEWS_STRINGS=["open news", "can you tell me the latest news", "search news", "show me the latest news",
                          "can you open the news for me please", "can you please open the news for me",
                          "can you read me the latest news"]

            for phrase in NEWS_STRINGS:
                if phrase in text:
                    try:
                        # speak("keyword")
                        # keyword = get_audio()
                        url="https://news.google.com/news/rss/"
                        Client=urlopen(url)
                        xml_page=Client.read()
                        Client.close()

                        soup_page=soup(xml_page, "lxml")
                        news_list=soup_page.findAll("item")

                        speak("How many news would you like me to read sir?")
                        read_articles=get_audio()

                        speak("Alright sir, Reading news")

                        for news in news_list[:int(read_articles)]:
                            speak(news.title.text.encode('utf-8'))
                        #  news()
                    except:
                        speak("You have not yet programmed me for this feature, sir ")

            YOUTUBE_STRINGS=["open youtube", "play videos on youtube"]
            for phrase in YOUTUBE_STRINGS:
                if phrase in text:
                    youtube()

            # SONGS_STRING=["play songs", "can you play some music", "can you please play some music",
            #               "can you play songs please", "hit it", "songs"]
            # for phrase in SONGS_STRING:
            #     if phrase in text:
            #         songs()

            # SOCIAL_MEDIA = ["open " + "social media accounts", "can you please open my social media accounts"]
            # for phrase in SOCIAL_MEDIA:
            #     if phrase in text.lower():
            #         # speak("which one would you like me to open, sir")
            #         text = get_audio()
            #         speak("opening facebook")
            #         url="https://www.facebook.com/"
            #         webbrowser.get().open(url)
            #         userEmailId = selenium.find_element_by_id('email')

            ALARM_STRINGS=["set up an alarm", "wake me up at"]
            for phrases in ALARM_STRINGS:
                if phrases in text.lower():
                    alarm(text)

            GROCERY_STRINGS = ["open grocery list and add items", "add items to the grocery list"]
            for phrase in GROCERY_STRINGS:
                if phrase in text:
                    grocery = GroceryList.Grocery()
                    grocery.GroceryList()

            SHOW_GROCERY_LIST_STRINGS=["what's there in my grocery list", "show me the grocery list"]
            for phrase in SHOW_GROCERY_LIST_STRINGS:
                if phrase in text:
                    grocery = GroceryList.Grocery()
                    grocery.ShowGroceryList()

            if text.count(EXIT) > 0:
                speak("Alright sir")
                exit()

            return speak
##    else:
##        speak("Sir I cannot recognize you")


if __name__ == '__main__':
    jarvis()
