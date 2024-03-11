import re
import sqlite3


def import_csv_to_db(df):
    conn = sqlite3.connect('data_clean_fix.db')
    # df = pd.read_csv(file_path, encoding='iso-8859-1')
    df.to_sql('table_data', conn, if_exists='replace', index=False)
    return df


def filter_text(text):
    # Hilangkan karakter non-alfanumerik kecuali spasi
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Hilangkan text xX & A-F & 0-9
    text = re.sub(r'[xX][0-9a-fA-F]{2}', '', text)
    # Ubah teks menjadi huruf kecil
    text = text.lower()
    text = re.sub(r'(?<=\D)(?=\d)|(?<=\d)(?=\D)', ' ', text)
    # Memeriksa apakah terdapat angka di awal atau di akhir kalimat
    text = re.sub(r'^(\d+)|(\d+)$', r'\1\2 ', text)
    text = re.sub(r'(\d+)(\D+)', r'\1 \2', text)
    # Pisahkan kata-kata dengan spasi tunggal
    text = re.sub(r'\s+', ' ', text)
    # Menghapus spasi berlebih dengan satu spasi
    text = re.sub(r'\s+', ' ', text).strip()

    return text


# cleaning data dan mengembalikan DataFrame yang telah dibersihkan
def clean_data(df):
    # temp_df = import_csv_to_db(df)
    # temp_df['text_clean'] = temp_df['Tweet'].apply(filter_text)
    df = df.drop_duplicates()
    df['text_clean'] = df['Tweet'].apply(filter_text)

    return df


# export DataFrame ke file Excel
def export_to_excel(cleaned_df):
    output_file = 'cleaned_data.xlsx'
    cleaned_df.to_excel(output_file, index=False)

    return output_file
