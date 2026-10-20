import os
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

@app.route('/db-check')
def db_check():
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'postgres-db'),
            port=int(os.environ.get('DB_PORT', 5432)),
            database=os.environ.get('DB_NAME', 'jobportal'),
            user=os.environ.get('DB_USER', 'jpuser'),
            password=os.environ.get('DB_PASSWORD', 'jppassword')
        )
        conn.close()
        return jsonify({'db': 'connected', 'host': os.environ.get('DB_HOST', 'postgres-db')})
    except Exception as e:
        return jsonify({'db': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
