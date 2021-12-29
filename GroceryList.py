from jarvis import speak, get_audio
import os

# class Grocery:
#     def __init__(self):
#         pass
#
#
#     def GroceryItems(self):
#         return speak("In Grocery")
#
#
# grocery = Grocery()
# grocery.GroceryItems()

class Grocery(object):
    def GroceryList(self):

        self.groceryList=['']

        speak("Is it one item or more, sir?")
        text=get_audio()

        if text == 1:
            speak("What would you like me to add, sir")
            text=get_audio()
            self.groceryList.append(text)
            with open("GroceryList.txt", "a") as GroceryList:
                GroceryList.write("\n".join(text))
            speak(f"{text} added to the list")
        else:
            speak("what items would you like me to add, sir?")
            text=get_audio()
            textSplit=text.split()
            self.groceryList.append(textSplit)
            with open("GroceryList.txt", "a") as GroceryList:
                GroceryList.write("\n".join(textSplit))
            speak(f"{textSplit} added to the list")

    def ShowGroceryList(self):
        if os.stat("GroceryList.txt").st_size != 0:
            File=open('GroceryList.txt', 'r')
            FileContents=File.read()
            speak(FileContents)
            File.close()
        else:
            speak("There's no item in the list, sir")