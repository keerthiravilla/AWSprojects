from flask import Flask, request, jsonify, render_template
import boto3
import time
import json

app = Flask(__name__)

# AWS S3 Configuration
S3_BUCKET = "text-audio-processor"
S3_POLLY_OUTPUT = "destination/polly-output/"
S3_TRANSCRIBE_OUTPUT = "destination/transcribe-output/"
s3 = boto3.client("s3")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_key = "source/" + file.filename

    try:
        # Upload file to S3 (Triggers Lambda)
        s3.upload_fileobj(file, S3_BUCKET, file_key)

        return jsonify({
            "message": "File uploaded successfully. Processing started.",
            "file_name": file.filename
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_result", methods=["GET"])
def get_result():
    file_name = request.args.get("file_name")
    if not file_name:
        return jsonify({"error": "Missing file name"}), 400

    if file_name.endswith(".txt"):
        processed_file_key = S3_POLLY_OUTPUT + file_name.replace(".txt", ".mp3")
    elif file_name.endswith(".mp3") or file_name.endswith(".wav"):
        processed_file_key = S3_TRANSCRIBE_OUTPUT + file_name.replace(".mp3", ".json").replace(".wav", ".json")
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    # Wait for S3 file (Polling)
    for _ in range(10):
        try:
            s3.head_object(Bucket=S3_BUCKET, Key=processed_file_key)
            file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{processed_file_key}"

            # If transcribed text, fetch and return it
            if file_name.endswith(".mp3") or file_name.endswith(".wav"):
                obj = s3.get_object(Bucket=S3_BUCKET, Key=processed_file_key)
                transcribed_data = json.loads(obj["Body"].read().decode("utf-8"))
                transcribed_text = transcribed_data.get("results", {}).get("transcripts", [{}])[0].get("transcript", "")

                return jsonify({"transcribed_text": transcribed_text}), 200

            return jsonify({"file_url": file_url}), 200
        except:
            time.sleep(2)

    return jsonify({"error": "Processed file not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
