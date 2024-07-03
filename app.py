from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import boto3
import json
from io import BytesIO

app = Flask(__name__)
socketio = SocketIO(app)

# Configure your AWS S3 bucket
S3_BUCKET = 'cadas-testing-data'

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('navigate')
def handle_navigate(path):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=path, Delimiter='/')
    
    directories = []
    files = []

    if 'CommonPrefixes' in response:
        directories = [prefix['Prefix'] for prefix in response['CommonPrefixes']]
    
    if 'Contents' in response:
        files = [obj['Key'] for obj in response['Contents'] if obj['Key'] != path]

    emit('update_files', {'directories': directories, 'files': files, 'path': path})

@app.route('/file_content', methods=['GET'])
def file_content():
    file_key = request.args.get('file_key')
    s3_client = boto3.client('s3')
    file_obj = s3_client.get_object(Bucket=S3_BUCKET, Key=file_key)
    file_content = file_obj['Body'].read()

    if file_key.endswith('.json'):
        file_content = json.loads(file_content.decode('utf-8'))
        return jsonify(file_content)
    elif file_key.endswith('.wav'):
        return send_file(BytesIO(file_content), mimetype='audio/wav')

if __name__ == '__main__':
    socketio.run(app, debug=True)
