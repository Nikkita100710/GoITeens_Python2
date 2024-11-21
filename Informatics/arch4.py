import os
# import random
# import string
from PIL import Image
# import numpy as np
from fpdf import FPDF
from docx import Document
import csv
# import sqlite3
# import wave
# import pydub
# from io import BytesIO
# from pydub import AudioSegment
from pydub.generators import Sine
from moviepy.editor import ColorClip


def pad_file_to_size(file_path, size_bytes):
    current_size = os.path.getsize(file_path)
    if current_size < size_bytes:
        with open(file_path, 'ab') as f:
            f.write(b'\0' * (size_bytes - current_size))
    elif current_size > size_bytes:
        with open(file_path, 'rb+') as f:
            f.truncate(size_bytes)


def generate_txt_file(name, size_mb):
    size_bytes = size_mb * 1024 * 1024
    with open(name + '.txt', 'w') as f:
        f.write('A' * size_bytes)


def generate_csv_file(name, size_mb):
    size_bytes = size_mb * 1024 * 1024
    num_rows = size_bytes // (1024 * 10)  # Approx 10 KB per row
    with open(name + '.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for _ in range(num_rows):
            writer.writerow(['A'] * 10)  # 10 columns
    pad_file_to_size(name + '.csv', size_bytes)


def generate_jpg_file(name, size_mb):
    size_bytes = size_mb * 1024 * 1024
    width, height = 1024, 1024
    img = Image.new('RGB', (width, height), color='red')
    img.save(name + '.jpg', 'JPEG', quality=85)  # Adjust quality if needed
    pad_file_to_size(name + '.jpg', size_bytes)


def generate_png_file(name, size_mb):
    size_bytes = size_mb * 1024 * 1024
    width, height = 1024, 1024
    img = Image.new('RGBA', (width, height), color='blue')
    img.save(name + '.png')
    pad_file_to_size(name + '.png', size_bytes)


def generate_mp3_file(name, size_mb):
    size_bytes = size_mb * 1024 * 1024
    duration_ms = (size_bytes / (128 * 1024)) * 1000  # Approx 128 kbps
    tone = Sine(440)  # 440 Hz sine wave
    audio = tone.to_audio_segment(duration=duration_ms)
    audio.export(name + '.mp3', format='mp3')
    pad_file_to_size(name + '.mp3', size_bytes)


def generate_mp4_file(name, size_mb):
    size_bytes = size_mb * 1024 * 1024
    duration = size_bytes / (100 * 1024 * 1024)  # Approx 100 MB/min
    clip = ColorClip(size=(640, 480), color=(255, 0, 0), duration=duration)
    clip.write_videofile(name + '.mp4', fps=24)
    pad_file_to_size(name + '.mp4', size_bytes)


def generate_sql_file(name, size_mb):
    size_bytes = size_mb * 1024 * 1024
    num_lines = size_bytes // 50  # Approx 50 bytes per line
    with open(name + '.sql', 'w') as f:
        f.write('CREATE TABLE test (id INTEGER PRIMARY KEY, data TEXT);\n')
        for i in range(num_lines):
            f.write(f'INSERT INTO test (data) VALUES ("A");\n')
    pad_file_to_size(name + '.sql', size_bytes)


def generate_docx_file(name, size_mb):
    size_bytes = size_mb * 1024 * 1024
    num_paragraphs = size_bytes // 1024  # Approx 1 KB per paragraph
    doc = Document()
    for _ in range(num_paragraphs):
        doc.add_paragraph('A' * 1000)
    doc.save(name + '.docx')
    pad_file_to_size(name + '.docx', size_bytes)


def generate_pdf_file(name, size_mb):
    size_bytes = size_mb * 1024 * 1024
    num_pages = size_bytes // (1024 * 50)  # Approx 50 KB per page
    pdf = FPDF()
    for _ in range(num_pages):
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="A" * 1000)
    pdf.output(name + '.pdf')
    pad_file_to_size(name + '.pdf', size_bytes)


def main():
    name = input('Enter the file name (without extension): ')
    size_mb = int(input('Enter the file size in MB (1-20): '))

    if size_mb < 1 or size_mb > 20:
        print('Size must be between 1 and 20 MB.')
        return

    print('Generating files...')
    generate_txt_file(name, size_mb)
    generate_csv_file(name, size_mb)
    generate_jpg_file(name, size_mb)
    generate_png_file(name, size_mb)
    generate_mp3_file(name, size_mb)
    generate_mp4_file(name, size_mb)
    generate_sql_file(name, size_mb)
    generate_docx_file(name, size_mb)
    generate_pdf_file(name, size_mb)
    print('Files generated successfully.')


if __name__ == '__main__':
    main()
