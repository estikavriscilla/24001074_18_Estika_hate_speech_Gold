import re
from flask import Flask, jsonify, send_file
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
import sqlite3
import pandas as pd
from function_clean import import_csv_to_db, filter_text, clean_data, export_to_excel

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder

swagger_template = dict(
    info={
        'title': LazyString(lambda: 'API Documentation From Data Processing and Modeling'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling'),
    },
    host=LazyString(lambda: request.host)
)

swagger_config = {
    'headers': [],
    'specs': [
        {
            'endpoint': 'testing',
            'route': '/docs.json',
        }
    ],
    'static_url_path': '/flasgger_statics',
    'swagger_ui': True,
    'specs_route':'/docs/'
}

swagger = Swagger(app, template=swagger_template,
                  config=swagger_config)


@app.route('/', methods=['GET'])
def hello_world():
    json_response = {
        'kode_status': 200,
        'description': 'Server API',
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
        'data': filter_text(text),

    }
    return jsonify(json_respons)


@swag_from('docs/hello_world.yml', methods=['POST'])
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.getlist('file')[0]
    # Import file csv ke Pandas
    df = pd.read_csv(file, encoding='latin-1')
    cleaned_df = clean_data(df)

    # Import Pandas ke db
    df_fix = import_csv_to_db(cleaned_df)

    # cleansed_db(cleaned_df)
    print(df_fix['text_clean'])
    output = {'message': 'File uploaded successfully',
              'output_file': cleaned_df['text_clean'].tolist()}

    return jsonify(output)


if __name__ == '__main__':
    app.run()