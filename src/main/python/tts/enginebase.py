
from abc import ABCMeta
from abc import abstractmethod
from tempfile import NamedTemporaryFile


class EngineBase(metaclass=ABCMeta):

    def __init__(self, rate, volume, voice):
        """

        :param rate:
        :param volume:
        :param voice:
        """
        self._rate = rate
        self._volume = volume
        self._voice = voice

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        self._rate = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, voice):
        self._voice = voice

    @property
    @abstractmethod
    def voice_all(self):
        pass

    def say(self, text, suffix='.mp3'):
        f = NamedTemporaryFile(delete=False, mode='wb+', suffix=suffix)
        f.close()
        filename = f.name
        self.save_to_file(text, filename)
        return filename

    @abstractmethod
    def save_to_file(self, text, filename):
        pass

    @abstractmethod
    def list_save_to_file(self, text_list, dirname):
        pass