#!/usr/bin/env python

import os
import subprocess
import distutils.spawn
import datetime
import re
import markdown
import convert2html
import sendmail
from local_settings import *

today = datetime.date.fromordinal(datetime.date.today().toordinal())
yesterday = datetime.date.fromordinal(datetime.date.today().toordinal()-2)
#print "today : {0}, yesterday : {1}".format(today, yesterday)
html = ""
branch_commitid = []
outputpath = "{}/log".format(os.getcwd())
filename = "{}/{}_gitfetch.txt".format(outputpath, today)
gitpath = distutils.spawn.find_executable("git")

if os.path.exists(filename) :
	f = open(filename, 'r')
	outlog = f.read()
	f.close()
else :
	args = [gitpath, "fetch", myremote]
	#print args
	os.chdir(mypath)
	logproc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(outlog, errlog) = logproc.communicate()

	########### save fetch log ###########
	outlog = errlog # fetch log outputs stderr
	f = open(filename, 'w')
	f.write(outlog)
	f.close()

if len(outlog) :
	for item in outlog.split('\n') :
		#print item
		oneline = re.split("->", item)
		if len(oneline) == 2:
			if oneline[0][3] != "[":
				#print oneline[0][3:]
				(branch, commitid) = (re.split("[ ]+",oneline[0][3:])[1], \
					re.split("[\.]+",re.split("[ ]+",oneline[0][3:])[0]))
				#print (branch, commitid)
				for br_item in mybranch:
					if br_item == branch:
						print "matched : " + branch
						branch_commitid.append((branch, commitid))
	print branch_commitid

#if 1:
#	item = branch_commitid[0]
for item in branch_commitid :
	print item
	args = [gitpath, "log", "--oneline", "--no-merges", \
		"{}/{}".format(myremote, item[0]), "{}..{}".format(item[1][0], item[1][1])]
	print args
	#cmdline = "git log --oneline --no-merges {}/{} {}..{}".format(myremote, item[0], item[1][0], item[1][1])
	#print cmdline
	os.chdir(mypath)
	#logproc = subprocess.Popen([cmdline], stdout=subprocess.PIPE, shell=True)
	logproc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(outlog, errlog) = logproc.communicate()
	#html = convert2html.convert2html(outlog)
	summary, html = convert2html.convert2html("{} : {}".format(today,item[0]), outlog)
	print "------------------"
	#print html.encode('utf-8')

	########### save html ###########
	filename = "{}/{}_{}.html".format(outputpath, today, re.sub('/','_',item[0]))
	f = open(filename, 'w')
	f.write(html.encode('utf-8'))
	f.close()

	########### send email ###########
	sendmail.sendmail(sender, recipients, "{} : {}".format(today, item[0]), summary, html)

