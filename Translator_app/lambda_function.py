import json
import boto3
import uuid  # Import uuid for generating unique filenames

# Initialize AWS clients for Translate and Polly
translate_client = boto3.client('translate')
polly_client = boto3.client('polly')

def lambda_handler(event, context):
    # Get input from the event
    input_text = event['text']
    target_language = event['targetLanguage']
    
    # Translate the text
    translated_text = translate_text(input_text, target_language)
    
    # Convert translated text to speech
    audio_url = text_to_speech(translated_text)
    
    # Prepare response
    response = {
        'translatedText': translated_text,
        'audioUrl': audio_url
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def translate_text(text, target_language):
    response = translate_client.translate_text(
        Text=text,
        SourceLanguageCode='auto',  # Automatically detect the source language
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']

def text_to_speech(translated_text):
    response = polly_client.synthesize_speech(
        Text=translated_text,
        OutputFormat='mp3',
        VoiceId='Joanna'  # You can choose different voices
    )
    
    audio_stream = response['AudioStream']
    audio_file = f'/tmp/translated_speech_{uuid.uuid4()}.mp3'  # Generate a unique filename
    
    # Save the audio stream to a file
    with open(audio_file, 'wb') as file:
        file.write(audio_stream.read())
    
    # Upload the audio file to S3 and return the URL
    s3_client = boto3.client('s3')
    bucket_name = 'voice-translation-bucket-keerthi'  # replace with your S3 bucket name
    audio_key = f'translated_speech_{uuid.uuid4()}.mp3'  # Unique key for the uploaded file
    
    # Upload the file to S3
    s3_client.upload_file(audio_file, bucket_name, audio_key)
    
    # Generate the URL for the audio file
    audio_url = f'https://{bucket_name}.s3.amazonaws.com/{audio_key}'
    
    return audio_url
