from Speak import speak
from GoogleNews import GoogleNews

def news():
    googlenews=GoogleNews(lang='en')
    speak("What would you like me to search the news for")
    search=get_audio()
    googlenews.search(search)
    result=googlenews.result()

    for search_result in result:
        speak(search_result)
