import pyttsx3
import wikipedia
import pygame
import smtplib
import speech_recognition as sr
import datetime
import time
import webbrowser
import os
import requests


# For getting the audio 
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Speak the commands 
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# For greeting 
def wishme():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")


# To get input voice from user 
def takeCommand():
    query = None
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 0.8
        r.energy_threshold = 300
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-IN')
        print(f"User said: {query}\n")
        return query
    except sr.UnknownValueError:
        print("Could not understand the audio")
        speak("I couldn't understand. Please type your command.")
        
    except sr.RequestError as e:
        print("Service error: ", e)
        speak("I couldn't understand. Please type your command.")

    return query
    

# contact for emails 
contacts = {
    "Reciver_name": "Recievers_email.com",
}

# Send the emails 
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email.com', 'your_email_password')
    server.sendmail('your_email.com', to, content)
    server.close()


# Play the song 
song_index = 0
music_dir = 'path\music\directory'
songs = os.listdir(music_dir)
pygame.mixer.init()


# Store the result or info in the txt file get result from chatgpt api 
def gpt(prompt):
    # Correct API endpoint and key
    api_url = "your_api_url/endpoint"  # Updated endpoint
    api_key = "your_api_key"

    text = f"AI response for Prompt: {prompt} \n ********************************* \n \n"

    # Payload for text generation
    payload = {
        "model": "jamba-1.5-large",  # Use one of the valid model names
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4000,
    }

    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Make the request
    response = requests.post(api_url, headers=headers, json=payload)

    # Check response status and print
    if response.status_code == 200:
        response_json = response.json()
        if "choices" in response_json and response_json["choices"]:
            # Print only the generated content
            generated_text = response_json["choices"][0]["message"]["content"]
            text += generated_text
        else:
            print("No choices found in the response.")
            text += "No choices found in the response."
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        text += str(response.json())

    # Create directory if it doesn't exist
    if not os.path.exists("Openai"):
        os.makedirs("Openai")

    # Create file with a random name
    file_name = f"Openai\{''.join(prompt.split('ai')[1:]).split()}.txt"
    with open(file_name, "w") as f:
        f.write(text)
    
    print(f"Result it stored in file : {file_name}.")



# For chat/talk with user by using the gpt api 
chatstr = ""
def chat(query): 
    global chatstr
    
    # Correct API endpoint and key
    api_url = "your_api_url/endpoint"  
    api_key = "your_api_key"

    chatstr += f"Swapnil: {query} \nJarvis: "
    
    # Payload for text generation
    payload = {
        "model": "jamba-1.5-large", 
        "messages": [
            {"role": "user", "content": chatstr}
        ],
        "max_tokens": 4000,
    }

    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Make the request
    response = requests.post(api_url, headers=headers, json=payload)

    # Check response status and print
    if response.status_code == 200:
        response_json = response.json()
        if "choices" in response_json and response_json["choices"]:
            # Print only the generated content
            generated_text = response_json["choices"][0]["message"]["content"]
            chatstr += f"{generated_text}\n"
            speak(generated_text)
            return generated_text
        else:
            print("No choices found in the response.")
            chatstr += "No choices found in the response."
    else:
        error_message = f"Error: {response.status_code}\n{response.json()}"
        print(error_message)
        chatstr += error_message
        return error_message
    

# Main program or access the function     

if __name__ == "__main__":
    speak("Hello, sir.")
    wishme()
    
    while True:   # For continuesly listen the commands 
        query = takeCommand()

        if query is None : 
            query = input("Entet the command : ").lower()
            print(f"Processing the text input : {query}")
        else:
            query = query.lower()

        if 'wikipedia' in query:
            speak("Searching Wikipedia")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia:")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("http://www.youtube.com")
            speak("Opening YouTube")

        elif 'open google' in query:
            webbrowser.open("http://www.google.com")
            speak("Opening Google")

        elif 'play music' in query:
            path = os.path.join(music_dir, songs[song_index])
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            speak(f"Playing {songs[song_index]}")

        elif 'next song' in query or 'next' in query:
            song_index = (song_index + 1) % len(songs)
            path = os.path.join(music_dir, songs[song_index])
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            speak(f"Playing {songs[song_index]}")

        elif 'previous song' in query or 'previous' in query:
            song_index = (song_index - 1) % len(songs)
            path = os.path.join(music_dir, songs[song_index])
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            speak(f"Playing {songs[song_index]}")

        elif 'stop song' in query:
            pygame.mixer.music.stop()
            speak("Music stopped")

        elif 'time' in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {current_time}")

        elif 'open vs code' in query or 'code' in query:
            path = "C:\\Program Files\\Microsoft VS Code\\Code.exe"
            os.startfile(path)

        elif 'send email' in query or 'email send' in query:
            try:
                speak("Who do you want to send the email to?")
                name = takeCommand()
                if name is None : 
                  name = input("Entet the command : ").lower()
                  print(f"Processing the text input : {name}") 

                if name in contacts:
                    to = contacts[name]
                    speak("What should I say?")
                    content = takeCommand()
                    if content is None :
                       content = input("Enter the text which you want to send :")
                       print(f"Processing the text input : {content}")
                    sendEmail(to, content)
                    speak("Email has been sent!")
                else:
                    speak("I don't have an email address for that name")

            except Exception as e:
                print(e)
                speak("There was a problem sending the email")

        elif 'ai' in query or 'chatgpt' in query:
            prompt = takeCommand()
            gpt(prompt)

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye, sir.")
            break
        
        elif 'reset chat'  in query :
            chatstr = " "

        else:
            print("Chating....")
            chat(query)
          
        time.sleep(1)
