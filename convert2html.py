#!/usr/bin/env python
import re
import subprocess

header = """<html>
<head>
<style type="text/css">
/* Toggle
================================================== */
.symple-toggle .symple-toggle-trigger { display: block; color: #555; display: block; padding: 10px 10px 10px 37px; border: 1px solid #ddd; background: #f9f9f9 url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAI0lEQVQY02P4//8/AzJOS0v7D8Lo4gwDqBAmQQgTr3AI+BoAoHAONHHyzJUAAAAASUVORK5CYII=) no-repeat 15px center; outline: 0; text-transform: none; letter-spacing: normal; font-weight: normal; font-size: 1em; line-height: 1.0em; margin: 0; margin-top: 10px; cursor: pointer; }
.symple-toggle .symple-toggle-trigger:hover { background-color: #eee; text-decoration: none; }
.symple-toggle .symple-toggle-trigger.active, .symple-toggle .symple-toggle-trigger.active:hover { color: #000; background-color: #eee; background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAHElEQVQY02P8//8/AzGAcQAVpqWl/aeuwiHgawC6cBxVWdHqegAAAABJRU5ErkJggg==); text-decoration: none; }
.symple-toggle .symple-toggle-container { display: none; overflow: hidden; padding: 10px; border: 1px solid #ddd; border-top: 0px; }
</style>
<script type='text/javascript' src='http://wpexplorer-demos.com/symple-shortcodes/wp-includes/js/jquery/jquery.js'></script>
<script type='text/javascript' src='http://wpexplorer-demos.com/symple-shortcodes/wp-includes/js/jquery/jquery-migrate.min.js'></script>
<script type='text/javascript' src='http://wpexplorer-demos.com/symple-shortcodes/wp-content/plugins/symple-shortcodes/includes/js/symple_toggle.js'></script>
</head>
<body>
"""

footer = """</body>
</html>"""

def get_header():
	return header

def get_footer():
	return footer

def get_maintext(title, text):
#	converted_text = ""
	converted_text = "<h2>{}</h2>".format(title)
	summary = "<html><head></head><body><h2>{}</h2>".format(title)
	for item in text.split('\n') :
		#print "length ({0}) : {1}".format(len(item), item)
		if len(item) == 0 :
			break
		oneline = re.split(" ", item, maxsplit=1)
		print oneline
		cmdline = "git log -1 --stat {0}".format(oneline[0])
		fulllogproc = subprocess.Popen([cmdline], stdout=subprocess.PIPE, shell=True)
		(outfulllog, errfulllog) = fulllogproc.communicate()
		#print outfulllog.splitlines()[0]
		cr = re.search(r'CRs-Fixed\:\s+([0-9]*)', outfulllog)
		if cr:
			oneline[1] += " <b>({})</b>".format(cr.group(0))
		commitid = re.search(r'commit\s+([a-zA-Z0-9]*)\n',
			outfulllog)
		outfulllog = re.sub(r'commit\s+([a-zA-Z0-9]*)\n',
			r'commit <a target="_blank" href="https://www.codeaurora.org/cgit/quic/la/kernel/msm-3.10/diff/?id=\1">\1</a>\n',
			outfulllog)
		outfulllog = unicode(outfulllog, encoding='utf-8')

		converted_text += '<div class="symple-toggle symple-all">'
		converted_text += '<h3 class="symple-toggle-trigger">'
		#converted_text += '{} {}</h3>'.format(oneline[0], oneline[1])
		converted_text += '{}</h3>'.format(oneline[1])
		converted_text += '<div class="symple-toggle-container">'
		#converted_text += md.convert(outfulllog)
		converted_text += '<pre>'
		converted_text += outfulllog
		converted_text += '</pre>'
		converted_text += '</div>'
		converted_text += '</div>'

		commitlink = '<a target="_blank" href="https://www.codeaurora.org/cgit/quic/la/kernel/msm-3.10/commit/?id={}">{}</a>\n'.format(commitid.group(1), oneline[0])
		summary += '<h3>{} : {}</h3>'.format(commitlink, oneline[1])
	summary += "</body></html>"
	#print summary
	return summary, converted_text

def convert2html(text):
	return get_header() + get_maintext(text) + get_footer()

def convert2html(title, text):
	summary, main = get_maintext(title, text)
	return summary, get_header() + main + get_footer()

