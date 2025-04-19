import pyttsx3

eg = pyttsx3.init()

eg.setProperty('rate', 200)

eg.say("У вас 123 очков")

eg.runAndWait()