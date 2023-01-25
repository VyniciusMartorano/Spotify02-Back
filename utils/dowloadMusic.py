from pytube import YouTube
import os


def dowloadMusic(urlMusic: str, output_path: str, filename: str) -> str:
    parcial_file_full_path = f'{output_path}/{filename}.mp3'

    if os.path.isfile(parcial_file_full_path): raise FileExistsError
    yt = YouTube(url=urlMusic)

    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=output_path, filename=filename)
    base, extension = os.path.splitext(out_file)
    
    new_file_path = base + '.mp3'
    os.rename(out_file, new_file_path)
    return new_file_path

