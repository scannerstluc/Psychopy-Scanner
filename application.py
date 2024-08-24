from flask import Flask, render_template, request, jsonify
import subprocess
import sys
import webbrowser
from waitress import serve


app = Flask(__name__)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    print("")
    return render_template('about.html')


@app.route('/')
def home():
    return render_template('about.html')





@app.route('/submit-text', methods=['POST'])
def submit_text():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        words = data.get('words')
        zoom = data.get('zoom')
        trigger = data.get('trigger')
        file = data.get('filePath')
        output_file = data.get('output_file')
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_Text.py',
            '--duration', duration,
            '--words', words,
            '--file', file,
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
            sys.executable, 'Python_scripts/Psychopy_EMO_VOICES.py',
            '--duration', duration,
            '--file', file,
            '--betweenstimuli', betweenstimuli,
            '--output_file', output_file,
        ])

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-cyberball', methods=['POST'])
def submit_cyberball():
    try:
        data = request.get_json()
        premiere_phase = data.get("premiere_phase")
        exclusion = data.get("exclusion")
        transition = data.get("transition")
        minimum = data.get("minimum")
        maximum = data.get("maximum")
        trigger = data.get("trigger")
        patient_name = data.get("patient_name")
        output_file = data.get("output_file")
        filePath = data.get("filePath")
        print("ça passe")
        print(data)
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_Cyberball.py',
            '--premiere_phase', premiere_phase,
            '--exclusion', exclusion,
            '--transition', transition,
            '--minimum', minimum,
            '--patient_name', patient_name,
            '--maximum', maximum,
            '--trigger', trigger,
            '--output_file', output_file,
            '--filePath', filePath,

        ])

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/submit-emo-faces', methods=['POST'])
def submit_emo_faces():
    try:
        print("working here?")
        data = request.get_json()
        duration = data.get('duration')
        betweenstimuli = data.get('betweenstimuli')
        file = data.get('filePath')
        output_file = data.get('output_file')
        print("working here?")
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_EMO_FACE.py',
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
        entrainement = data.get('entrainement')
        per_block = data.get('per_block')
        print("working here?")
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_Adjectifs.py',
            '--duration', duration,
            '--file', file,
            '--blocks', blocks,
            '--zoom', zoom,
            '--entrainement', entrainement,
            '--per_block', per_block,
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
        choice = data.get('choice')
        print(data)
        subprocess.Popen([
            sys.executable, 'Python_scripts/Psychopy_colors.py',
            '--duration', duration,
            '--file', file,
            '--zoom', zoom,
            '--choice', choice,
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
        trigger = data.get('trigger')
        output_file = data.get('output_file')

        print(data)
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_LOCALIZER.py',
            '--duration', duration,
            '--blocks', blocks,
            '--per_block', per_block,
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
        trigger = data.get('trigger')
        betweenstimuli = data.get('betweenstimuli')
        output_file = data.get('output_file')
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_Image.py',
            '--duration', duration,
            '--file', file,
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
        trigger = data.get('trigger')
        betweenstimuli = data.get('betweenstimuli')
        output_file = data.get('output_file')
        subprocess.run([
            sys.executable, 'Python_scripts/Psychopy_Video.py',
            '--duration', duration,
            '--file', file,
            '--trigger', trigger,
            '--output_file', output_file,
            '--betweenstimuli', betweenstimuli,
            '--zoom', zoom
        ])

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

    
if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')

    serve(app, host='0.0.0.0', port=5000)
