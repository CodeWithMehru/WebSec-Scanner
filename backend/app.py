from flask import Flask, render_template, request, jsonify
from models import db, Vulnerability
from scanner import scan_website
import os


app = Flask(__name__, template_folder='templates', static_folder='static')


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


with app.app_context():
    db.create_all()



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        
        result = scan_website(url)
        
        
        vulnerability = Vulnerability(url=url, result=result)
        db.session.add(vulnerability)
        db.session.commit()
        
        return jsonify({'status': 'success', 'result': result})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/scans', methods=['GET'])
def get_scans():
    scans = Vulnerability.query.all()
    data = [{'id': s.id, 'url': s.url, 'result': s.result} for s in scans]
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
