import speech_recognition as sr
from Speak import speak

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
