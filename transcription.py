# ### Audio Transcription and Translation Script

# This Python script processes `.ogg` audio files from the `audios/` directory, transcribes them using OpenAI's Whisper model, translates the transcription into English, and saves the result as a JSON file.  

# #### How It Works:
# 1. Fetches API Key – Retrieves the OpenAI API key from environment variables.  
# 2. Finds Audio Files – Searches for `.ogg` files in the `audios/` folder.  
# 3. Transcribes Audio – Uses the Whisper model (`whisper-1`) to convert speech to text.  
# 4. Processes with GPT – Translates the transcription into English and formats it into a JSON document.  
# 5. Saves Output – Creates a JSON file with the translated text and the original audio file’s timestamp.  

# Each audio file generates a separate JSON file named after its recording date.  



from openai import OpenAI
import os
import glob
import whatsapp_utils

key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key = key)

pattern = "audios/*.ogg"

ogg_files = glob.glob(pattern)


# Create one JSON file for each audio file transcription
for file_name in ogg_files:
    file_datetime = whatsapp_utils.extract_datetime_from_filename(file_name)
    print(f"Processing {file_name}")
    audio_file = open(file_name, "rb")
    transcription = client.audio.transcriptions.create(
        model = "whisper-1",
        response_format="text",
        file = audio_file,
        temperature = 0.2,
        prompt = "Mister Jack"
    )
    
    moderations_response = client.moderations.create(input = transcription)
    if (moderations_response.results[0].flagged):
        print("ALERT!")
        print(transcription)
        break
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            { "role":"system", "content":"You are a helpful assistant."},
            { "role":"user", "content":
            f"""
            Translate into English the following text that is surrounded by 3 stars (***).
            Create a JSON document with the following elements:
            - {file_datetime.date()}. Put the translated text here.
            - audiofile_datetime. The value must be: {file_datetime}
            ***
            {transcription}
            ***
            """
            }
        ], response_format={"type":"json_object"}
    )

    with open(f"{file_datetime.date()}.json", "w") as file:
        file.write(completion.choices[0].message.content)

    print("Done!")
    
    

