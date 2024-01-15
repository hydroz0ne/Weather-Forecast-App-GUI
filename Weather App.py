from tkinter import *
import time
import requests
from pygame import mixer
from datetime import datetime
from PIL import Image, ImageTk
from tkinter import messagebox
from configparser import ConfigParser

app = Tk()
app.geometry("1080x750")
app.resizable(False,False)
app.title("Weather Forecast")

#API Key Requirements
url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config["api_key"]["key"]

#Retrieves weather data for a given city using the OpenWeatherMap API.
def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        city = json["name"]
        country = json["sys"]["country"]
        temp_kelvin = json["main"]["temp"]
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9 / 5 + 32
        tempfeels_like_kelvin = json["main"]["feels_like"]
        tempfeels_like_celsius = tempfeels_like_kelvin - 273.15
        timezone = json["timezone"]
        sunrise = json["sys"]["sunrise"]
        sunset = json["sys"]["sunset"]
        humidity = json["main"]["humidity"]
        rain_info = json.get("rain", {"1h": 0})
        rain = rain_info["1h"]
        icon = json["weather"][0]["icon"]
        weather = json["weather"][0]["description"] 
        wind = json["wind"]["speed"]
        visibility = json["visibility"]

        #Convert sunrise and sunset times to local time
        sunrise_time_local = datetime.utcfromtimestamp(sunrise + timezone).strftime("%I:%M %p")
        sunset_time_local = datetime.utcfromtimestamp(sunset + timezone).strftime("%I:%M %p")

        final = (city, country, icon, weather, temp_celsius, temp_fahrenheit, tempfeels_like_celsius, timezone, 
                 sunrise_time_local, sunset_time_local, humidity, rain, wind, visibility)
        return final
    else:
        return None

#Sound mixer for background sounds
mixer.init()
def play_sound(weather_condition):
    if "rain" in weather_condition or "drizzle" in weather_condition: 
        mixer.music.load("Light Rain.mp3") 
    elif "thunderstorm" in weather_condition:
        mixer.music.load("Rain Sound.mp3") 
    elif "clear" in weather_condition:
        mixer.music.load("Clear Sound.mp3")  
    elif "cloud" in weather_condition:
        mixer.music.load("Cloudy Sound.mp3") 
    elif "snow" in weather_condition:
        mixer.music.load("Snow Sound.mp3") 
    elif "fog" in weather_condition or "mist" in weather_condition:
        mixer.music.load("Fog Sound.mp3") 
    else:
        return

    #Sets the volume and plays the background sound.
    mixer.music.set_volume(0.5)
    mixer.music.play(-1) 

#Search function
def search():
    city = city_title.get()
    weather = get_weather(city)
    if weather:
        weather_condition = weather[3].lower()

        #Update the background color of the right frame based on the weather condition
        if "rain" in weather_condition or "drizzle" in weather_condition:
            right_frame_color = "cadet blue"
        elif "clear" in weather_condition:
            right_frame_color = "powder blue"
        elif "cloud" in weather_condition:
            right_frame_color = "light steel blue"
        elif "thunderstorm" in weather_condition:
            right_frame_color = "goldenrod"
        elif "snow" in weather_condition:
            right_frame_color = "alice blue"
        elif "fog" in weather_condition or "mist" in weather_condition:
            right_frame_color = "light cyan"
        else:
            right_frame_color = rightbg_color

        #Updates the background color of the right frame and the weather_footer label
        right_frame.config(bg=right_frame_color)
        weather_footer.config(bg=right_frame_color)
            
        play_sound(weather_condition) #Plays the background sound

        city_name["text"] = "{}, {}".format(weather[0], weather[1])
        image_path = "weather_logos/{}.png".format(weather[2])

        #Weather Image Setting
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((180, 180))
        icon_image = ImageTk.PhotoImage(pil_image)
        image["image"] = icon_image
        image.image = icon_image

        #Condition & Temperatures
        city_weather["text"] = "{}".format(weather[3].capitalize())
        city_temp["text"] = "Temperature: \n{:.0f}°C, {:.0f}°F".format(weather[4], weather[5])
        city_feelslike["text"] = "Feels like {:.0f}°C".format(weather[6])

        #Timezone Setting - converts seconds to hours and format
        utc_time = "{:+.2f}".format(weather[7] / 3600)
        city_timezone["text"] = "UTC Timezone: \n{} hours".format(utc_time)

        #Sunrise, Sunset, Humidity, Rain, Wind, Visibility
        city_sunrise["text"] = "Sunrise: {}".format(weather[8])
        city_sunset["text"] = "Sunset: {}".format(weather[9])
        city_humidity["text"] = "Humidity: {}%".format(weather[10])
        city_rain["text"] = "Rain: {}%".format(weather[11])
        city_wind["text"] = "Wind: {:.0f} km/h".format(weather[12] * 3.6)
        city_visibility["text"] = "Visibility: {:.0f} km".format(weather[13] / 1000)
    else:
        messagebox.showerror("Error", "Cannot find city {}...".format(city))

