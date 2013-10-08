#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import subprocess
import os
from cStringIO import StringIO
from flask import Flask, Response, send_from_directory, request
from werkzeug import secure_filename

app = Flask(__name__, static_url_path = "")
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class ZipEncoder(object):
    def __init__(self, incoming):
        self.incoming = incoming

    def zip(self, filename):
        command = ["/usr/bin/zip", "-9", "-", filename]
        if os.path.isdir(filename):
            command.insert(2, "-r")
        print command
        cmd = subprocess.Popen(command, stdout = subprocess.PIPE , stderr = subprocess.PIPE)
        out, err = cmd.communicate()
        return StringIO(out)


    def __call__(self, *argl):
        return self.zip(self.incoming)

@app.route("/upload", methods = ['POST'])
def upload():
    file = request.files['upfile']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "cacca"

@app.route('/uploaded_file')
def uploaded_file():
    return ""

@app.route("/static/<path:filename>")
def send_static(filename):
    return send_from_directory("static", filename)

@app.route("/<path>")
def getzip(path):
    zipper = ZipEncoder(path)
    return Response(zipper(), mimetype = "application/zip", direct_passthrough = True, headers = {"Content-disposition" : "attachment; filename=\"%s.zip\"" % path })

@app.route("/")
def root():
    txt = """
		<html>
		<head>
			<title>%(TITLE)s</title>
			<meta http-equiv="Content-Type" content="text/html; charset=utf8" />
			<script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>
			<script type="text/javascript" src="static/js/plupload.full.js"></script>
			<script type="text/javascript" src="static/js/jquery.plupload.queue.js"></script>
			<script type="text/javascript" src="static/js/upload.js"></script>
			<link rel="stylesheet" type="text/css" href="static/css/plupload.css">
			</script>
		</head>
		<body>
			<h4>Upload something dude...</h4>
			<div id="uploader">I'm sorry, are you from the past?</div>
		</body>
		</html>
            """
    return txt

if __name__ == "__main__":
    app.run("0.0.0.0", 8081)

