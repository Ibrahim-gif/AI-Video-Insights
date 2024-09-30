# Video Processing and Transcription Workflow

This project implements a 5-step workflow for downloading videos, transcribing audio, extracting valuable information, clipping videos, and storing the results.

## Workflow Overview

The script follows a structured 5-step process outlined below:

### 1. Video Download
The video is downloaded using the `yt_dlp` library in both audio and video formats, with a unique ID assigned to each video for identification.

### 2. Transcription
The Whisper model is used to transcribe the audio file, generating timestamps and corresponding text.

### 3. Valuable Information Extraction
Using OpenAI's API, the transcript with timestamps and text is sent to extract the most valuable information through prompt engineering techniques. The response is structured as valid JSON.

### 4. Video Clipping
The timestamps of the valuable content from the LLM response are used to clip the video accordingly.

### 5. Storage
Finally, the processed clips are uploaded to Supabase storage.

## Code Structure

The `main.py` file contains all the code necessary for the above workflow. This code is ready to be deployed as a web service, either on Render or AWS Lambda for serverless execution.

## Usage

To run the script, ensure you have the necessary dependencies installed and configure your API keys as needed.

```bash
pip install -r requirements.txt
