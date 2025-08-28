# Voice.py
import sounddevice as sd
import numpy as np
import io
import wavio

# Voice_Sound_Recorder
# 8/15/2025
# AUX-441


class Sound_Voice:

    @staticmethod
    def get_loopback_device():
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            name = dev['name'].lower()
            if 'loopback' in name or 'stereo mix' in name:
                print(f"Using device: {dev['name']}")
                return i
        print("[-] No loopback device found, using default input.")
        return None

    @staticmethod
    def record_system_audio(duration=20, samplerate=44100):
        device_id = Sound_Voice.get_loopback_device()

        print(f"Recording for {duration} seconds...")
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype='int16',
                           device=device_id)
        sd.wait()

        buffer = io.BytesIO()
        wavio.write(buffer, recording, samplerate, sampwidth=2)
        buffer.seek(0)

        print("Recording finished.")
        return buffer.getvalue()


if __name__ == "__main__":
    audio_bytes = Sound_Voice.record_system_audio(duration=20)
    print(f"Recorded {len(audio_bytes)} bytes")
