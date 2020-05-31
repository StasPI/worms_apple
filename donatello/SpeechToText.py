# import speech_recognition as sr
#
# filename = 'recorded.wav'
# r = sr.Recognizer()
#
# with sr.AudioFile(filename) as source:
#     audio_data = r.record(source)
#     text = r.recognize_google(audio_data, language='ru-RU')
#     print(text)


import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    audio_data = r.record(source, duration=5)
    print('Record...')
    text = r.recognize_google(audio_data, language='ru-RU')
    print(text)