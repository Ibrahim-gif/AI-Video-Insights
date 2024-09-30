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
```
### Enhancements

### Enhance Video Clip Output Based on Transcript Analysis

**Overview:** Improve video clip extraction using transcript analysis and additional logical processes.

**Key Strategies:**
1. **Keyword-Based Clip Selection**
   - Identify key topics or keywords in the transcript for relevant clips using NLP techniques.
   - Implement a function `extract_keywords` to extract top N keywords and their timestamps.

2. **Contextual Clipping**
   - Capture clips around identified keywords for enhanced meaning with a context window (e.g., 30 seconds before and after each keyword).

3. **Sentiment Analysis**
   - Prioritize clips exhibiting strong emotional content using the `get_sentiment` function to compute sentiment polarity.

4. **Speaker Focus**
   - Ensure clips prominently feature the main speaker through audio and video analysis.

5. **Scene Change Detection**
   - Maintain visual coherence by detecting significant scene changes using video analysis libraries like OpenCV.

**Implementation Functions:**
- `extract_keywords`: Extracts top N keywords (noun phrases) from the transcript.
- `get_sentiment`: Computes sentiment polarity for each segment, filtering based on a defined threshold.
- `identify_clip_timestamps`: Identifies segments with keywords and sufficient sentiment.
- `mock_segments`: Mocks transcript segmentation into timed segments.
- `extract_clips`: Integrates keyword extraction and sentiment analysis for clip determination.
- **Uploading Clips**: Clips are uploaded to Supabase storage, ensuring only valuable content is retained.

**Next Steps:**
- Integrate accurate timestamps to enhance clip extraction precision.
- Adjust context windows dynamically based on keyword density.
- Implement audio analysis techniques for speaker detection.
- Incorporate video quality assessments to filter low-quality clips.

### Enhance the Workflow Using Algorithms to Make Clips More Valuable

**Enhancements:**
1. **Metadata Enrichment**
   - Automatically generate descriptive metadata (titles, tags) for improved searchability.
   - Utilize OpenAI's GPT models for title and tag generation based on the clip transcript.

2. **Clustering and Categorization**
   - Group similar clips to enhance user navigation through the content library using clustering algorithms (e.g., K-Means).

3. **Recommendation System**
   - Suggest clips based on user viewing history or preferences through collaborative filtering or content-based algorithms.

4. **Quality Assessment**
   - Evaluate and score clip quality based on visual and audio features using computer vision and audio analysis libraries.

5. **Duplicate Detection**
   - Identify and remove duplicate or similar clips to maintain high-quality content.

**Explanation of Enhancements:**
1. **Metadata Enrichment**
   - Functions:
     - `generate_metadata`: Generates concise titles and relevant tags based on clip transcripts.
     - `enrich_metadata`: Iterates through all clips to generate and save metadata in JSON format.

2. **Clustering and Categorization**
   - Functions:
     - `load_transcripts`: Prepares transcripts for clustering.
     - `cluster_clips`: Applies TF-IDF vectorization and K-Means clustering.
     - `categorize_clips`: Integrates loading and clustering, saving results in JSON.

3. **Workflow Integration**
   - Function:
     - `main`: Processes clips and generates transcripts, enriches metadata, and categorizes clips.

**Next Steps for Task 2:**
- Develop a recommendation engine based on user interactions.
- Incorporate video and audio quality checks.
- Implement similarity metrics to identify and eliminate duplicates.
- Collect user feedback to enhance clip selection and categorization.

## Conclusion

This project aims to streamline video processing while ensuring the extraction of valuable content and enhancing user engagement through metadata enrichment and intelligent categorization. Future enhancements will further improve the workflow's efficiency and effectiveness.
