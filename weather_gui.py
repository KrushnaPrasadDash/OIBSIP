import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading

API_KEY = "YOUR_API_KEY_HERE"
GEO_URL = "https://api.openweathermap.org/geo/1.0/direct"
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

WEATHER_ICONS = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌫️"
}


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Weather Dashboard")
        self.geometry("520x650")
        self.minsize(480, 600)
        self.configure(bg="#1e2a3a")

        self.lat = None
        self.lon = None

        self.build_ui()

    def build_ui(self):
        top_frame = tk.Frame(self, bg="#1e2a3a")
        top_frame.pack(fill="x", padx=20, pady=15)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            top_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 13),
            bg="#2c3e50",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        search_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))
        search_entry.bind("<Return>", lambda e: self.search_location())
        search_entry.insert(0, "Enter city name")
        search_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(search_entry))

        search_btn = tk.Button(
            top_frame,
            text="Search",
            command=self.search_location,
            bg="#3498db",
            fg="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            padx=12
        )
        search_btn.pack(side="left")

        self.status_label = tk.Label(
            self,
            text="Search for a city to get started",
            font=("Segoe UI", 10),
            bg="#1e2a3a",
            fg="#95a5a6"
        )
        self.status_label.pack(pady=(0, 5))

        self.main_card = tk.Frame(self, bg="#2c3e50")
        self.main_card.pack(fill="x", padx=20, pady=10)

        self.city_label = tk.Label(
            self.main_card,
            text="--",
            font=("Segoe UI", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        self.city_label.pack(pady=(15, 0))

        self.icon_label = tk.Label(
            self.main_card,
            text="",
            font=("Segoe UI", 48),
            bg="#2c3e50",
            fg="white"
        )
        self.icon_label.pack()

        self.temp_label = tk.Label(
            self.main_card,
            text="--°C",
            font=("Segoe UI", 36, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        self.temp_label.pack()

        self.desc_label = tk.Label(
            self.main_card,
            text="",
            font=("Segoe UI", 13),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        self.desc_label.pack(pady=(0, 15))

        details_frame = tk.Frame(self.main_card, bg="#2c3e50")
        details_frame.pack(pady=(0, 15), fill="x")

        self.humidity_label = self.make_detail(details_frame, "Humidity", "--%", 0)
        self.wind_label = self.make_detail(details_frame, "Wind", "-- m/s", 1)
        self.pressure_label = self.make_detail(details_frame, "Pressure", "-- hPa", 2)
        self.feels_label = self.make_detail(details_frame, "Feels Like", "--°C", 3)

        forecast_title = tk.Label(
            self,
            text="Hourly Forecast",
            font=("Segoe UI", 12, "bold"),
            bg="#1e2a3a",
            fg="white",
            anchor="w"
        )
        forecast_title.pack(fill="x", padx=20, pady=(10, 5))

        self.hourly_frame = tk.Frame(self, bg="#1e2a3a")
        self.hourly_frame.pack(fill="x", padx=20)

        daily_title = tk.Label(
            self,
            text="5-Day Forecast",
            font=("Segoe UI", 12, "bold"),
            bg="#1e2a3a",
            fg="white",
            anchor="w"
        )
        daily_title.pack(fill="x", padx=20, pady=(15, 5))

        self.daily_frame = tk.Frame(self, bg="#1e2a3a")
        self.daily_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

    def make_detail(self, parent, title, value, col):
        frame = tk.Frame(parent, bg="#2c3e50")
        frame.grid(row=0, column=col, padx=10, sticky="n")

        title_label = tk.Label(frame, text=title, font=("Segoe UI", 9), bg="#2c3e50", fg="#95a5a6")
        title_label.pack()

        value_label = tk.Label(frame, text=value, font=("Segoe UI", 11, "bold"), bg="#2c3e50", fg="white")
        value_label.pack()

        parent.grid_columnconfigure(col, weight=1)
        return value_label

    def clear_placeholder(self, entry):
        if entry.get() == "Enter city name":
            entry.delete(0, "end")

    def search_location(self):
        city = self.search_var.get().strip()
        if not city or city == "Enter city name":
            messagebox.showwarning("Input needed", "Please type a city name first.")
            return

        if API_KEY == "YOUR_API_KEY_HERE":
            messagebox.showerror("API Key Missing", "Please set your OpenWeatherMap API key in the code.")
            return

        self.status_label.config(text="Loading...")
        thread = threading.Thread(target=self.fetch_weather, args=(city,))
        thread.start()

    def fetch_weather(self, city):
        try:
            geo_params = {"q": city, "limit": 1, "appid": API_KEY}
            geo_resp = requests.get(GEO_URL, params=geo_params, timeout=10)
            geo_data = geo_resp.json()

            if not geo_data:
                self.after(0, lambda: self.status_label.config(text="City not found."))
                return

            self.lat = geo_data[0]["lat"]
            self.lon = geo_data[0]["lon"]
            display_name = f"{geo_data[0]['name']}, {geo_data[0].get('country', '')}"

            current_params = {"lat": self.lat, "lon": self.lon, "appid": API_KEY, "units": "metric"}
            current_resp = requests.get(CURRENT_URL, params=current_params, timeout=10)
            current_data = current_resp.json()

            forecast_params = {"lat": self.lat, "lon": self.lon, "appid": API_KEY, "units": "metric"}
            forecast_resp = requests.get(FORECAST_URL, params=forecast_params, timeout=10)
            forecast_data = forecast_resp.json()

            self.after(0, lambda: self.update_ui(display_name, current_data, forecast_data))

        except requests.exceptions.RequestException:
            self.after(0, lambda: self.status_label.config(text="Network error. Check your connection."))
        except Exception:
            self.after(0, lambda: self.status_label.config(text="Something went wrong fetching the data."))

    def update_ui(self, display_name, current_data, forecast_data):
        self.status_label.config(text="")

        self.city_label.config(text=display_name)

        main_weather = current_data["weather"][0]["main"]
        description = current_data["weather"][0]["description"].title()
        temp = round(current_data["main"]["temp"])
        feels_like = round(current_data["main"]["feels_like"])
        humidity = current_data["main"]["humidity"]
        pressure = current_data["main"]["pressure"]
        wind_speed = current_data["wind"]["speed"]

        icon = WEATHER_ICONS.get(main_weather, "🌡️")
        self.icon_label.config(text=icon)
        self.temp_label.config(text=f"{temp}°C")
        self.desc_label.config(text=description)

        self.humidity_label.config(text=f"{humidity}%")
        self.wind_label.config(text=f"{wind_speed} m/s")
        self.pressure_label.config(text=f"{pressure} hPa")
        self.feels_label.config(text=f"{feels_like}°C")

        self.populate_hourly(forecast_data)
        self.populate_daily(forecast_data)

    def populate_hourly(self, forecast_data):
        for widget in self.hourly_frame.winfo_children():
            widget.destroy()

        entries = forecast_data.get("list", [])[:6]

        for entry in entries:
            time_text = entry["dt_txt"].split(" ")[1][:5]
            temp = round(entry["main"]["temp"])
            weather_main = entry["weather"][0]["main"]
            icon = WEATHER_ICONS.get(weather_main, "🌡️")

            card = tk.Frame(self.hourly_frame, bg="#2c3e50")
            card.pack(side="left", expand=True, fill="x", padx=4, pady=4)

            tk.Label(card, text=time_text, font=("Segoe UI", 9), bg="#2c3e50", fg="#95a5a6").pack(pady=(8, 2))
            tk.Label(card, text=icon, font=("Segoe UI", 18), bg="#2c3e50", fg="white").pack()
            tk.Label(card, text=f"{temp}°", font=("Segoe UI", 11, "bold"), bg="#2c3e50", fg="white").pack(pady=(2, 8))

    def populate_daily(self, forecast_data):
        for widget in self.daily_frame.winfo_children():
            widget.destroy()

        entries = forecast_data.get("list", [])
        seen_dates = {}

        for entry in entries:
            date_part = entry["dt_txt"].split(" ")[0]
            time_part = entry["dt_txt"].split(" ")[1]

            if time_part == "12:00:00" and date_part not in seen_dates:
                seen_dates[date_part] = entry

        for date_str, entry in list(seen_dates.items())[:5]:
            temp = round(entry["main"]["temp"])
            weather_main = entry["weather"][0]["main"]
            description = entry["weather"][0]["description"].title()
            icon = WEATHER_ICONS.get(weather_main, "🌡️")

            row = tk.Frame(self.daily_frame, bg="#2c3e50")
            row.pack(fill="x", pady=3)

            tk.Label(row, text=date_str, font=("Segoe UI", 10), bg="#2c3e50", fg="#bdc3c7", width=12, anchor="w").pack(side="left", padx=10, pady=8)
            tk.Label(row, text=icon, font=("Segoe UI", 16), bg="#2c3e50", fg="white").pack(side="left", padx=10)
            tk.Label(row, text=description, font=("Segoe UI", 10), bg="#2c3e50", fg="#bdc3c7", anchor="w").pack(side="left", fill="x", expand=True)
            tk.Label(row, text=f"{temp}°C", font=("Segoe UI", 11, "bold"), bg="#2c3e50", fg="white").pack(side="right", padx=10)


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