# Sets background color for main app and both frames
bg_color = "gray"
leftbg_color = "light blue"
rightbg_color = "white"

#///////////////////////////////////////////////////////////////

#Left Section
left_frame = Frame(app, bg=leftbg_color, width=500, height=500, padx=10, pady=10, borderwidth=2, relief="solid")
left_frame.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nsew")

#Header, Search Bar, and Search Button
weather_header = Label(left_frame, text="Weather API", font=("bold", 16), bg=leftbg_color)
city_title = StringVar()
city_searchbar = Entry(left_frame, textvariable=city_title, width=30, bg="white")
searchbtn = Button(left_frame, text="Search City", width=15, command=search, bg="white")

weather_header.grid(row=0, column=1, pady=(10, 5), sticky="nsew")
city_searchbar.grid(row=1, column=1, pady=(5, 2), sticky="nsew")
searchbtn.grid(row=2, column=1, pady=(5, 5), sticky="nsew")

#City Details
city_name = Label(left_frame, text="City Name", font=("bold", 14), bg=leftbg_color)
image = Label(left_frame, text="Weather Image", font=("Arial", 12), bg=leftbg_color)
city_weather = Label(left_frame, text="Weather", font=("Arial", 12), bg=leftbg_color)
city_temp = Label(left_frame, text="Temperature", font=("Arial", 12), bg=leftbg_color)
city_feelslike = Label(left_frame, text="Feels like...", font=("Arial", 12), bg=leftbg_color)
city_timezone = Label(left_frame, text="Timezone", font=("Arial", 12), bg=leftbg_color)
date_time_label = Label(left_frame, text="", font=("Arial", 12), bg=leftbg_color)

image.grid(row=3, column=1, pady=30, sticky="nsew")
city_name.grid(row=4, column=1, pady=(0, 10), sticky="nsew")
city_weather.grid(row=5, column=1, pady=(0, 10), sticky="nsew")
city_temp.grid(row=6, column=1, pady=(0, 10), sticky="nsew")
city_feelslike.grid(row=7, column=1, pady=(0, 10), sticky="nsew")
city_timezone.grid(row=8, column=1, pady=(0, 10), sticky="nsew")
date_time_label.grid(row=9, column=1, pady=(0, 10), sticky="nsew")

#Updates the time and date periodically
def update_date_time():
    current_time = time.strftime('%H:%M:%S')
    formatted_date_time = datetime.now().strftime('%B %d, %Y\n') + datetime.now().strftime('%A\n') + ("Current Time: ") + current_time
    date_time_label.config(text=formatted_date_time)
    app.after(1000, update_date_time)  # Updates every 1 second

update_date_time()

#///////////////////////////////////////////////////////////////

#Right Section
right_frame = Frame(app, bg=rightbg_color, width=500, height=500, padx=10, pady=10, borderwidth=2, relief="solid")
right_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")

