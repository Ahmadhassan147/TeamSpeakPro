import win32com.client as wn
try:
    if __name__ == '__main__':
        robo = wn.Dispatch("SAPI.SpVoice")
        print("Welcome to Robo Speaker 1.1 (Developed by : Ahmad)")
        while True:
            x = input("Enter text you want to speak: ")
            if x == "0":
                robo.Speak("Goodbye, thanks for using Robo Speaker")
                break
            robo.Speak(x)
except Exception as e:
    print("Following error occur : ", e)