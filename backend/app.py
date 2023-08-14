from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
origins = ["http://localhost:8080"]  # Add other allowed origins if needed
CORS(app, origins=origins, supports_credentials=True)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define a dictionary to store subtitles (in-memory storage for demonstration)
subtitles = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if video_file and allowed_file(video_file.filename):
        filename = secure_filename(video_file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video_file.save(video_path)

        return jsonify({'message': 'Video uploaded successfully'}), 200
    else:
        return jsonify({'error': 'Invalid file format'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/create_subtitle', methods=['POST'])
def create_subtitle():
    data = request.json
    video_id = data['video_id']
    subtitle_text = data['subtitle_text']
    timestamp = data['timestamp']

    if video_id not in subtitles:
        subtitles[video_id] = []

    subtitles[video_id].append({'text': subtitle_text, 'timestamp': timestamp})

    return jsonify({'message': 'Subtitle created successfully'}), 201

@app.route('/api/get_subtitles/<video_id>', methods=['GET'])
def get_subtitles(video_id):
    if video_id not in subtitles:
        return jsonify({'message': 'No subtitles available'}), 404

    return jsonify(subtitles[video_id]), 200

if __name__ == '__main__':
    app.run(debug=True)
