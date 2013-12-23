#!/usr/bin/python

import sublime, sublime_plugin, sys, os

# Crazy shit needed to get MySQLdb working
directory = os.path.dirname(os.path.realpath(__file__)) + "\\"
sys.path.append(directory+"\\MySQLdb")
sys.path.append(directory+"\\MySQLdb\\constants")

from MySQLdb import *
from MySQLdb.constants import *

class DBManager:
	def __init__(self):
		self.settings = sublime.load_settings('MySublimeQL.sublime-settings')
		self.get_connections()
		self.connect_to_database()

	def get_connections(self):
		self.connections = self.settings.get('connections')
		return self.connections

	def connect_to_database(self, database=None):
		params = {}
		if database is None:
			database = self.settings.get('default_schema')

		for connection in self.connections:
			if connection.get('name') == database:
				params = connection

		self.db = connect(params.get('host'), params.get('user'), params.get('pass'), params.get('db'))

	def query(self, query):
		cursor = self.db.cursor()
		cursor.execute(query)
		return cursor.fetchall()

db = DBManager()

def autocomplete(show_tables=True, table_name=None):
	query = ''
	if show_tables or table_name == '':
		query = 'SHOW TABLES'
	else:
		query = 'DESCRIBE ' + table_name
	data = db.query(query)
	completions = [(x[0],) * 2 for x in data]
	return completions

completions = autocomplete()

class SwitchSchemaCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.connection_list = []
		for connection in db.get_connections():
			self.connection_list.append([connection.get('name'), 'Host: ' + connection.get('host')])
		window = sublime.active_window()
		window.show_quick_panel(self.connection_list, self.on_done)

	def on_done(self, picked):
		global completions
		if picked >= 0:
			db.connect_to_database(self.connection_list[picked][0])
			completions = autocomplete()

class MySublimeQL(sublime_plugin.EventListener):
	def on_modified(self, view):
		global completions
		view_sel = view.sel()
		sel = view_sel[0]
		pos = sel.end()
		text = view.substr(sublime.Region(pos - 1, pos))
		if text == '.' :
			table_name = view.substr(view.word(pos -1))
			completions = autocomplete(False, table_name)
		elif text == ' ':
			completions = autocomplete()

	def on_query_completions(self, view, prefix, locations):
		if view.match_selector(locations[0], "source.sql"):
			return (completions)