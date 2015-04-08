#!/usr/bin/env python

from distutils.core import setup
import platform
import fileinput
import sys
import os
import shutil
import subprocess
import gzip
import glob

if not sys.version_info[0] == 2 and sys.version_info[1] < 4:
    print "AsciiDoc requires Python 2.4 or newer"
    sys.exit(1) # return non-zero value for failure

data_files=[
		('asciidoc/filters/code', ['filters/code/code-filter.py', 'filters/code/code-filter.conf']),
		('asciidoc/filters/graphviz', ['filters/graphviz/graphviz2png.py', 'filters/graphviz/graphviz-filter.conf']),
		('asciidoc/filters/music', ['filters/music/music2png.py', 'filters/music/music-filter.conf']),
		('asciidoc/filters/latex', ['filters/latex/latex2img.py', 'filters/latex/latex-filter.conf']),
		('asciidoc/filters/source', ['filters/source/source-highlight-filter.conf']),
		('asciidoc/themes', ['themes/flask/flask.css']),
		('asciidoc/volnitsky', ['themes/volnitsky/volnitsky.css']),
		('asciidoc/volnitsky', ['themes/volnitsky/volnitsky.css']),
]

scripts=["asciidoc.py", "a2x.py"]

if platform.system() == "Windows":
	data_files.append(
		("", ["asciidoc.bat"])
	)
else:
	scriptdir = os.path.join("build","scripts")
	if not os.path.exists(scriptdir):
		os.makedirs(scriptdir)
	newScripts = []
	for s in scripts:
		newpath = os.path.join(scriptdir, os.path.splitext(s)[0])
		outFh = open(newpath, "w")
		inFh = open(s, "r")
		for line in inFh:
			if line.startswith("CONF_DIR = '"):
				line = "CONF_DIR = '/usr/local/asciidoc'%s" % os.linesep
			outFh.write(line)
		newScripts.append(newpath)
	scripts = newScripts

	mantxt = glob.glob("doc/*.1")
	if not os.path.exists(os.path.join("build","man")):
		os.makedirs(os.path.join("build","man"))
	newman = []
	for mt in mantxt:
		newname = "%s.gz" % os.path.basename(mt)
		newpath = os.path.join("build","man","%s" % newname)

		f_in = open(mt, 'rb')
		f_out = gzip.open(newpath, 'wb')
		f_out.writelines(f_in)
		f_out.close()
		f_in.close()

		newman.append(newpath)
	
	data_files.append(
		(os.path.join('man', 'man1'), newman)
	)

conf = glob.glob("*.conf")
conf.extend(
	glob.glob("README*") + glob.glob("BUGS*") + glob.glob("INSTALL*") + glob.glob("CHANGELOG*")
)

data_files.append(
	("asciidoc", conf)
)
	
docbook = glob.glob(os.path.join("docbook-xsl","*.xsl"))
data_files.append(
	("asciidoc/docbook-xsl", docbook)
)

dblatex = glob.glob(os.path.join("dblatex","*.sty"))
data_files.append(
	("asciidoc/dblatex", dblatex)
)

css = glob.glob(os.path.join("stylesheets","*.css"))
data_files.append(
	("asciidoc/stylesheets", css)
)

js = glob.glob(os.path.join("javascripts","*.js"))
data_files.append(
	("asciidoc/javascripts", js)
)

callouts = glob.glob(os.path.join("images", "icons", "callouts","*"))
data_files.append(
	("asciidoc/images/icons/callouts", callouts)
)

icons = glob.glob(os.path.join("images", "icons", "*.png"))
icons.append("images/icons/README")
data_files.append(
	("asciidoc/images/icons", icons)
)
	
setup(name='AsciiDoc',
	version='8.6.9',
	description='Human-readable document format using plain-text mark-up conventions',
	author='AsciiDoc',
	author_email='',
	url='http://asciidoc.org/',
	license="GNU General Public License version 2 (GPLv2).",
	py_modules=["asciidocapi"],
	scripts=scripts,
	data_files=data_files
)
