from app import app
import os
import urllib.request
from flask import Flask, flash, request, redirect, render_template, send_from_directory, current_app, send_file, jsonify
from werkzeug.utils import secure_filename

import csv


ALLOWED_EXTENSIONS = ['csv']
app.secret_key = "secret key"



def some_function(context):
	'''
	
	THERE ARE SOME MAIN FUNC 
	now there are stub: fun reverse first record at each rows

	'''
	for line in context:
		print(line)
		line[0] = line[0][::-1]
		print(line)
	return context


def file_info(file_object):
	file = open(os.path.join('./upload', file_object))
	context = list(csv.reader(file))
	return len(context)


@app.route('/process', methods=['POST'])		
def process():
	filelist = []
	file_info_list = []
	for filename in os.listdir('./upload'):
		file_info_list.append(file_info(filename))
		filelist.append(filename)
	return render_template('process.html', filelist=filelist, file_info_list=file_info_list)


@app.route('/process/<path:file>')
def process_file(file):
	file_csv_read = open(os.path.join(app.config['UPLOAD_FOLDER'], file))
	context = list(csv.reader(file_csv_read))
	
	some_function(context)
				
	new_filename = 'new' + file
	file_csv_write = os.path.join(app.config['DOWNLOAD_FOLDER'], new_filename)
	with open(file_csv_write, 'w') as f_object:
		writer = csv.writer(f_object)
		for row in context:
			writer.writerow(row)
	return redirect('/')


@app.route('/delete/<path:file>')
def delete_file_from_upload_folder(file):
	file_to_del = os.path.join(app.config['UPLOAD_FOLDER'], file)
	os.remove(file_to_del)
	return redirect('/')


@app.route('/')
def upload_form():
	return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:		#check for valid filename/extension
			filename = secure_filename(file.filename)
			file.save(os.path.join('./upload', filename))
			flash('File was successfully uploaded. Thank you.')
			return redirect('/')
		else:
			flash('Allowed file type is: csv')
			return redirect(request.url)


@app.route("/list_for_download", methods=["POST"])
def list_files_for_download():
	filelist = []
	for filename in os.listdir(app.config['DOWNLOAD_FOLDER']):
		filelist.append(filename)
	return render_template('download.html', filelist=filelist)


@app.route('/download_file/<path:filename>')
def download_this_file(filename):
	return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


@app.route('/delete_download/<path:filename>')
def delete_file_from_download_folder(filename):
	file_to_del = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
	os.remove(file_to_del)
	return redirect('/')