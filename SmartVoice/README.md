# **SmartVoice**  
**AI-Powered Text-to-Speech & Speech-to-Text Converter**  

SmartVoice is a web-based application that leverages **AWS Transcribe** and **AWS Polly** to convert speech into text and text into speech. Users can upload audio files for transcription or generate speech from text seamlessly.  

## **Features**  
✅ Upload **.mp3** files for automatic transcription  
✅ Convert text into speech and download the audio  
✅ AWS-powered processing for high accuracy  
✅ Simple and intuitive UI with real-time feedback  
✅ Secure file storage in **AWS S3**  

## **Tech Stack**  
- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Flask (Python)  
- **Cloud Services**: AWS S3, AWS Transcribe, AWS Polly  
- **Deployment**: EC2, Gunicorn  

## **Project Structure**  
```
smartvoice-project/
│── app.py                   # Flask backend for handling requests  
│── templates/  
│   └── index.html            # Frontend UI  
│── static/  
│   ├── styles.css            # Custom styles  
│   ├── script.js             # JavaScript for frontend logic  
│── requirements.txt          # Dependencies  
│── README.md                 # Project documentation  
│── .env                      # AWS credentials & configurations  
```

## **Setup & Installation**  
### **1️⃣ Clone the Repository**  
```sh
git clone https://github.com/your-username/smartvoice.git
cd smartvoice
```

### **2️⃣ Install Dependencies**  
```sh
pip install -r requirements.txt
```

### **3️⃣ Set Up AWS Credentials**  
Create a `.env` file and add:  
```
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=your_region
S3_BUCKET_NAME=your_s3_bucket
```

### **4️⃣ Run the Flask App**  
```sh
python app.py
```
The app will be available at `http://127.0.0.1:8080`

## **Deployment**  
To deploy on an **AWS EC2 instance**, follow these steps:  
1. **Launch an EC2 instance** with Python and Flask installed  
2. **Transfer files** using SCP or Git  
3. **Install dependencies**  
   ```sh
   pip install -r requirements.txt
   ```
4. **Run the Flask app**  
   ```sh
   gunicorn --bind 0.0.0.0:8080 app:app
   ```
5. **Configure Security Groups** to allow port `8080`  

## **Usage**  
- Upload an `.mp3` file for transcription  
- View transcribed text in a pop-up  
- Download or listen to AI-generated speech  

## **Contributing**  
Feel free to submit issues, feature requests, or pull requests!  

