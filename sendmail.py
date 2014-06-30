#!/usr/bin/env python

import smtplib
import re
import copy

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

def sendmail(sender, recipients, subject, summary, html):
	# me == my email address
	# you == recipient's email address
	#me = "jang574@localhost"
	#you = "jang574@gmail.com"

	# Create message container - the correct MIME type is multipart/alternative.
	#msg = MIMEMultipart('alternative')
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = sender
	msg['To'] = ", ".join(recipients)

	# Create the body of the message (a plain-text and an HTML version).
	if False:
		text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
		html = """\
		<html>
		  <head></head>
		  <body>
		    <p>Hi!<br>
		       How are you?<br>
		       Here is the <a href="http://www.python.org">link</a> you wanted.
		    </p>
		  </body>
		</html>
		"""

	# Record the MIME types of both parts - text/plain and text/html.
	#part1 = MIMEText(text, 'plain')
	#part2 = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
	part1 = MIMEText(summary.encode('utf-8'), 'html', 'utf-8')
	part2 = MIMEBase('text', 'html')
	part2.set_payload(html.encode('utf-8'))
	encoders.encode_base64(part2)

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	#msg.attach(part2)

	# attachment
	part2.add_header('Content-Disposition', 'attachment; filename={}.html'.format(re.sub(r'[ /:]+','_', subject)))
	msg.attach(part2)
	
	# Send the message via local SMTP server.
	if False :
		s = smtplib.SMTP('localhost')
	else:
		s = smtplib.SMTP(host='smtp.gmail.com', port=587)

		# gmail needs starttls
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login("user@gmail.com", "password")

	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.
	s.sendmail(sender, recipients, msg.as_string())
	s.quit()

