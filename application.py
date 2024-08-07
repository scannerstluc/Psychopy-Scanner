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
        print("je capte plus")
        print("test")
        data = request.get_json()
        duration = data.get('duration')
        words = data.get('words')
        zoom = data.get('zoom')
        file = data.get('filePath')
        print("pour être")
        print(data)
        print(file)
        print("sur")
        subprocess.run([
            sys.executable, 'psychopy_runner.py',
            '--duration', duration,
            '--words', words,
            '--file', file,
            '--zoom', zoom
        ])

        return jsonify({'status': 'success', 'message': 'Données reçues et script exécuté'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
