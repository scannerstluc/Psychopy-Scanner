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
    return render_template('about.html')


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
        port = data.get('port')
        baudrate = data.get('baudrate')
        trigger = data.get('trigger')
        file = data.get('filePath')
        output_file = data.get('output_file')
        subprocess.run([
            sys.executable, 'psychopy_runner.py',
            '--duration', duration,
            '--words', words,
            '--file', file,
            '--port', port,
            '--baudrate', baudrate,
            '--trigger', trigger,
            '--output_file', output_file,
            '--zoom', zoom
        ])

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-emo-voice', methods=['POST'])
def submit_emo_voice():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        betweenstimuli = data.get('betweenstimuli')
        file = data.get('filePath')
        output_file = data.get('output_file')
        print("working here?")
        subprocess.run([
            sys.executable, 'Psychopy_EMO_VOICES.py',
            '--duration', duration,
            '--file', file,
            '--betweenstimuli', betweenstimuli,
            '--output_file', output_file,
        ])

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-datass', methods=['POST'])
def submit_datass():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        betweenstimuli = data.get('betweenstimuli')
        file = data.get('filePath')
        output_file = data.get('output_file')
        print("working here?")
        subprocess.run([
            sys.executable, 'Psychopy_EMO_FACE.py',
            '--duration', duration,
            '--file', file,
            '--betweenstimuli', betweenstimuli,
            '--output_file', output_file,
        ])

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/submit-adjectifs', methods=['POST'])
def submit_adjectifs():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        betweenstimuli = data.get('betweenstimuli')
        file = data.get('filePath')
        output_file = data.get('output_file')
        blocks = data.get('blocks')
        zoom = data.get('zoom')
        print("working here?")
        subprocess.run([
            sys.executable, 'Psychopy_Adjectifs.py',
            '--duration', duration,
            '--file', file,
            '--blocks', blocks,
            '--zoom', zoom,
            '--betweenstimuli', betweenstimuli,
            '--output_file', output_file,
        ])

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/submit-stroop', methods=['POST'])
def submit_stroop():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        betweenstimuli = data.get('betweenstimuli')
        file = data.get('filePath')
        output_file = data.get('output_file')
        zoom = data.get('zoom')
        print(data)
        subprocess.run([
            sys.executable, 'Psychopy_colors.py',
            '--duration', duration,
            '--file', file,
            '--zoom', zoom,
            '--betweenstimuli', betweenstimuli,
            '--output_file', output_file,
        ])
        print("working here?")

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/submit-localizer', methods=['POST'])
def submit_localizer():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        betweenstimuli = data.get('betweenstimuli')
        blocks = data.get('blocks')
        per_block = data.get('per_blocks')
        port = data.get('port')
        baudrate = data.get('baudrate')
        trigger = data.get('trigger')
        output_file = data.get('output_file')

        print(data)
        subprocess.run([
            sys.executable, 'Psychopy_LOCALIZER.py',
            '--duration', duration,
            '--blocks', blocks,
            '--per_block', per_block,
            '--port', port,
            '--baudrate', baudrate,
            '--trigger', trigger,
            '--betweenstimuli', betweenstimuli,
            '--output_file', output_file,
        ])
        print("working here?")

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
        port = data.get('port')
        baudrate = data.get('baudrate')
        trigger = data.get('trigger')
        betweenstimuli = data.get('betweenstimuli')
        output_file = data.get('output_file')
        subprocess.run([
            sys.executable, 'image_opti.py',
            '--duration', duration,
            '--file', file,
            '--port', port,
            '--baudrate', baudrate,
            '--trigger', trigger,
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
        port = data.get('port')
        baudrate = data.get('baudrate')
        trigger = data.get('trigger')
        betweenstimuli = data.get('betweenstimuli')
        output_file = data.get('output_file')
        subprocess.run([
            sys.executable, 'video_psychopy.py',
            '--duration', duration,
            '--file', file,
            '--port', port,
            '--baudrate', baudrate,
            '--trigger', trigger,
            '--output_file', output_file,
            '--betweenstimuli', betweenstimuli,
            '--zoom', zoom
        ])

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
if __name__ == '__main__':
    app.run(debug=True)
