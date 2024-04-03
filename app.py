from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash
import os

app = Flask(__name__)
app.config['VERSION'] = 'v1.0'
app.secret_key = 'super_secret_key :D'

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    folder = request.form['folder']
    if folder:
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    else:
        folder_path = app.config['UPLOAD_FOLDER']
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    
    if file:
        filename = file.filename
        file.save(os.path.join(folder_path, filename))
        flash(f'File {filename} uploaded successfully')
    return redirect(url_for('index'))

@app.route('/files')
def list_files():
    folders = []
    files = []
    for item in os.listdir(app.config['UPLOAD_FOLDER']):
        if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], item)):
            folders.append(item)
        else:
            files.append(item)
    return render_template('files.html', folders=folders, files=files)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<path:filename>')
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            # Recursively delete all files and subdirectories within the folder
            for root, dirs, files in os.walk(file_path, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
            # After all files and subdirectories are deleted, remove the directory itself
            os.rmdir(file_path)
        else:
            os.remove(file_path)
        flash(f'{filename} deleted successfully')
    return redirect(url_for('list_files'))

@app.route('/folder/<foldername>')
def folder_files(foldername):
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], foldername)
    files = os.listdir(folder_path)
    return render_template('folder.html', foldername=foldername, files=files)

if __name__ == '__main__':
    app.run(debug=True)
