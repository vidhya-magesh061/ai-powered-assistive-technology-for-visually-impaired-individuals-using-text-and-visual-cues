import speech_recognition as sr
import pyttsx3
from collections import Counter
import serial
import time

from text_detection import TextDetection
from scene_description import SceneDescription
from object_detection import ObjectDetection

# arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)
# time.sleep(2)

text_detector = TextDetection()
scene_describer = SceneDescription()
object_detector = ObjectDetection()
r = sr.Recognizer()
e = pyttsx3.init()
e.setProperty('rate', 130)

def speak(text):
    e.say(text)
    e.runAndWait()

# def get_distance():
#     if arduino.in_waiting > 0:
#         distance = arduino.readline().decode('utf-8').strip()
#         if distance.isdigit():
#             return int(distance)
#     return None

while True:
    distance = 100
    # print("Distance: ", distance)
    if distance and distance < 20:
        print("Warning! Obstacle detected within 20 centimeters.")
        speak("Warning! Obstacle detected within 20 centimeters.")
    else: 
        with sr.Microphone() as source:
            print("Listening...")
            audio_text = r.listen(source)
        try:
            comm = r.recognize_google(audio_text).lower()
            print("Command:", comm)
            l = comm.split()
            
            if "text" in l:
                detected_text = text_detector.text_detect()
                speak(f"The detected text is {detected_text}")
            
            elif "object" in l or "objects" in l:
                objects = object_detector.object_detect()
                
                if objects:
                    object_counts = Counter(objects)
                    speak("Listing the objects in your surroundings. There's")
                    
                    for obj, count in object_counts.items():
                        if count == 1:
                            speak(f"1 {obj}")
                        else:
                            speak(f"{count} {obj}s")
                else:
                    speak("No objects detected.")

            elif "describe" in l or "description" in l:
                description = scene_describer.scene_detect()
                speak("The requested scene description is")
                speak(description)

            elif "stop" in l:
                speak("Stopping the program.")
                break

        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            speak("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")