# app.py
  
from shiny import reactive
from shiny.express import input, ui, render
from shinywidgets import render_widget
from shiny import reactive
from faicons import icon_svg as icon
from phoenix import info_smoother
import time

import shared
from helpers import show_city, show_trend

import pyaudio
import audioop

# Constants for audio capture
FORMAT = pyaudio.paInt16 # Audio format (16-bit PCM)
CHANNELS = 1 # Mono audio
RATE = 1000 #44100 # Sample rate
CHUNK = 2000 # Number of audio frames per buffer

ui.page_opts(title="Bikeshare availability in three cities", )

p = pyaudio.PyAudio()

# Open stream for audio input
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

with ui.sidebar():
    ui.input_radio_buttons(  
        "city",  
        "Select a city:",  
        {"austin": "Austin", "chicago": "Chicago", "dc": "Washington DC"}, 
        selected = "dc"   
    )  

@reactive.calc
def bike_data():
    return shared.bikes[shared.bikes['city'] == input.city()]

@reactive.calc
def station_data():
    return shared.stations[shared.stations['city'] == input.city()]

with ui.layout_columns():

    with ui.value_box(
        showcase = icon("bicycle"),
        theme = ui.value_box_theme(bg = "#9FD8CB")
    ):
        "Bikes available"
        @render.text
        def bikes_available():
            latest_day_data = bike_data()[bike_data()['time'].dt.date == bike_data()['time'].dt.date.max()]

            n_bikes = (
              latest_day_data.groupby("time")["num_bikes_available"]
              .sum()
              .max()
            )
            print("HERE")
            print(audio_info())
            return f"{audio_info()}"
            # return f"{n_bikes:,}"
    
    with ui.value_box(
        showcase = icon("square", style="regular"),
        theme = ui.value_box_theme(bg = "#517664", fg = "#FFFFFF")
    ):
        "Average bikes available"
        @render.text
        def average_bikes_available():
            avg_bikes = bike_data()['num_bikes_available'].median().astype(int)
            return f"{avg_bikes:,}"

    with ui.value_box(
        showcase=icon("building", style="regular"),
        theme = ui.value_box_theme(bg = "#2D3319", fg = "#FFFFFF")
    ):
        "Number of stations"
        @render.text
        def number_of_stations():
            n_stations = bike_data()['station_id'].nunique()
            return f"{n_stations:,}"

with ui.layout_columns(col_widths=[5, 7]):

    with ui.card():
        ui.card_header("Station Map")
        @render_widget  
        def map():
            return show_city(stations = station_data(), size = audio_info())
            
    with ui.card():
        ui.card_header("Availability")
        @render_widget
        def line_chart():
            return show_trend(bike_data())

with ui.layout_columns():

    with ui.card():
        ui.card_header("Station information")
        @render.data_frame  
        def table():
            return render.DataTable(bike_data().head(1000))

# Volume TRACKING ====
    

# def record_audio(duration=1, samplerate=44100):
#     """Record audio for a given duration and samplerate."""
#     print("Recording...")
#     recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='float64')
#     sd.wait()  # Wait until recording is finished
#     print("Recording done.")
#     return recording

# def calculate_volume(audio_data):
#     """Calculate the RMS volume of the recorded audio."""
#     rms = np.sqrt(np.mean(audio_data**2))
#     return 20 * np.log10(rms)

# Record a short audio sample
# duration = 1  # seconds
# samplerate = 44100  # Hz
# audio_data = record_audio(duration, samplerate)



@reactive.calc
def audio_info():
    """The current volume level"""
    # Read raw audio data
    reactive.invalidate_later(2)
    data = stream.read(CHUNK)
    # Calculate RMS volume
    rms = audioop.rms(data, 2) # Width=2 for format=paInt16
    print(rms)
    # stream.close()
    return rms



# The raw data is a little jittery. Smooth it out by averaging a few samples
# @reactive_smooth(n_samples=5, smoother=info_smoother)
# @reactive.calc
# def smooth_camera_info():
#     return camera_info()


@reactive.effect
def update_plotly_camera():
    """Update Plotly camera using the hand tracking"""
    # info = smooth_camera_info() if input.use_smoothing() else camera_info()
    info = audio_info()
    return info
