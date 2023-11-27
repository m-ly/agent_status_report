# app.py
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from status_report import format_report, set_working_file
import os

app = Flask(__name__)

def process_files_and_generate_links(files):
    output_path = 'static/output/'
    os.makedirs(output_path, exist_ok=True)

    # Process and format the files using your custom format_report function
    excel_files = format_report(files, output_path)

    # Render a template with links to download the processed files
    return render_template('success_multiple.html', excel_files=excel_files)

@app.route('/', methods=['GET', 'POST'])
def process_files():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files[]')
        if uploaded_files:
            # Process the files and generate links
            return process_files_and_generate_links(uploaded_files)

    # Render the upload form
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
