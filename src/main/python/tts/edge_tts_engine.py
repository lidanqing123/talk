#!/usr/bin/env python3


import os
import asyncio

import edge_tts
from edge_tts import VoicesManager

from utils import make_md5, trans_audio, savefile

from tts.enginebase import EngineBase


class EdgeTtsEngine(EngineBase):

    def __init__(self, rate: str = "+0%", volume: str = "+0%", voice=None, *args, **kwargs):
        """

        :param rate:
        :param volume:
        :param voice:
        """
        super(EdgeTtsEngine, self).__init__(rate, volume, voice, *args, **kwargs)

        self.VoicesManager = VoicesManager()
        self.VoicesManager = asyncio.get_event_loop().run_until_complete(self.VoicesManager.create())

    @property
    def voice_all(self):
        return self.VoicesManager.voices

    def save_to_file(self, text, filepath, rm_midfile: bool = True, save_text: bool = False):
        temp_path = filepath
        filename, suffix = os.path.splitext(filepath)
        if suffix != ".mp3":
            temp_path = filename + ".mp3"

        communicate = edge_tts.Communicate(text, voice=self._voice, volume=self._volume, rate=self._rate)
        asyncio.get_event_loop().run_until_complete(communicate.save(temp_path))

        if suffix != ".mp3":
            trans_audio(temp_path, suffix.lower().strip("."))
            if rm_midfile:
                os.remove(temp_path)

        if save_text:
            savefile(text, filename + ".txt")

        return filename

    def list_save_to_file(self, text_list: list, dirname: str):
        for text in text_list:
            if not text:
                continue
            text_md5 = make_md5(text)
            filename = os.path.join(dirname, f"{text_md5}.wav")
            self.save_to_file(text, filename, rm_midfile=False, save_text=True)


if __name__ == "__main__":
    # # asyncio.get_event_loop().run_until_complete(_main())
    edge_tts_engine_obj = EdgeTtsEngine(voice="Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)")
    voices = edge_tts_engine_obj.voice_all
    print(voices)
    edge_tts_engine_obj.save_to_file("话不多说，我们开始！", "aaa.mp3")
