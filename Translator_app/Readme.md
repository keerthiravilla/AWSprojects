# Voice Translation App

## Overview
This project is a Translation App that enables seamless communication across different languages using AWS services. By integrating AWS Lambda, Amazon Translate, and Amazon Polly, the app translates user input in real-time and provides audio output of the translated text.

## Key Features
- Real-time translation of text input.
- Audio output of translated text.
- User-friendly interface for input and target language selection.

## Architecture
The app utilizes the following AWS services:
- **AWS Lambda**: Handles the logic for translating text and converting it to speech.
- **Amazon Translate**: Translates input text into the desired language.
- **Amazon Polly**: Converts the translated text into speech.
- **Amazon S3**: Stores the generated audio files.
- **API Gateway**: Facilitates communication between the frontend and the backend Lambda function.

## Prerequisites
- An active AWS account.
- Basic knowledge of AWS services and the AWS Management Console.

## Step-by-Step Instructions

### Step 1: Set Up AWS Account
- Sign up for an AWS account on the [AWS Free Tier](https://aws.amazon.com/free/).

### Step 2: Create an S3 Bucket
1. Navigate to the S3 service in the AWS Management Console.
2. Create a new bucket with a unique name (e.g., `voice-translation-bucket-keerthi`).
3. Configure the permissions and enable CORS as needed.

### Step 3: Create the Lambda Function
1. Navigate to the Lambda service in the AWS Management Console.
2. Create a new function and set the runtime to Python 3.8 (or your preferred language).
3. Add the necessary permissions for accessing Amazon Translate, Amazon Polly, and the S3 bucket.
4. Insert the Lambda function code to manage translations and audio output.

### Step 4: Set Up API Gateway
1. Navigate to the API Gateway service.
2. Create a new REST API and set up a resource for translation.
3. Create a POST method that triggers the Lambda function.
4. Deploy the API to make it accessible.

### Step 5: Testing the Application
- Use tools like Postman or curl to send POST requests to your API endpoint with the text and target language.

## Conclusion
This Voice Translation App showcases the power of AWS services in enabling communication across languages. By following the steps outlined in this README, you can successfully build and deploy your own voice translation application.
