import os
from bs4 import BeautifulSoup
import json
import sqlite3

import TempArticles

def generateDatabase():
	basePath = os.path.dirname(os.path.realpath(__file__))
	pathToCore = basePath.rsplit("/", 1)[0]
	pathToHTML = pathToCore + "/OldHtml"

	sectionFolders = os.popen("cd " + pathToHTML + ";ls -1").read().split("\n")[:-1]

	os.system("")

	tA = TempArticles.TempArticles("tempArticlesDB.db")

	import csv
	import sys

	f = open("dates.csv", 'rt')
	try:
		dates = []
		reader = csv.reader(f)
		for line in reader:
			dates.append(line)
	except:
		print("Could not open CSV File")

	for i in range(0,len(dates)):
		dateTemp = dates[i][2].split("/")
		dates[i][2] = str("19" + dateTemp[2] + "-" + dateTemp[1] + "-" + dateTemp[0])



	for section in range(0, len(sectionFolders)):
			filesInFoldersTemp = [os.path.join(dp, f) for dp, dn, filenames in
														os.walk(pathToHTML + "/" + sectionFolders[section]) for f in filenames if
														os.path.splitext(f)[1] == '.html']

			filesInFolders = []

			for i in range(0, len(filesInFoldersTemp)):
					if ".html" in filesInFoldersTemp[i] and "milestone" not in filesInFoldersTemp[i]:
							filesInFolders.append(str(filesInFoldersTemp[i]))

			for file in filesInFolders:
					
					
					
					
					
					articleSection = sectionFolders[section]
					with open(file, "r") as in_file:
							text = in_file.read()
					rawArticleData = BeautifulSoup(text)

					mainBody = rawArticleData.find("div", attrs = {"id": "contentContainer", "class": "clearfix"})

					if mainBody == None:
							# input(file)
							break

					# Actual content of the HTML.
					# Just until the begin of the external links
					mainContent = str(mainBody.find("div", attrs = {"id": "content"})).rsplit('<div class="externalLinks">',1)[0]


					# Manually added to content an empty div for the external links
					mainContent += '\n<div class="externalLinks">' \
												 '\n<!-- External links go here -->' \
												 '\n</div>' \
												 '\n</div>'

					# Actual article title
					articleTitle = rawArticleData.find("title").get_text()

					externalLinksTemp = mainBody.find("div", attrs = {"class": "externalLinks"})
					if externalLinksTemp == None:
							externalLinks = "None"
							print("No external links")
					else:
							externalLinks = externalLinksTemp.find("ol")
							if externalLinks == None:
									externalLinks = "None"

					linkToArticle = str(sectionFolders[section] + "/" + file.rsplit("/", 1)[1])
					articleDate = "PLACEHOLDER"
					for i in range(0,len(dates)):
						if dates[i][0] == linkToArticle:
							articleDate = dates[i][2]
					tA.addArticle(sectionFolders[section], articleTitle, mainContent, externalLinks, articleDate, linkToArticle)

	sectionTables = tA.getListOfTables()
	# Create the final DB
	finalDB = TempArticles.TempArticles("finalDB.db")
	for table in range(0,len(sectionTables)):
		dbData = tA.getEntriesAscending(sectionTables[table])
		jsonData = []
		for i in range(0,len(dbData)):
			currentEntry = dbData[i]
			jsonData.append({
				"title":currentEntry[1],
				"body":currentEntry[2],
				"category":currentEntry[3],
				"link":currentEntry[4],
				"previousTitle":currentEntry[5],
				"previousLink":currentEntry[6],
				"nextTitle":currentEntry[7],
				"nextLink":currentEntry[8],
				"externalLinks":currentEntry[9],
				"date":currentEntry[10]
				})


		for a in range(0,len(jsonData)):
			jsonData[a]["previousTitle"] = jsonData[a-1]["title"]
			jsonData[a]["previousLink"] = jsonData[a-1]["link"]
			if (a >= len(jsonData)-1):
				jsonData[a]["nextTitle"] = jsonData[0]["title"]
				jsonData[a]["nextLink"] = jsonData[0]["link"]
			else:
				jsonData[a]["nextTitle"] = jsonData[a+1]["title"]
				jsonData[a]["nextLink"] = jsonData[a+1]["link"]
		for a in range(0,len(jsonData)):
			finalDB.addArticleWithConnections(jsonData[a]["category"], jsonData[a]["title"], jsonData[a]["body"],jsonData[a]["externalLinks"], jsonData[a]["date"], jsonData[a]["link"], jsonData[a]["previousTitle"], jsonData[a]["previousLink"], jsonData[a]["nextTitle"], jsonData[a]["nextLink"])
		
	tA.disconnect()	
	finalDB.disconnect()
				
				