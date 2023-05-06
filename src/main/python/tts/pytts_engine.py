#!/usr/bin/env python3


import os

import pyttsx3

from tts.enginebase import EngineBase
from utils import make_md5, trans_audio, savefile
from utils.language import get_language


class Pyttsx3Engine(EngineBase):

    def __init__(self, rate=200, volume=1.0, voice=None, *args, **kwargs):
        super(Pyttsx3Engine, self).__init__(rate, volume, voice, *args, **kwargs)
        self.engine = pyttsx3.init()

        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        if voice:
            self.engine.setProperty('voice', voice)
        else:
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[1].id)

        self.engine.connect('started-utterance', self.onStart)
        self.engine.connect('started-word', self.onWord)
        self.engine.connect('finished-utterance', self.onEnd)

    def onStart(self, name):
        print('starting', name)

    def onWord(self, name, location, length):
        print('word', name, location, length)

    def onEnd(self, name, completed):
        print('finishing', name, completed)

    @property
    def voice_all(self):
        voice_all = []
        for voice in self.engine.proxy._driver._tts.GetVoices():
            temp_voice = {}
            temp_voice["Name"] = voice.GetAttribute("Name")
            temp_voice["Gender"] = voice.GetAttribute("Gender")
            temp_voice["Age"] = voice.GetAttribute("Age")
            temp_voice["Language_code"] = voice.GetAttribute("Language")
            temp_voice["Language"] = get_language(temp_voice["Language_code"]).get("LCID_string", "")
            temp_voice["Vendor"] = voice.GetAttribute("Vendor")
            temp_voice["Description"] = voice.GetDescription()
            temp_voice["Id"] = voice.Id
            voice_all.append(temp_voice)
        return voice_all

    def save_to_file(self, text, filepath, rm_midfile: bool = True, save_text: bool = False):

        temp_path = filepath
        filename, suffix = os.path.splitext(filepath)
        if suffix != ".wav":
            temp_path = filename + ".wav"

        self.engine.setProperty('rate', self._rate)
        self.engine.setProperty('volume', self._volume)
        self.engine.setProperty('voice', self._voice)
        self.engine.save_to_file(text, temp_path)
        self.engine.runAndWait()
        if suffix != ".wav":
            trans_audio(temp_path, suffix.lower().strip("."))
            if rm_midfile:
                os.remove(temp_path)
        if save_text:
            savefile(text, filename + ".txt")

        return filepath

    def list_save_to_file(self, text_list: list, dirname: str):
        for text in text_list:
            text = text.strip()
            if not text:
                continue
            text_md5 = make_md5(text)
            filename = os.path.join(dirname, f"{text_md5}.mp3")
            self.save_to_file(text, filename, rm_midfile=False, save_text=True)


if __name__ == "__main__":

    # engine = pyttsx3.init()
    # voices = engine.getProperty('voices')
    # print(engine.getProperty('voice'))
    # print(engine.getProperty('volume'))
    # print(engine.getProperty('rate'))
    # print(engine.proxy._driver._tts.GetVoices())
    # for voice in engine.proxy._driver._tts.GetVoices():
    #     print(dir(voice))
    #     print(voice.GetAttribute("Name"))
    #     print(voice.GetAttribute("Gender"))
    #     print(voice.GetAttribute("Age"))
    #     print([voice.GetAttribute("Language"),])
    #     print(voice.GetAttribute("Vendor"))
    #     print(voice.Id)
    #     print(voice.GetDescription())
    #
    # engine.say("返回指定键的值，如果键不在字典中返回默认值，如果不指定默认值，则返回 None。")
    # engine.save_to_file(text="返回指定键的值，如果键不在字典中返回默认值，如果不指定默认值，则返回 None。", filename="Pyttsx.mp3")
    # engine.runAndWait()


    engine_obj = Pyttsx3Engine(voice="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0")
    voices = engine_obj.voice_all
    print(voices)
    engine_obj.say("返回指定键的值，如果键不在字典中返回默认值，如果不指定默认值，则返回 None。")
