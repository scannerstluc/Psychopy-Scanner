from flask import Flask, render_template, request, jsonify
import subprocess
import sys

app = Flask(__name__)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/mypsycho')
def psychopy_utilities():
    subprocess.run([sys.executable, 'psychopy_runner.py'])
    return render_template('index.html')


@app.route('/submit-data', methods=['POST'])
def submit_data():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        words = data.get('words')
        zoom = data.get('zoom')
        file = data.get('filePath')
        output_file = data.get('output_file')
        subprocess.run([
            sys.executable, 'psychopy_runner.py',
            '--duration', duration,
            '--words', words,
            '--file', file,
            '--output_file', output_file,
            '--zoom', zoom
        ])

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/submit-images', methods=['POST'])
def submit_images():
    try:
        data = request.get_json()
        duration = data.get('duration')
        file = data.get('filePath')
        zoom = data.get('zoom')
        betweenstimuli = data.get('betweenstimuli')
        output_file = data.get('output_file')
        subprocess.run([
            sys.executable, 'image_opti.py',
            '--duration', duration,
            '--file', file,
            '--output_file', output_file,
            '--betweenstimuli', betweenstimuli,
            '--zoom', zoom
        ])

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-videos', methods=['POST'])
def submit_videos():
    try:
        data = request.get_json()
        print(data)
        duration = data.get('duration')
        file = data.get('filePath')
        zoom = data.get('zoom')
        betweenstimuli = data.get('betweenstimuli')
        output_file = data.get('output_file')
        print(zoom)
        print(betweenstimuli)
        subprocess.run([
            sys.executable, 'video_psychopy.py',
            '--duration', duration,
            '--file', file,
            '--output_file', output_file,
            '--betweenstimuli', betweenstimuli,
            '--zoom', zoom
        ])

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
if __name__ == '__main__':
    app.run(debug=True)
