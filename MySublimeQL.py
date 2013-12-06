#!/usr/bin/python

import sublime, sublime_plugin, sys, os

# Crazy shit needed to get MySQLdb working
directory = os.path.dirname(os.path.realpath(__file__)) + "\\"
sys.path.append(directory+"\\MySQLdb")
sys.path.append(directory+"\\MySQLdb\\constants")

from MySQLdb import *
from MySQLdb.constants import *

settings = sublime.load_settings('MySublimeQL.sublime-settings')
connection = settings.get('connections')[0]

host   = connection.get('host')
user   = connection.get('user')
passwd = connection.get('pass')
db     = connection.get('db')

db = connect(host, user, passwd, db)
cursor = db.cursor()
cursor.execute("SHOW TABLES")
data = cursor.fetchall()
completions = [(x[0],) * 2 for x in data]

class SwitchSchemaCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print 'hello'

class MySublimeQL(sublime_plugin.EventListener):
	def on_modified(self, view):
		view_sel = view.sel()
		sel = view_sel[0]
		pos = sel.end()
		text = view.substr(sublime.Region(pos - 1, pos))
		if text == '.' :
			print view.substr(view.word(pos -1))

	def on_query_completions(self, view, prefix, locations):
		if view.match_selector(locations[0], "source.sql"):
			return (completions)