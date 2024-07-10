from flask import Flask, render_template, request, jsonify, send_file, redirect, request, send_from_directory
from flask_socketio import SocketIO, emit
import boto3
import json
from io import BytesIO
import pandas as pd
import os

FILES_DIRECTORY = 'static/'

app = Flask(__name__)
socketio = SocketIO(app)

# Configure your AWS S3 bucket
S3_BUCKET = 'cadas-testing-data'
S3_PREFIX = 'data/'  # Set this to the specific directory you want to list from


@app.route('/')
def red():
    return redirect('/home')

@app.route('/home')
def homepage():
    return render_template('home.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/dataset')
def index():
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    try:
        # Ensure the file path is safe
        safe_path = os.path.join(FILES_DIRECTORY, filename)
        print(safe_path)
        return send_file(safe_path, as_attachment=True)
    except FileNotFoundError:
        print(filename)
        return "File not found!", 404

@socketio.on('navigate')
def handle_navigate(path):
    s3_client = boto3.client('s3')
    full_prefix = f'{S3_PREFIX}{path}'
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=full_prefix, Delimiter='/')
    
    directories = []
    files = []
    total_files = 0

    if 'CommonPrefixes' in response:
        directories = [prefix['Prefix'][len(S3_PREFIX):] for prefix in response['CommonPrefixes']]
    
    if 'Contents' in response:
        total_files = len(response['Contents']) - 1  # subtracting 1 because of the prefix itself
        files = [obj['Key'][len(S3_PREFIX):] for obj in response['Contents'] if obj['Key'] != full_prefix]
        files = files[:200]  # limit to the first 200 files

    emit('update_files', {'directories': directories, 'files': files, 'path': path, 'total_files': total_files})

@app.route('/file_content', methods=['GET'])
def file_content():
    file_key = request.args.get('file_key')
    full_key = f'{S3_PREFIX}{file_key}'
    s3_client = boto3.client('s3')
    file_obj = s3_client.get_object(Bucket=S3_BUCKET, Key=full_key)
    file_content = file_obj['Body'].read()

    if file_key.endswith('.json'):
        file_content = json.loads(file_content.decode('utf-8'))
        return jsonify(file_content)
    elif file_key.endswith('.wav'):
        return send_file(BytesIO(file_content), mimetype='audio/wav')

@app.route('/test')
def render_test():
    return render_template('test.html')

@app.route('/data')
def data():
    # Read CSV file
    df = pd.read_csv('/home/loganb/Programs/proj/cadas-web-app/Classsifications.csv', encoding='utf-8-sig')
    
    # Group by date and category
    grouped = df.groupby(['time per 12 hours', 'events.classifications.keyword: Descending'])['Number of audio clips'].sum().unstack(fill_value=0).reset_index()
    
    # Prepare data for Plotly
    chart_data = {
        'dates': grouped['time per 12 hours'].tolist(),
        'categories': grouped.columns[1:].tolist(),
        'values': [grouped[category].tolist() for category in grouped.columns[1:]]
    }
    return jsonify(chart_data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
