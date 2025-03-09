import boto3
import json
import os

s3 = boto3.client("s3")
transcribe = boto3.client("transcribe")
polly = boto3.client("polly")

S3_BUCKET = "text-audio-processor"
S3_SOURCE_FOLDER = "source/"
S3_TRANSCRIBE_OUTPUT = "destination/transcribe-output/"
S3_POLLY_OUTPUT = "destination/polly-output/"

def lambda_handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        file_key = record['s3']['object']['key']
        
        print(f"File uploaded: {file_key}")
        
        # Check file type
        if file_key.endswith((".mp3", ".wav")):
            return process_audio_file(bucket_name, file_key)
        elif file_key.endswith(".txt"):
            return process_text_file(bucket_name, file_key)
        else:
            print("Unsupported file type")
            return {
                "statusCode": 400,
                "body": json.dumps("Unsupported file type")
            }

# 🔹 Speech-to-Text: Process audio files using AWS Transcribe
def process_audio_file(bucket, file_key):
    job_name = file_key.split("/")[-1].split(".")[0]
    file_uri = f"s3://{bucket}/{file_key}"

    try:
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": file_uri},
            MediaFormat=file_key.split(".")[-1],
            LanguageCode="en-US",
            OutputBucketName=bucket,
            OutputKey=S3_TRANSCRIBE_OUTPUT + job_name + ".json"
        )
        print(f"Transcription started for {file_key}")
        return {"statusCode": 200, "body": "Transcription job started"}
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": json.dumps(str(e))}

# 🔹 Text-to-Speech: Process text files using AWS Polly
def process_text_file(bucket, file_key):
    obj = s3.get_object(Bucket=bucket, Key=file_key)
    text_data = obj['Body'].read().decode("utf-8")
    
    try:
        response = polly.synthesize_speech(
            Text=text_data,
            OutputFormat="mp3",
            VoiceId="Joanna"
        )

        output_file_key = S3_POLLY_OUTPUT + file_key.split("/")[-1].replace(".txt", ".mp3")

        s3.put_object(Bucket=bucket, Key=output_file_key, Body=response['AudioStream'].read())
        
        print(f"Polly synthesis completed. Output: {output_file_key}")
        return {"statusCode": 200, "body": "Polly conversion completed"}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": json.dumps(str(e))}
