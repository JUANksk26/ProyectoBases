import flet as ft
import pygame
import os
from mutagen.mp3 import MP3
import asyncio



class Song:
    def __init__(self, filename):
        self.filename = filename
        self.title = os.path.splitext(filename)[0]
        self.duration = self.get_duration()
    def get_duration(self): 
       audio = MP3(os.path.join("C:\\Users\\ljuan\\Documents\\Canciones", self.filename))
       return audio.info.length

    
async def main(page : ft.Page):
    page.title = "Letit"
    page.padding = 25
    page.bgcolor = "#100D16"
    titulo = ft.Text("LetItSound", color ="#EAE4F4", size = 40)
    pygame.mixer.init()
    playlist = [Song(f) for f in os.listdir("C:\\Users\\ljuan\\Documents\\Canciones") if f.endswith(".mp3")]

    def load_song():
        pygame.mixer.music.load(os.path.join("C:\\Users\\ljuan\\Documents\\Canciones", playlist[current_song_index].filename))
    
    def pause(e):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            play_button.icon = ft.Icons.PLAY_ARROW
        else:
            if pygame.mixer.music.get_pos() == -1:
                load_song()
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.unpause()
            play_button.icon = ft.Icons.PAUSE
        page.update()
    def on_keyboard(e : ft.KeyboardEvent):
        if e.key == " ":
            pause(e)    

    def change_song(x):
        nonlocal current_song_index
        current_song_index = (current_song_index + x) % len(playlist)
        load_song()
        pygame.mixer.music.play()
        update_song_info()

    def update_song_info():
        song = playlist[current_song_index]
        Song_info.value = f"{song.title}"
        duration.value = format_time(song.duration)
        progress_bar.value = 0.0
        current_time_text.value = "00:00"
        page.update()
    
    def format_time(seconds):
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    async def update_progress():
        while True:
            if pygame.mixer.music.get_busy():
               current_time = pygame.mixer.music.get_pos() /1000
               progress_bar.value = current_time / playlist[current_song_index].duration
               current_time_text.value = format_time(current_time)
               page.update()
            await asyncio.sleep(0.5)   



    current_song_index = 0
    Song_info = ft.Text(size=20, color="#EAE4F4")
    current_time_text = ft.Text("00:00",color="#EAE4F4",)
    duration = ft.Text("00:00", color="#EAE4F4")
    progress_bar = ft.ProgressBar(value=0.0, width=300, color="#EAE4F4", bgcolor="#1C1626" )
    play_button = ft.IconButton(icon=ft.Icons.PLAY_ARROW, on_click=pause, icon_color="#EAE4F4")
    prev_button = ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS,on_click=lambda e: change_song(-1), icon_color="#EAE4F4")
    next_button = ft.IconButton(icon=ft.Icons.SKIP_NEXT, on_click=lambda e: change_song(1), icon_color="#EAE4F4")
    page.on_keyboard_event = on_keyboard
    
    Controls = ft.Row(
        controls=[prev_button, play_button, next_button],
        alignment=ft.MainAxisAlignment.CENTER
    )
    Fila_reproductor = ft.Row (
        [current_time_text, progress_bar, duration],
        alignment= ft.MainAxisAlignment.CENTER
    )

    

    Columna = ft.Column([Song_info, Fila_reproductor, Controls],
             alignment=ft.MainAxisAlignment.END, 
             spacing=20,
             expand=True
             )
    

        
    
    page.add(titulo,Columna)

    if playlist:
        load_song()
        update_song_info()
        page.update()
        await update_progress()
    else:
        Song_info.value = "Nada por aquí..."    


ft.run(main)

