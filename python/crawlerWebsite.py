
import urllib.request
import re
import time
from bs4 import BeautifulSoup


sqlFile = open("file.txt","w")

"""*****************
*** Define the patterns and groups
*****************"""
namePattern = re.compile("([A-Za-z][\w\s.\d]*),([\w\s\d]*)[\,\.\s]*(DO|MD)")
addressPattern = re.compile("(<br\s?/>\s[\s\d\w,\.\(\)]+)+\(")
removeBrTagPattern = re.compile("(\s\s)*<br[\s]*/?>(\s\s)*")
removeDoubleSpacePattern = re.compile("(\s\s)+")
phonePattern = re.compile('(\([0-9\(\)\-\s]+)[\d]')
docIdPattern = re.compile('\'([\d]+)\'' )
specialtyPattern = re.compile("d>([\d\w\s\<\/>&\.\-,']+)</td")
removeITagPattern = re.compile('<i>[\w\s\d]*</i>')
totalDocsPattern = re.compile("([\d,]*)\)")
"""*********************"""

#Test
urlBase = "http://127.0.0.1:8501/fake_hcsc_response.html?%s=&%s"

letters = ('A')

#Some measures
startTime = time.time()
granTotal = 0

sqlBase =   "insert into table"

sqlStatement = ""
for letter in letters:
    html = urllib.request.urlopen(urlBase % (letter,'1'))
    parsedHtml = BeautifulSoup(html.read())
    totalTag = parsedHtml.select(".results_header")[0]
    total = int(totalDocsPattern.search(str(totalTag)).group(1).replace(",",""))

    #########
    ## Calculate the total of pages
    ########
    numberPages = int(total/50)
    if total%15 > 0:
        numberPages+=1

    for i in range(1,numberPages+1):
        print("Processing letter %s - page %s" % (letter, str(i) ) )
        htmlPerPage = urllib.request.urlopen(urlBase % (letter, str(i)))
        parsedHtmlPerPage = BeautifulSoup(htmlPerPage.read())
        trResultRowTags = parsedHtmlPerPage.find_all(name="tr",attrs=("class","result_row"))

        for trTag in trResultRowTags:
            trTagParsed = trTag

            ################
            ## 
            ## 
            ################
            docId = trTagParsed.a.get("href")
            docId = docIdPattern.search(docId).group(1)

            docName = trTagParsed.a.string
            docName = namePattern.search(docName)

            """" Check if the doc is MD or DO """
            if not docName:
                continue

            ################
            ## Get and format the name information
            ################
            lastName = docName.group(1).strip()
            firstNameUnformatted = docName.group(2).strip().split(" ")
            firstName = firstNameUnformatted[0]
            middleName = ""

            fullName = docName.group(2) + " " + docName.group(1)

            if len(firstNameUnformatted) > 1:
                middleName = firstNameUnformatted[1]
           
            ################
            ## Get and format the address
            ################
            address = addressPattern.search(str(trTagParsed.td)).group().strip()
            address = removeBrTagPattern.sub(", ",address)
            address = address[1:len(address)-4]
            address = removeDoubleSpacePattern.sub(" ",address)

            ################
            ## Get phone information
            ################
            phone = phonePattern.search(str(trTagParsed)).group()

            ################
            ## Get and format the specialty information
            ################
            specialtyTag = str(trTagParsed.find_all("td")[1]).strip()
            specialty = specialtyPattern.search(specialtyTag).group(1)
            specialty = removeITagPattern.sub("",specialty)
            specialty = removeBrTagPattern.sub("",specialty).strip()

            sqlStatement += (sqlBase % (firstName,middleName,lastName,fullName,address,phone,specialty, docId) )        

        sqlFile.write(sqlStatement);
        sqlStatement = ""        
    
    granTotal += total
print(time.time() - startTime )