# """
# voice recognizing part -- here
# """
# import speech_recognition as sr
# import pyttsx3 
# import time
 
# r = sr.Recognizer() 
 
# # Function to convert text to speech
# def SpeakText(command):
     
#     # engine initialization
#     engine = pyttsx3.init()
#     engine.say(command) 
#     engine.runAndWait()
     
     
 
# while(1):    
     
#     # Exception handling to handle excetions at run time
#     try:
         
#         # use the microphone as input
#         with sr.Microphone() as source2:
             
#             #adjusting for ambient noises
#             r.adjust_for_ambient_noise(source2, duration=0.2)
             
#             #to give user time to get ready
#             time.sleep(3)

#             #text to indicate to prompt the user to speak
#             print("Please say your move")
#             SpeakText("Please say your move")

#             #listens for the user's input 
#             audio2 = r.listen(source2)
             
#             # Using google to recognize audio
#             notation = r.recognize_google(audio2)
#             notation = notation.lower()
            
 
#             print("Did you say ",notation)
#             SpeakText("Did you say")
#             SpeakText(notation)
            
#             #confirming the move that was played
#             SpeakText("Please say confirm if you want to proceed with")
#             SpeakText(notation)
#             SpeakText("otherwise say no to correct your move")

#             print(f"Please say confirm if you want to proceed with {notation} otherwise say no to correct your move")

#             audio2 = r.listen(source2)
#             confirm = r.recognize_google(audio2)

#             if confirm == "confirm":
#                 notations = notation.split(" to ")
#             elif confirm == "exit":
#                 exit()
#             else:
#                 voiceCom()

#             print(notation)

#     except sr.RequestError as e:
#         print("Could not request results; {0}".format(e))
         
#     except sr.UnknownValueError:
#         print("unknown error occurred")
        
    