import streamlit as st
from google.cloud import speech, texttospeech
from moviepy.editor import VideoFileClip
import os

st.title("AI Audio Correction")

# File uploader
uploaded_file = st.file_uploader("Upload a Video File", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Show the uploaded video
    st.video(uploaded_file)
    
    # Save the video temporarily
    video_path = "temp_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    # Extract audio from the video
    clip = VideoFileClip(video_path)
    audio = clip.audio
    audio_path = "temp_audio.wav"
    audio.write_audiofile(audio_path)

    # Transcribe audio using Google Speech-to-Text
    def transcribe_audio(audio_file):
        client = speech.SpeechClient()
        with open(audio_file, "rb") as f:
            audio_content = f.read()
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="en-US"
        )
        response = client.recognize(config=config, audio=audio)
        return " ".join([result.alternatives[0].transcript for result in response.results])

    transcription = transcribe_audio(audio_path)
    st.write("Original Transcription:", transcription)

    # Correct transcription using GPT-40 (Assume GPT-40 is wrapped in a function)
    def correct_transcription(text):
        # Placeholder for GPT-40 API correction logic
        corrected_text = text.replace("umm", "").replace("hmm", "")  # Basic correction for demo
        return corrected_text

    corrected_transcription = correct_transcription(transcription)
    st.write("Corrected Transcription:", corrected_transcription)

    # Convert corrected text to speech using Google Text-to-Speech
    def text_to_speech(text):
        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Wavenet-D"  # Example voice, adjust as necessary
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
        return response.audio_content

    generated_audio = text_to_speech(corrected_transcription)

    # Save the generated audio
    generated_audio_path = "generated_audio.mp3"
    with open(generated_audio_path, "wb") as out:
        out.write(generated_audio)

    st.audio(generated_audio_path, format="audio/mp3")

    # Here you would add logic to sync the new audio with the video file