#Subframes for the Right Frame
f1 = Frame(right_frame, bg=bg_color, width=250, height=50)
f1.grid(row=0, column=1, pady=(0, 0))
f2 = Frame(right_frame, bg=bg_color, width=250, height=50)
f2.grid(row=0, column=2, pady=(0, 0))
f3 = Frame(right_frame, bg=bg_color, width=250, height=50)
f3.grid(row=0, column=3, pady=(0, 0))
f4 = Frame(right_frame, bg=bg_color, width=250, height=50)
f4.grid(row=1, column=1, pady=(0, 0))
f5 = Frame(right_frame, bg=bg_color, width=250, height=50)
f5.grid(row=1, column=2, pady=(0, 0))
f6 = Frame(right_frame, bg=bg_color, width=250, height=50)
f6.grid(row=1, column=3, pady=(0, 0))

#Frame for Humidity
humidphoto = PhotoImage(file="Humidity - transparent.png")
humidphoto = humidphoto.subsample(2) 
humid_label = Label(f1, image=humidphoto, bg=rightbg_color)
humid_label.grid(row=0, column=0, sticky="nsew")

city_humidity = Label(f1, text="Humidity", font=("Arial", 14), bg=rightbg_color)
city_humidity.grid(row=1, column=0, sticky="nsew") 

#Frame for Sunrise
risephoto = PhotoImage(file="Sunrise - transparent.png")
risephoto = risephoto.subsample(2)  
rise_label = Label(f2, image=risephoto, bg=rightbg_color)
rise_label.grid(row=0, column=0, sticky="nsew")

city_sunrise = Label(f2, text="Sunrise", font=("Arial", 14), bg=rightbg_color)
city_sunrise.grid(row=1, column=0, sticky="nsew") 

#Frame for Sunset
setphoto = PhotoImage(file="Sunset - transparent.png")
setphoto = setphoto.subsample(2) 
set_label = Label(f3, image=setphoto, bg=rightbg_color)
set_label.grid(row=0, column=0, sticky="nsew")

city_sunset = Label(f3, text="Sunset", font=("Arial", 14), bg=rightbg_color)
city_sunset.grid(row=1, column=0, sticky="nsew") 

#Frame for Rain
rainphoto = PhotoImage(file="Rain - transparent.png")
rainphoto = rainphoto.subsample(2) 
rain_label = Label(f4, image=rainphoto, bg=rightbg_color)
rain_label.grid(row=0, column=0, sticky="nsew")

city_rain = Label(f4, text="Rain", font=("Arial", 14), bg=rightbg_color)
city_rain.grid(row=1, column=0, sticky="nsew") 

#Frame for Wind
windphoto = PhotoImage(file="Wind - transparent.png")
windphoto = windphoto.subsample(2)  
wind_label = Label(f5, image=windphoto, bg=rightbg_color)
wind_label.grid(row=0, column=0, sticky="nsew")

city_wind = Label(f5, text="Wind", font=("Arial", 14), bg=rightbg_color)
city_wind.grid(row=1, column=0, sticky="nsew")

#Frame for Visibility
visibilityphoto = PhotoImage(file="Visibility - transparent.png")
visibilityphoto = visibilityphoto.subsample(2)  
visibility_label = Label(f6, image=visibilityphoto, bg=rightbg_color)
visibility_label.grid(row=0, column=0, sticky="nsew")

city_visibility = Label(f6, text="Visibility Level", font=("Arial", 14), bg=rightbg_color)
city_visibility.grid(row=1, column=0, sticky="nsew")

weather_footer = Label(right_frame, text="Powered by OpenWeatherAPI.", font=("Arial", 8), bg=rightbg_color)
weather_footer.grid(row=2, column=2)

#Adjusts the left frame row and column weights for resizing
left_frame.grid_columnconfigure(0, weight=1)
left_frame.grid_columnconfigure(2, weight=1)
left_frame.grid_rowconfigure(9, weight=1)

#Adjusts the right frame row and column weights for resizing
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_rowconfigure(2, weight=1)

right_frame.grid_columnconfigure(1, weight=1)
right_frame.grid_columnconfigure(2, weight=1)
right_frame.grid_columnconfigure(3, weight=1)

#Adjusts main column weights and row weights for resizing
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

app.mainloop()
