import os
import jinja2 #Used to substitute the tags in the html
import sqlite3
import json

def allArticlesFromTable(category):
	dbConnect = sqlite3.connect("finalDB.db")
	cur = dbConnect.cursor()
	queryToExecute = "SELECT * FROM " + str(category) + " WHERE NOT date = \"PLACEHOLDER\"  ORDER BY date ASC;"
	cur.execute(queryToExecute)
	allArticles = cur.fetchall()
	jsonData = []
	for i in range(0,len(allArticles)):
		queryResult = allArticles[i]

		jsonData.append({
			"title":queryResult[1],
			"body":queryResult[2],
			"category":queryResult[3],
			"link":queryResult[4],
			"previousTitle":queryResult[5],
			"previousLink":"/"+queryResult[6],
			"nextTitle":queryResult[7],
			"nextLink":queryResult[8],
			"externalLinks":queryResult[9],
			"date":queryResult[10],
			"articleImage":queryResult[11],
			"articleDescription":queryResult[12]
		})
	return jsonData

def queryDatabase(stringToSearch):
	finalString = stringToSearch.split(" ")

	for i in range(0,len(finalString)):
		finalString[i] = "%" +  finalString[i] + "%"


	dbConnect = sqlite3.connect("finalDB.db")
	cur = dbConnect.cursor()
	tempTables = cur.execute("select name from sqlite_master where type = 'table';")
	tables = tempTables.fetchall()

	listOfTables = []
	for i in range(0,len(tables)):
		listOfTables.append(tables[i][0])

	jsonData = []

	for i in range(0,len(listOfTables)):
		queryToExecute = "SELECT * FROM " + str(listOfTables[i]) + " WHERE title LIKE ?"
		for i in range(1,len(finalString)):
			queryToExecute +=  " AND title LIKE ?"
		queryToExecute += ";"
		cur.execute(queryToExecute,finalString)
		queryResultTemp = cur.fetchall()
		if len(queryResultTemp) != 0:
			for j in range(0,len(queryResultTemp)):
				queryResult = queryResultTemp[j]
				jsonData.append({
					"title":queryResult[1],
					"link":queryResult[4],
				})

	return jsonData
		

def getArticleForURL(section,articleURL):
	articleCategory = section
	articlePage = articleURL
		
	dbConnect = sqlite3.connect("finalDB.db")
	cur = dbConnect.cursor()
	queryToExecute = "SELECT * FROM " + str(articleCategory) + " WHERE linkToArticle = ?;"
	articleLink = str(articleCategory + "/" + articlePage)
	cur.execute(queryToExecute,(articleLink,))
	queryResultTemp = cur.fetchall()
	if len(queryResultTemp) == 0:
		print("DEAD LINK")
		return "ERROR"
	queryResult = queryResultTemp[0]
	jsonData = {
		"title":queryResult[1],
		"body":queryResult[2],
		"category":queryResult[3],
		"link":queryResult[4],
		"previousTitle":queryResult[5],
		"previousLink":"/"+queryResult[6],
		"nextTitle":queryResult[7],
		"nextLink":queryResult[8],
		"externalLinks":queryResult[9],
		"date":queryResult[10],
		"articleImage":queryResult[11],
		"articleDescription":queryResult[12]
	}

	return jsonData

def getSectionIndexPage(section):
	articleCategory = section
	
	dbConnect = sqlite3.connect("finalDB.db")
	cur = dbConnect.cursor()
	queryToExecute = "SELECT * FROM " + str(articleCategory) + " WHERE linkToArticle = ?;"
	articleLink = str(articleCategory + "/index.html")
	cur.execute(queryToExecute,(articleLink,))
	queryResultTemp = cur.fetchall()
	if len(queryResultTemp) == 0:
		print("DEAD LINK")
		return "ERROR"
	queryResult = queryResultTemp[0]
	
	jsonData = {
		"title":queryResult[1],
		"body":queryResult[2],
		"category":queryResult[3],
		"link":queryResult[4],
		"previousTitle":queryResult[5],
		"previousLink":"/"+queryResult[6],
		"nextTitle":queryResult[7],
		"nextLink":queryResult[8],
		"externalLinks":queryResult[9],
		"date":queryResult[10],
		"articleImage":queryResult[11],
		"articleDescription":queryResult[12]
	}

	return jsonData


def jinjaSubstitution(dictWithValues,jinjaFilename):
	"""
	Returns the html requested with the supplied parameters. dictWithValues should be a simple 
	dict with "jinjaVariabeName" : "valueToSubstitute", whereas the jinjaFilename should be the
	name of the file, complete with the extension. 
	"""
	templateLoader = jinja2.FileSystemLoader( searchpath="/" )
	#Get the current path of this file. From here, put togehter the path of the template file
	basePath = os.path.dirname(os.path.abspath(__file__))
	# An environment provides the data necessary to read and
	#   parse our templates.  We pass in the loader object here.
	templateEnv = jinja2.Environment( loader=templateLoader )

	if ".jinja" not in jinjaFilename: 
		jinjaFilename += ".jinja"

	# This constant string specifies the template file we will use.
	#TEMPLATE_FILE = basePath + "/JinjaTemplates/table.jinja"
	TEMPLATE_FILE = basePath + "/Templates/" + jinjaFilename
	# Read the template file using the environment object.
	# This also constructs our Template object.
	template = templateEnv.get_template( TEMPLATE_FILE )

	# Specify any input variables to the template as a dictionary.
	templateVars = dictWithValues

	# Finally, process the template to produce our final text.
	outputText = template.render( templateVars )

	return outputText

def dateToUnixTimestamp(date):
	"""
	Converts the date to a unix timestamp, for easy sorting. The format should be YYYY-MM-DD
	"""
	return os.popen("date -j -f \"%Y-%m-%d\" \"" + str(date) + "\" \"+%s\"").read()