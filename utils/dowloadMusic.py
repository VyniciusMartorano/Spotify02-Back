from pytube import YouTube
import os
  

def dowloadMusic(musica):
    yt = YouTube(musica)
    video = yt.streams.filter(only_audio=True).first()
    output_path=r'C:\Users\VYNICIUS MARTORANO\Downloads\musicas'
    out_file = video.download(output_path)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file

