MySublimeQL
===========

A Sublime Text 2 plugin to provide autocompletions in SQL scripts using table/column names from a connected database

Installing
==========

**With Git:** Clone this repository into the ST2 Package folder

**Without Git:** Download the latest source and move the directory into the ST2 Package folder

Using
=====

Create a new document and set its sytanx to SQL then start typing. A list of table names from the connected schema will start to appear in the autocompletions list.

###Switching Schemas

You can cycle through a listing of database connections as defined in your users settings by using the following command:

* Switch Schema: `ctrl+shift+q`

A list of avaliable connections will appear in the quick view menu from which you can select the desired connection. Once selected, the autocompletions will rebuild themselves based on the new database tabels/columns

Configuration
=============

MySqublimeQL requires a set of connection parameters that can be defined as follows:

	{
		"connections":
		[
			{
				"name": "Schema Name",
				"host": "localhost",
				"user": "username",
				"pass": "password",
				"db"  : "database"
			}
		],
		"default_schema": "Schema Name"
	}

The default schema is set to the name of the schema configuration object that MySublimeQL will default its completion lists