from app import app
import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
from .ready_report import create_ready_report
from .status_report import create_status_report
import time
import tempfile

def wait_for_files(directory, expected_count):
    start_time = time.time()
    while len(os.listdir(directory)) < expected_count:
        if time.time() - start_time > 10:  # Timeout after 10 seconds
            raise Exception("Timeout waiting for files to be ready")
        time.sleep(0.5)

@app.route('/upload', methods=['POST'])
def upload_file():

    try:
           
        script = request.form.get('script')
        with tempfile.TemporaryDirectory() as tempdir:
          DIRECTORY = './uploads'
        
        
          if request.files:
            for key in request.files:
                file = request.files[key]
                filename = secure_filename(file.filename)
                file.save(os.path.join('./uploads', filename))
            
                # print(f"Saved file: {filename}, Exists: {os.path.exists(os.path.join(DIRECTORY, filename))}")

            # Ensure all files are saved before processing
            wait_for_files(DIRECTORY, len(request.files))
            
                
            if script == 'ready':
                create_ready_report(DIRECTORY)
            else:
                create_status_report(DIRECTORY)
            

        return jsonify({"status": 1})
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({"status": 0})
