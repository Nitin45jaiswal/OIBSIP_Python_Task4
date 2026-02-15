import tkinter as tk
from tkinter import messagebox
import requests

API_KEY = "622147cd00c47bbae4673dcdd2514de2"
BASE_URL = "http://api.weatherstack.com/current"


class WeatherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App - Dark Edition")
        self.root.geometry("420x380")
        self.root.resizable(False, False)

        # Dark Theme Colors
        self.bg_color = "#0f0f0f"
        self.blue_color = "#1f6feb"
        self.text_color = "#ffffff"
        self.entry_bg = "#1c1c1c"

        self.root.configure(bg=self.bg_color)

        self.placeholder_text = "Enter city name"
        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="Weather App",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg_color,
            fg=self.blue_color
        )
        title.pack(pady=12)

        # City Entry
        self.city_entry = tk.Entry(
            self.root,
            width=28,
            font=("Segoe UI", 11),
            bg=self.entry_bg,
            fg="gray",
            insertbackground="white"
        )
        self.city_entry.pack(pady=6)
        self.city_entry.insert(0, self.placeholder_text)

        self.city_entry.bind("<FocusIn>", self.clear_placeholder)
        self.city_entry.bind("<FocusOut>", self.add_placeholder)

        tk.Button(
            self.root,
            text="Search",
            width=15,
            bg=self.blue_color,
            fg="white",
            activebackground="#1554c0",
            activeforeground="white",
            bd=0,
            command=self.fetch_weather
        ).pack(pady=8)

        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 11),
            justify="left",
            bg=self.bg_color,
            fg=self.text_color
        )
        self.result_label.pack(pady=15)

    # -------- Placeholder Handlers --------
    def clear_placeholder(self, event):
        if self.city_entry.get() == self.placeholder_text:
            self.city_entry.delete(0, tk.END)
            self.city_entry.config(fg=self.blue_color)

    def add_placeholder(self, event):
        if not self.city_entry.get():
            self.city_entry.insert(0, self.placeholder_text)
            self.city_entry.config(fg="gray")

    # -------- Weather Logic --------
    def fetch_weather(self):
        city = self.city_entry.get().strip()

        if not city or city == self.placeholder_text:
            messagebox.showerror("Input Error", "Please enter a city name.")
            return

        params = {
            "access_key": API_KEY,
            "query": city
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=10)
            data = response.json()

            if "error" in data:
                messagebox.showerror("Error", data["error"]["info"])
                return

            self.display_weather(data)

        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Unable to connect to weather service.")

    def display_weather(self, data):
        location = data["location"]
        current = data["current"]

        output = (
            f"Location   : {location['name']}, {location['country']}\n"
            f"Temperature: {current['temperature']} °C\n"
            f"Condition  : {current['weather_descriptions'][0]}\n"
            f"Humidity   : {current['humidity']}%\n"
            f"Wind Speed : {current['wind_speed']} km/h"
        )

        self.result_label.config(text=output)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherGUI(root)
    root.mainloop()
