from flask import Flask, render_template, request, jsonify
import threading
from scraper import run_scraper

app = Flask(__name__)

stop_event = threading.Event()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_scraper():
    global scraper_thread
    if not stop_event.is_set():
        stop_event.clear()
        scraper_thread = threading.Thread(target=run_scraper, args=(stop_event,))
        scraper_thread.start()
        return jsonify({'message': 'Scraper started'}), 200
    return jsonify({'message': 'Scraper already running'}), 200

@app.route('/stop', methods=['POST'])
def stop_scraper():
    stop_event.set()
    return jsonify({'message': 'Scraper stopped'}), 200

if __name__ == '__main__':
    app.run(debug=True)
