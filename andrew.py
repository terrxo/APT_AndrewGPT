import openai
import gtts
import json
from playsound import playsound#
from os import system
import argparse
import queue
import sys
import sounddevice as sd
import pprint

from vosk import Model, KaldiRecognizer

def apitalk(text):
	print("Input: \n" + text +  "\n")
	openai.api_key = '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'
	prompt = text
	response = openai.Completion.create(engine="text-davinci-001", prompt=prompt, max_tokens=1024)
	# print(response)
	data = json.loads(str(response))
	text = data['choices'][0]['text'].replace("\n", "")
	print("Chat GPT: \n" + text)
	say(text)

def say(text):
	system(f"""say {text}""")

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    # if status:
        # print(status, file=sys.stderr)
    q.put(bytes(indata))

def tts():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-l", "--list-devices", action="store_true",help="show list of audio devices and exit")
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        # print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter,parents=[parser])
    parser.add_argument("-f", "--filename", type=str, metavar="FILENAME",help="audio file to store recording to")
    parser.add_argument("-d", "--device", type=int_or_str,help="input device (numeric ID or substring)")
    parser.add_argument("-r", "--samplerate", type=int, help="sampling rate")
    parser.add_argument("-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
    args = parser.parse_args(remaining)

    try:
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, "input")
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info["default_samplerate"])
        
        if args.model is None:
            model = Model(lang="en-us")
        else:
            model = Model(lang=args.model)

        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None

        with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
            print("#" * 80)
            # print("Press Ctrl+C to stop the recording")
            # print("#" * 80)

            rec = KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    # print(rec.Result())
                    data = json.loads(rec.Result())
                    api_text = data['text']
                    # print("tts: " + api_text)
                    return(api_text)
                # else:
                    # print(rec.PartialResult())
                if dump_fn is not None:
                    dump_fn.write(data)

    except KeyboardInterrupt:
        print("\nDone")
        parser.exit(0)
    except Exception as e:
         parser.exit(type(e).__name__ + ": " + str(e))

def andrew():
     while True:
        speech = tts()
        print("print " + speech)
        if 'andrew' in speech:
            print("Input: \n" + speech + "\n")
            apitalk(speech)
        elif 'tim' in speech:
            print("Input: \n" + speech + "\n")
            apitalk("answer me like i am a five year old " + speech)
        elif 'exit' in speech:
            exit()
        else:
            apitalk(speech)
        print("#" * 80)

def looptts():
    while True:
        text = tts()
        # print("text " + text)

andrew()
# say("Hello World")
# apitalk("Say Hello World")