import yt_dlp
# import openai
import whisper
import os
import cv2
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

#Load the Keys
OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
# Supabase Config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def upload_to_supabase(file_path, bucket_name):
    """Upload file to Supabase storage."""
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    #Selct the video file
    video_file_path = ""
    for filename in os.listdir(fr"{file_path}"):
        if filename.endswith('.mp4'):
            video_file_path = os.path.join(file_path, filename)
            print(video_file_path)
            
    file_name = os.path.basename(video_file_path)
    file_name = re.sub(r'[^a-zA-Z0-9\s]', '_', file_name)
    print("file name: ", file_name)
    with open(video_file_path, "rb") as file:
        supabase.storage.from_(bucket_name).upload(file_name, file)

def download_video(url, output_path):
    """Download video from a URL using yt-dlp."""
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path + '%(id)s/%(title)s.mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
    ydl_opts =  {'extract_audio': True, 'format': 'bestaudio', 'outtmpl': output_path + '%(id)s/%(title)s.mp3'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    info_dict = ydl.extract_info(url, download=False)
    # print(info_dict)
    return output_path + info_dict['id']
     

def transcribe_video(file_path):
    """Transcribe video using OpenAI Whisper."""    
       
    #Selct the MP3 audio file
    audio_file_path = ""
    for filename in os.listdir(fr"{file_path}"):
        if filename.endswith('.mp3'):
            audio_file_path = os.path.join(file_path, filename)
            print(audio_file_path)

    # Load the model
    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path)
    # print(result)
    
    #clean up 
    text_with_timestamps = []
    # Extract sentences and timestamps
    for segment in result['segments']:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text'].strip()  
        text_with_timestamps.append({"start": start_time, "end": end_time, "text": text})
    print(text_with_timestamps)
    return text_with_timestamps

def extract_clips(video_path, clips, output_dir):
    """Extract clips based on the transcript"""
    video = cv2.VideoCapture(video_path)
    
    for i, (start, end) in enumerate(clips):
        output_clip = os.path.join(output_dir, f"clip_{i}.mp4")
        save_clip(video, start, end, output_clip)

def save_clip(video, start_time, end_time, output_path):
    """Save a clip from the video between start_time and end_time."""
    fps = video.get(cv2.CAP_PROP_FPS)
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    frame_count = start_frame
    out = None
    
    while frame_count <= end_frame:
        ret, frame = video.read()
        if not ret:
            break
        
        if out is None:
            # Define the codec and create VideoWriter object
            height, width = frame.shape[:2]
            out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
        
        out.write(frame)
        frame_count += 1
    
    if out:
        out.release()

def main():
    # Example URLs to test
    test_urls = [
        "https://www.youtube.com/watch?v=c0m6yaGlZh4"
    ]

    # Create output directories
    os.makedirs("videos", exist_ok=True)
    os.makedirs("clips", exist_ok=True)

    for url in test_urls:
        # Step 1: Download the video
        output_path = fr"videos/"
        output_path = download_video(url, output_path)

        # Step 2: Transcribe the video
        transcript = transcribe_video(output_path)
        
        # Step 3: Extract the Most Valuable Information (MVI) from the content
        #Make an Open AI Call and get the MVI in JSON format
        # prompt = Below is an audio transcribed with start and end timestamps for the corresponding text. 
        # Give the most valuable information from the below text content and their corresponding timestamps in JSON format (Use the JSON mode of gpt-4o to guarantee a valid JSON):
        # ### (The Transcribe from whisper modle)
        mvi_clips = [
                {
                    "start": 18.86,
                    "end": 23.6,
                    "text": "What is artificial intelligence and what can AI actually do?"
                },
                {
                    "start": 23.6,
                    "end": 29.98,
                    "text": "AI involves using computers to do things that usually require human intelligence."
                },
                {
                    "start": 55.48,
                    "end": 61.28,
                    "text": "AI algorithms identify patterns, make predictions, and recommend actions."
                },
                {
                    "start": 63.28,
                    "end": 68.54,
                    "text": "Artificial intelligence is already all around us, but today's best AI still can't compete with the human brain in some ways."
                },
                {
                    "start": 70.88,
                    "end": 76.48,
                    "text": "In 2016, the computer program AlphaGo defeated a legendary professional Go player."
                },
                {
                    "start": 86.24,
                    "end": 91.76,
                    "text": "AI's computing power is massive, but our human brains can tackle a much wider set of data and methods."
                }
            ]


        # Step 4: Extract clips based on the llm response
        clips = [(item['start'], item['end']) for item in mvi_clips]
        # print(clips)
        extract_clips(output_path, clips, "clips")

        # Step 5: Upload the source video and clips to Supabase
        upload_to_supabase(output_path, "madvision.ai")
        for clip in os.listdir("clips"):
            upload_to_supabase(os.path.join("clips", clip), "madvision.ai")

if __name__ == "__main__":
    main()
