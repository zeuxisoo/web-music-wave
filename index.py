#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, hashlib, waveform
from bottle import debug, default_app, run, route, static_file, template, request, redirect, response

# Const variable
TITLE = "Music to Wave Image"
WWW_ROOT = os.path.abspath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(WWW_ROOT, 'static')
ATTACHMENT_ROOT = os.path.join(WWW_ROOT, 'attachment')

# Index
@route('/')
def index():
	return template("index", title=TITLE)
	
# Generate
@route('/generate', method="POST")
def generate():
	music = request.files.get('music')

	# had upload file
	if hasattr(music, "file"):
		basename, extension = os.path.splitext(music.filename)
		
		# valid the extension 
		if extension.lower() in ['.wav', '.aiff', '.au', '.ogg', '.flac', '.mp3']:
			raw = music.file.read()
			filename = md5(raw)
		
			# write upload file into attachment root
			f = open("%s/%s%s" % (ATTACHMENT_ROOT, filename, extension), "w")
			f.write(raw)
			f.close()
			
			# Draw wave image
			waveform.draw(
				"%s/%s%s" % (ATTACHMENT_ROOT, filename, extension), 
				"%s/%s%s" % (ATTACHMENT_ROOT, filename, ".png"), 
				(700, 100), 
				bgColor=(0,0,0,0), 
				fgColor=(0,0,128,255)
			)

			# Save filename into cookie for preview
			response.set_cookie("filename", music.filename)

			redirect('/preview/%s' % filename)
		else:
			redirect('/error/invalid-upload-file')
	
	redirect('/error/no-upload-file')

# Error
@route('/error/:status')
def error(status):
	return template('error', title=TITLE, status=status)

# Preview
@route('/preview/:id')
def preview(id):
	if os.path.exists("%s/%s%s" % (ATTACHMENT_ROOT, id, ".png")):
		filename = request.get_cookie("filename")
		response.set_cookie("filename", "")
		
		if filename is None:
			filename = "Unknow"
		
		return template('preview', title=TITLE, preview_id=id, filename=filename)
	else:
		redirect('/error/no-preview-file')

# Static file
@route('/static/:path#.+#')
def static_folder(path):
	return static_file(path, root=STATIC_ROOT)

@route('/attachment/:filename#.*\.png#')
def send_image(filename):
	return static_file(filename, root=ATTACHMENT_ROOT, mimetype='image/png')

#
def md5(content):
	return hashlib.md5(content).hexdigest()

# Boot
if __name__ == "__main__":
	debug(True)
	app = default_app()
	run(host='localhost', port=8083, reloader=True, app=app)