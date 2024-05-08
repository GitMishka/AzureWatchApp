from flask import Flask, jsonify
import multiprocessing
import os
import exchangeScrapper  # Assuming your scraping code is in 'exchangeScrapper.py'

app = Flask(__name__)
process = None

@app.route('/start_scraper', methods=['POST'])
def start_scraper():
    global process
    if process is None or not process.is_alive():
        process = multiprocessing.Process(target=exchangeScrapper.run_scrapper)
        process.start()
        return jsonify({'status': 'scraper started'}), 200
    else:
        return jsonify({'status': 'scraper already running'}), 200

@app.route('/stop_scraper', methods=['POST'])
def stop_scraper():
    global process
    if process is not None and process.is_alive():
        process.terminate()  # or use a more graceful shutdown method
        process.join()
        return jsonify({'status': 'scraper stopped'}), 200
    else:
        return jsonify({'status': 'scraper not running'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
