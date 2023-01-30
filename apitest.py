import openai
import gtts
import json
from playsound import playsound#
from os import system

text = input("Please input your Question for ChatGPT\n")

openai.api_key = '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'
prompt = text
response = openai.Completion.create(engine="text-davinci-001", prompt=prompt, max_tokens=1024)
# print(response)

data = json.loads(str(response))
text = data['choices'][0]['text'].replace("\n", "")
print(text)
# make request to google to get synthesis
print("say {}".format(text))
system("say {}".format(text))
print('Seesh')
# # save the audio file
# tts.save("audio.mp3")
# # play the audio file
# playsound("audio.mp3")
