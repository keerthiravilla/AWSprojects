import json
import boto3

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
    audio_url = text_to_speech(translated_text, target_language)
    
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
        SourceLanguageCode='auto',
        TargetLanguageCode=target_language
    )
    return response['TranslatedText']

def text_to_speech(translated_text, target_language):
    response = polly_client.synthesize_speech(
        Text=translated_text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    
    audio_stream = response['AudioStream']
    audio_file = '/tmp/translated_speech.mp3'
    
    with open(audio_file, 'wb') as file:
        file.write(audio_stream.read())
    
    # Upload the audio file to S3 and return the URL
    s3_client = boto3.client('s3')
    bucket_name = 'voice-translation-bucket-keerthi' #replace this with your bucket name
    audio_key = f'translated_speech_{target_language}.mp3'
    
    s3_client.upload_file(audio_file, bucket_name, audio_key)
    
    audio_url = f'https://{bucket_name}.s3.amazonaws.com/{audio_key}'
    
    return audio_url
