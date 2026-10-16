from flask import Flask, jsonify
from homepage import get_homepage
from jobs import list_jobs, search_jobs

app = Flask(__name__)

@app.route('/')
def homepage():
    return jsonify(get_homepage())

@app.route('/jobs')
def jobs():
    return jsonify(list_jobs())

@app.route('/jobs/search/<keyword>')
def search(keyword):
    return jsonify(search_jobs(keyword))

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'service': 'jobportal'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
