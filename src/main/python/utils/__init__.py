import hashlib
import os

from pydub import AudioSegment


def make_md5(text):
    m = hashlib.md5(text.encode())
    return m.hexdigest()


def savefile(text, filename):
    with open(filename, "w") as f:
        f.write(text)


def trans_audio(filepath, audio_type: str):
    """

    :param filepath:
    :param audio_type: 'mp3', 'wav', 'raw', 'ogg', 'flv'
    :return:
    """
    if audio_type not in ['mp3', 'wav', 'raw', 'ogg', 'flv']:
        raise "audio_type error"

    filename, suffix = os.path.splitext(filepath)

    out_f = ".".join([filename, audio_type])

    if suffix.lower().strip(".") == audio_type:
        return filename

    if suffix.lower() == ".wav":
        song = AudioSegment.from_wav(filepath)
    elif suffix.lower() == ".mp3":
        song = AudioSegment.from_mp3(filepath)
    elif suffix.lower() == ".raw":
        song = AudioSegment.from_raw(filepath)
    elif suffix.lower() == ".ogg":
        song = AudioSegment.from_ogg(filepath)
    elif suffix.lower() == ".flv":
        song = AudioSegment.from_flv(filepath)

    song.export(out_f, format=audio_type)
    return out_f
