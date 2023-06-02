from datetime import datetime
import os
from flask import Flask, flash, request, redirect, jsonify,json
from werkzeug.utils import secure_filename
import pickle 
import pandas as pd
from preproc import encodage
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlite3

app=Flask(__name__)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)

ALLOWED_EXTENSIONS = set(['csv'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(path, 'results.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    result = db.Column(db.String(50))
    dataset =db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    archive = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, filename, result,dataset):
        self.filename = filename
        self.result = result
        self.dataset = dataset

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#preprocessing
with open('preprocessing_transformer.pkl', 'rb') as file:
    preprocessing_transformer = pickle.load(file)

#Models
with open('DT_estimator.pkl', 'rb') as file:
    estimator_model_dt = pickle.load(file)

with open('RF_estimator.pkl', 'rb') as file:
         estimator_model_rf = pickle.load(file)

with open('KNN_estimator.pkl', 'rb') as file:
        estimator_model_knn = pickle.load(file)

with open('SVM_estimator.pkl', 'rb') as file:
        estimator_model_svm = pickle.load(file)

with open('LR_estimator.pkl', 'rb') as file:
        estimator_model_lr = pickle.load(file)

with open('xgb_estimator.pkl', 'rb') as file:
        estimator_model_xgb = pickle.load(file)

@app.route('/ScanWithDT', methods=['POST','GET'])
def dtt():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Get the directory path of the uploaded file
            #file_directory = os.path.dirname(file_path)

            # Read the .txt file into a DataFrame
            df = pd.read_csv(file_path)

            if 'duration' in df.columns:
                encoded_instance = preprocessing_transformer['encoder'](df)
                selected_features =  preprocessing_transformer['selected_features']
                scaler = preprocessing_transformer['scaler']
                normalized_instance = pd.DataFrame(scaler.transform(encoded_instance), columns=encoded_instance.columns)
                normalized_instance =normalized_instance[selected_features] 
                result = estimator_model_dt.predict(normalized_instance)
                if result == [0]:
                        result= 'normal'
                else:
                        result = 'attack'
            else : 
                print('t')
                if result == [0]:
                        result= 'normal'
                else:
                        result = 'attack'
            dataset='nsl-kdd'
            new_result = Result(filename, result,dataset)
            db.session.add(new_result)
            db.session.commit()

        response = {
        'result': result,
        'filename': filename
        }
        return json.dumps(response)


@app.route('/ScanWithRF', methods=['GET', 'POST'])
def rff():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Get the directory path of the uploaded file
            #file_directory = os.path.dirname(file_path)

            # Read the .txt file into a DataFrame
            df = pd.read_csv(file_path)

            if 'duration' in df.columns:
                encoded_instance = preprocessing_transformer['encoder'](df)
                selected_features =  preprocessing_transformer['selected_features']
                scaler = preprocessing_transformer['scaler']
                normalized_instance = pd.DataFrame(scaler.transform(encoded_instance), columns=encoded_instance.columns)
                normalized_instance =normalized_instance[selected_features] 
                result = estimator_model_rf.predict(normalized_instance)
                if result == [0]:
                        result= 'normal'
                else:
                        result = 'attack'
            else : 
                print('t')
                if result == [0]:
                        result= 'normal'
                else:
                        result = 'attack'
            dataset='nsl-kdd'
            new_result = Result(filename, result,dataset)
            db.session.add(new_result)
            db.session.commit()

        response = {
        'result': result,
        'filename': filename
        }
        return json.dumps(response)


@app.route('/ScanWithKNN', methods=['GET', 'POST'])
def knnn():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Get the directory path of the uploaded file
            #file_directory = os.path.dirname(file_path)

            # Read the .txt file into a DataFrame
            df = pd.read_csv(file_path)

            if 'duration' in df.columns:
                encoded_instance = preprocessing_transformer['encoder'](df)
                selected_features =  preprocessing_transformer['selected_features']
                scaler = preprocessing_transformer['scaler']
                normalized_instance = pd.DataFrame(scaler.transform(encoded_instance), columns=encoded_instance.columns)
                normalized_instance =normalized_instance[selected_features] 
                result = estimator_model_knn.predict(normalized_instance)
                if result == [0]:
                        result= 'normal'
                else:
                        result = 'attack'
            else : 
                print('t')
                if result == [0]:
                        result= 'normal'
                else:
                        result = 'attack'
            dataset='nsl-kdd'
            new_result = Result(filename, result,dataset)
            db.session.add(new_result)
            db.session.commit()

        response = {
        'result': result,
        'filename': filename
        }
        return json.dumps(response)


@app.route('/ScanWithSVM', methods=['GET', 'POST'])
def svmm():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Get the directory path of the uploaded file
            #file_directory = os.path.dirname(file_path)

            # Read the .txt file into a DataFrame
            df = pd.read_csv(file_path)

            if 'duration' in df.columns:
                encoded_instance = preprocessing_transformer['encoder'](df)
                selected_features =  preprocessing_transformer['selected_features']
                scaler = preprocessing_transformer['scaler']
                normalized_instance = pd.DataFrame(scaler.transform(encoded_instance), columns=encoded_instance.columns)
                normalized_instance =normalized_instance[selected_features] 
                result = estimator_model_svm.predict(normalized_instance)
                if result == [0]:
                        result= 'normal'
                else:
                        result = 'attack'
            else : 
                print('t')
                if result == [0]:
                        result= 'normal'
                else:
                        result = 'attack'
            dataset='nsl-kdd'
            new_result = Result(filename, result,dataset)
            db.session.add(new_result)
            db.session.commit()

        response = {
        'result': result,
        'filename': filename
        }
        return json.dumps(response)
    

@app.route('/ScanWithXGB', methods=['GET', 'POST'])
def xgbb():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Get the directory path of the uploaded file
            #file_directory = os.path.dirname(file_path)

            # Read the .txt file into a DataFrame
            df = pd.read_csv(file_path)

            if 'duration' in df.columns:
                encoded_instance = preprocessing_transformer['encoder'](df)
                selected_features =  preprocessing_transformer['selected_features']
                scaler = preprocessing_transformer['scaler']
                normalized_instance = pd.DataFrame(scaler.transform(encoded_instance), columns=encoded_instance.columns)
                normalized_instance =normalized_instance[selected_features] 
                result = estimator_model_xgb.predict(normalized_instance)
                if result == [0]:
                        result= 'normal'
                else:
                        result = 'attack'
            else : 
                print('t')
                if result == [0]:
                        result= 'normal'
                else:
                        result = 'attack'
            dataset='nsl-kdd'
            new_result = Result(filename, result,dataset)
            db.session.add(new_result)
            db.session.commit()

        response = {
        'result': result,
        'filename': filename
        }
        return json.dumps(response)
    

    
@app.route('/ScanWithLR', methods=['GET', 'POST'])
def lrr():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Get the directory path of the uploaded file
            #file_directory = os.path.dirname(file_path)

            # Read the .txt file into a DataFrame
            df = pd.read_csv(file_path)

            if 'duration' in df.columns:
                encoded_instance = preprocessing_transformer['encoder'](df)
                selected_features =  preprocessing_transformer['selected_features']
                scaler = preprocessing_transformer['scaler']
                normalized_instance = pd.DataFrame(scaler.transform(encoded_instance), columns=encoded_instance.columns)
                normalized_instance =normalized_instance[selected_features] 
                result = estimator_model_lr.predict(normalized_instance)
                if result == [0]:
                        result= 'normal'
                else:
                        result = 'attack'
            else : 
                print('t')
                if result == [0]:
                        result= 'normal'
                else:
                        result = 'attack'
            dataset='nsl-kdd'
            new_result = Result(filename, result,dataset)
            db.session.add(new_result)
            db.session.commit()

        response = {
        'result': result,
        'filename': filename
        }
        return json.dumps(response)
@app.route('/results', methods=['GET'])
def get_results():
    results = Result.query.all()
    result_list = []
    for result in results:
        result_data = {
            'id': result.id,
            'filename': result.filename,
            'result': result.result,
            'dataset': result.dataset,
            'date': result.date.strftime('%Y-%m-%d %H:%M:%S') , # Format the date as a string
            'archive': result.archive
        }
        result_list.append(result_data)
    return jsonify(result_list)

@app.route('/Dashboard', methods=['GET'])
def get_data():
    conn = sqlite3.connect('results.db')
    cursor = conn.cursor()
    # Execute a query to retrieve data from the table
    cursor.execute("SELECT id,strftime('%Y-%m-%d', date), filename, dataset, result FROM Result WHERE archive=False")

    data = cursor.fetchall()
    
    # Close the database connection
    cursor.close()
    conn.close()
    
    # Convert the data to a JSON response
    result = [
        {
            'id': row[0],
            'date': row[1],
            'filename': row[2],
            'datasetname': row[3],
            'result': row[4]
        }
        for row in data
    ]
    return jsonify(result)
@app.route('/Archive', methods=['GET'])
def get_archeive():
    conn = sqlite3.connect('results.db')
    cursor = conn.cursor()
    # Execute a query to retrieve data from the table
    cursor.execute("SELECT id,strftime('%Y-%m-%d', date), filename, dataset, result FROM Result where archive= True")
    data = cursor.fetchall()
    # Close the database connection
    cursor.close()
    conn.close()
    # Convert the data to a JSON response
    result = [
        {
            'id': row[0],
            'date': row[1],
            'filename': row[2],
            'datasetname': row[3],
            'result': row[4]
        }
        for row in data
    ]
    return jsonify(result)
    
@app.route('/Dashboard/<int:id>', methods=['PATCH'])
def archive_result(id):
    result = Result.query.get(id)
    if result:
        result.archive = True
        db.session.commit()
        return jsonify({'message': 'Result archived successfully'})
    else:
        return jsonify({'message': 'Result not found'}), 404

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=False)