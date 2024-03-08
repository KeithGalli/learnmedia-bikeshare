# import pyaudio
# import audioop

from statistics import mean
import pyaudio

# # Constants for audio capture
# FORMAT = pyaudio.paInt16 # Audio format (16-bit PCM)
# CHANNELS = 1 # Mono audio
# RATE = 44100 # Sample rate
# CHUNK = 1024 # Number of audio frames per buffer

# # Initialize PyAudio
# p = pyaudio.PyAudio()

# # Open stream for audio input
# stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 input=True,
#                 frames_per_buffer=CHUNK)

# print("Recording...")

# try:
#     while True:
#         # Read raw audio data
#         data = stream.read(CHUNK)
#         # Calculate RMS volume
#         rms = audioop.rms(data, 2) # Width=2 for format=paInt16
#         print(f"Volume: {rms}")
# except KeyboardInterrupt:
#     # Stop and close the stream
#     print("\nRecording stopped.")
#     stream.stop_stream()
#     stream.close()
#     p.terminate()

def info_smoother(points):
    return mean(points)