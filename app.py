import re
from flask import Flask, jsonify, send_file
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import sqlite3
import pandas as pd

app = Flask(__name__)
conn = sqlite3.connect('tweet_database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS table_tweet(
                    id INTEGER PRIMARY KEY,
                    column1 TEXT,
                    column2 INTEGER,
                    column3 INTEGER,
                    column4 INTEGER,
                    column5 INTEGER,
                    column6 INTEGER,
                    column7 INTEGER,
                    column8 INTEGER,
                    column9 INTEGER,
                    column10 INTEGER,
                    column11 INTEGER,
                    column12 INTEGER,
                    column13 INTEGER
                    )''')

conn.commit()

app.json_encoder = LazyJSONEncoder

swagger_template = dict(
    info={
        'title': LazyString(lambda: 'API Documentation From Data Processing and Modeling'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host=LazyString(lambda: request.host)
)
# swagger_template = {
#     "info": {
#         'title': 'API Documentation From Data Processing and Modeling',
#         'version': '1.0.0',
#         'description': 'Dokumentasi API untuk Data Processing dan Modeling',
#     },
#     "host": '127.0.0.1:5000'
# }

swagger_config = {
    'headers': [],
    'specs': [
        {
            'endpoint': 'testing',
            'route': '/testing.json',
        }
    ],
    'static_url_path': '/flasgger_statics',
    'swagger_ui': True,
    'specs_route':'/docs/'
}

swagger = Swagger(app, template=swagger_template,
                  config=swagger_config)


#@swag_from('docs/hello_world.yml', methods=['GET'])
@app.route('/', methods=['GET'])
def hello_world():
    json_response = {
        'kode_status': 200,
        'deskripsi': 'Server API',
        'data': 'Challenge Gold'
    }
    return jsonify(json_response)


@swag_from('docs/text_processing.yml', methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():

    text = request.form.get('text')

    json_respons = {

        'kode_status': 200,
        'deskripsi': 'teks yang sudah di proses',
        'data': re.sub(r'[^a-zA-Z0-9]',' ', text),
        'data': text.lower()
    }
    return jsonify(json_respons)


@swag_from('docs/upload_file.yml', methods=['POST'])
@app.route('/upload_file', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file_upload']
    if uploaded_file:
        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'No file uploaded'}), 400

    return jsonify(json_respons)


def clean_text(text):
    # Tambahkan metode pembersihan teks sesuai kebutuhan Anda
    cleaned_text = text.strip().lower()  # Contoh sederhana: menghapus spasi di awal dan akhir, dan mengonversi ke huruf kecil
    return cleaned_text


@swag_from('docs/upload_and_clean.yml', methods=['POST'])
@app.route('/upload_and_clean', methods=['POST'])
def upload_and_clean():
    if 'file' not in request.files:
        return jsonify({'error': 'File tidak ditemukan dalam request'}), 400

    received_file = request.files['file']
    filename = received_file.filename
    file_data = received_file.read()

    # Menyimpan file ke dalam database
    cursor.execute("INSERT INTO files (filename, file_data) VALUES (?, ?)", (filename, file_data))
    conn.commit()

    # Membersihkan data dari file
    cleaned_data = clean_text(file_data.decode('utf-8'))  # Menggunakan utf-8 untuk mendecode data file

    # Menyimpan data yang telah dibersihkan ke dalam database
    cursor.execute("INSERT INTO cleaned_texts (cleaned_text) VALUES (?)", (cleaned_data,))
    conn.commit()

    # Membuat DataFrame dari data bersih untuk Excel
    df = pd.DataFrame({'Cleaned Text': [cleaned_data]})

    # Menyimpan DataFrame ke dalam file Excel
    excel_filename = 'cleaned_data.xlsx'
    df.to_excel(excel_filename, index=False)

    # Mengembalikan file Excel sebagai respons
    return send_file(excel_filename, as_attachment=True)

if __name__== '__main__':
    app.run()
