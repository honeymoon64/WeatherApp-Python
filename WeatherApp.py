import tkinter as tk
from PIL import Image, ImageTk
import requests
import io
from WeatherManager import WeatherManager
import os
from dotenv import load_dotenv

class WeatherApp:
    def __init__(self, root, weather_manager):
        self.root = root
        self.weather_manager = weather_manager
        self.root.bind('<Return>', lambda event: self.display_weather())
        self.bg_color = "#121212"
        self.accent_color = "#00ADB5"
        self.text_color = "white"

        self.root.title("WeatherApp")
        self.root.geometry("450x300")
        self.root.configure(bg=self.bg_color)

        tk.Label(
            root, text="PODAJ MIASTO", font=("Consolas", 10, "bold"),
            bg=self.bg_color, fg=self.text_color
        ).pack(pady=(20, 5))

        self.city_entry = tk.Entry(
            root, font=("Consolas", 12), bg="#222831", fg="white",
            insertbackground="white", borderwidth=0, justify="center"
        )
        self.city_entry.pack(pady=10, ipady=5)

        self.check_button = tk.Button(
            root, text="SPRAWDŹ", command=self.display_weather(),
            bg=self.accent_color, fg="white", font=("Consolas", 9, "bold"),
            padx=15, pady=5, bd=0, cursor="hand2"
        )
        self.check_button.pack(pady=10)

        self.results_frame = tk.Frame(root, bg=self.bg_color)
        self.results_frame.pack(pady=20, padx=20, anchor="center")
        self.icon_label = tk.Label(self.results_frame, bg=self.bg_color)
        self.icon_label.pack(side="left")
        self.info_text_frame = tk.Frame(self.results_frame, bg=self.bg_color)
        self.info_text_frame.pack(side="left", padx=15)

        self.result_label = tk.Label(
            self.results_frame,
            font=("Consolas", 12, "bold"),
            fg=self.text_color,
            bg=self.bg_color,
            justify="left"
        )
        self.result_label.pack(anchor="w")
        self.air_label = tk.Label(
            self.results_frame,
            font=("Consolas", 12, "bold"),
            fg=self.text_color,
            bg=self.bg_color,
            justify="left"
        )
        self.air_label.pack(anchor="w")

    def display_weather(self, event=None):
        miasto = self.city_entry.get()
        dane = self.weather_manager.get_weather(miasto)

        if dane:
            opis_aqi, kolor_aqi = self.weather_manager.get_air_quality(dane['lat'], dane['lon'])
            try:
                icon_url = f"https://openweathermap.org/img/wn/{dane['icon_code']}@2x.png"
                response = requests.get(icon_url, stream=True)
                if response.status_code == 200:
                    img = Image.open(io.BytesIO(response.content))
                    photo = ImageTk.PhotoImage(img)
                    self.icon_label.config(image=photo)
                    self.icon_label.image = photo
            except:
                self.icon_label.config(image='', text="☁️")

            wynik_tekst = (
                f"    {miasto.upper()}\n"
                f"Temperatura: {dane['temp']}°C\n"
                f"{dane['opis'].capitalize()}\n"
                f"Wilgotność: {dane['wilgotnosc']}%"
            )
            self.result_label.config(text=wynik_tekst)
            aqi_info = f"Powietrze: {opis_aqi}"
            self.air_label.config(text=aqi_info)
            self.air_label.config(fg=kolor_aqi)
        else:
            self.icon_label.config(image='', text="")
            self.result_label.config(text="❌ Nie znaleziono miasta!", fg="#e74c3c")
            self.air_label.config(text="")
if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("WEATHER_API_KEY")
    root = tk.Tk()
    manager = WeatherManager(api_key)
    app = WeatherApp(root, manager)

    root.mainloop()