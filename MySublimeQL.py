#!/usr/bin/python

import sublime, sublime_plugin, sys, os

# Crazy shit needed to get MySQLdb working
directory = os.path.dirname(os.path.realpath(__file__)) + "\\"
sys.path.append(directory+"\\MySQLdb")
sys.path.append(directory+"\\MySQLdb\\constants")

from MySQLdb import *
from MySQLdb.constants import *

def get_connections():
	settings = sublime.load_settings('MySublimeQL.sublime-settings')
	return settings.get('connections')

def connect_to_database(connections, database=None):
	connection_params = {}
	if database is None:
		# Use default schema from settings
		database = sublime.load_settings('MySublimeQL.sublime-settings').get('default_schema')

	for connection in connections:
		if connection.get('name') == database:
			connection_params = connection

	host     = connection_params.get('host')
	user     = connection_params.get('user')
	passwd   = connection_params.get('pass')
	database = connection_params.get('db')

	db = connect(host, user, passwd, database)
	return db.cursor()

cursor = connect_to_database(get_connections())
cursor.execute("SHOW TABLES")
data = cursor.fetchall()
completions = [(x[0],) * 2 for x in data]

class SwitchSchemaCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		connection_list = []
		for connection in get_connections():
			connection_list.append([connection.get('name'), 'Host: ' + connection.get('host')])
		window = sublime.active_window()
		window.show_quick_panel(connection_list, None)

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