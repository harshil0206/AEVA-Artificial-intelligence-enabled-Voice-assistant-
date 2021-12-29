from Speak import speak

def note(text):
    # date = datetime.datetime.now()
    # file_name = str(date).replace(":","-") + "-note.txt"
    speak("what should i name the file sir")
    filename=get_audio()
    with open(filename, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", filename])
