import requests
import json
import io
import os
import urllib
import wikidata

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from wikidata.client import Client
from wikidata.multilingual import Locale

NotFoundArray = []
MultipleWikiDataLinksFoundArray = []
NotFoundWikiDataLink = []


def requests_retry_session(
    retries=10,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def extractEntity(uri):
  parts = uri.split('entity/')
  
  return(parts[1])

def getWikidataLabel(uri, language):

  client = Client()  
  entity = client.get(extractEntity(uri), load=True)
  try:
      label=entity.label[Locale(language)]
  except KeyError:
      label = ''
  return label


def getConcepts(text, language):
  #print (text)
  url = "https://api.dbpedia-spotlight.org/en/candidates?text="+urllib.parse.quote_plus(text)+"&confidence=0.95"
  headers = {
    'accept': 'application/json'
  }
  response = requests_retry_session().get(url,headers=headers)
  objJson = response.json()
  candidates = objJson.get('annotation').get('surfaceForm')
  conceptsArray = []
  seen = []


  if(type(candidates) is dict):
    #print ("this is a dict, convert to list")
    candidates=[candidates]

  if (not candidates is None):
    for candidate in candidates:
      concept = {}
      if (not candidate is None): 
        print (candidate)
        label=candidate.get('resource').get('@label')
        if (label not in seen):
          seen.append(label)
          if (language == 'en'):
            concept['label'] = label
            concept['language'] = 'en'
            TranslatedLabelFound=1
          else:
            translatedlabel=''
            TranslatedLabelFound=0
          dbpediaURI = 'http://dbpedia.org/resource/' + candidate.get('resource').get('@uri')
          concept['dbpediaURI'] = dbpediaURI

          #Dereference dbpedia URI and get the wikidata uri on the under the owl#sameas predicate
          dbpediaJsonURI = 'http://dbpedia.org/data/' + candidate.get('resource').get('@uri') + '.json'
          response2 = requests_retry_session().get(dbpediaJsonURI,headers=headers)
          foundWikiData=0
          dbpediaObj = response2.json()
          if (not dbpediaObj.get(dbpediaURI) is None):
            dbpediaPredicates = dbpediaObj.get(dbpediaURI).get('http://www.w3.org/2002/07/owl#sameAs')

            wikidata = []
            wikiDataURIs=""

            if not dbpediaPredicates is None:
              separator = ""
              for value in dbpediaPredicates:
                wikidataPredicate = {}
                strValue = value.get('value')
                if strValue.count('wikidata.org') > 0 :
                  if (foundWikiData == 1):
                    #There is more than one wikidata link, this is likely an error the LOD, but best we can do
                    #is to be transparent about this, and retrieve BOTH in this field
                    print ("Found multiple wikidata links in the record")
                    separator = "|"
                    MultipleWikiDataLinksFoundArray.append(label)
                  wikiDataURIs=wikiDataURIs+separator+strValue
                  wikidataPredicate['uri'] = wikiDataURIs
                  #get the labels from wikidata
                  #wikidataPredicate['labels'] = getWikidataLabels(strValue)
                  concept['wikidataURI'] = wikiDataURIs
                  print ("Found:"+strValue)
                  wikidata.append(wikidataPredicate)
                  foundWikiData=1
            

          if (not foundWikiData):
            #no sameas predicate found in dbpedia record, try the global service
            #https://global.dbpedia.org/same-thing/lookup/?uri=
            print ("Not found in sameAs predicate of dbpedia, attempting in global.dbpedia.org")
            globalJsonURI = 'https://global.dbpedia.org/same-thing/lookup/?uri=' + dbpediaURI
            print ("Searching in "+globalJsonURI)
            response2 = requests_retry_session().get(globalJsonURI,headers=headers)
            globalObj = response2.json()
            if (not globalObj.get('locals') is None):
              separator = ""
              globalPredicates = globalObj.get('locals')
              for strValue in globalPredicates:
                wikidataPredicate = {}
                if strValue.count('wikidata.org') > 0 :
                  if (foundWikiData == 1):
                    #There is more than one wikidata link, this is likely an error the LOD, but best we can do
                    #is to be transparent about this, and retrieve BOTH in this field
                    print ("Found multiple wikidata links in the record")
                    separator = "|"
                    MultipleWikiDataLinksFoundArray.append(label)
                  wikiDataURIs=wikiDataURIs+separator+strValue
                  print ("Found:"+strValue)
                  wikidataPredicate['uri'] = wikiDataURIs
                  concept['wikidataURI']=wikiDataURIs
                  wikidata.append(wikidataPredicate)
                  foundWikiData=1


            #last resort, didn't find wikidata link anywhere, set it to NotFound
            if (foundWikiData == 0):
              print ("Failed to find WikiData URI, last resort set it to NotFound")
              wikidataPredicate['uri']="NotFound"
              concept['wikidataURI']="NotFound"
              NotFoundWikiDataLink.append(label)
            
          wikidata.append(wikidataPredicate)

          #if language is not english, modify label for target language, if it exists
          #skip this if wikidata URI was not found either, as that is needed for labels
          if (language != "en"):
            if (foundWikiData == 1):
              if (separator == ""):
                translatedlabel=getWikidataLabel(concept['wikidataURI'], language)
              else:
                #there are multiple wikdata links, combine them into one label
                #wikidatalinksparts = concept['wikidataURI'].split(separator)
                #translatedlabelLink=wikidatalinksparts[0]
                #translatedlabel=getWikidataLabel(translatedlabelLink, language)
                i=0
                for translatedlabelLink in concept['wikidataURI'].split(separator):
                  if (i==0):
                    translatedlabel=getWikidataLabel(translatedlabelLink, language)
                  else:
                    translatedlabel=translatedlabel+separator+getWikidataLabel(translatedlabelLink, language)
                  i=i+1
              print (translatedlabel)
            if (not translatedlabel == ''):
              concept['label'] = translatedlabel
              concept['language'] = language
              TranslatedLabelFound=1
          if (TranslatedLabelFound == 1):
            conceptsArray.append(concept)
          else:
            #did not find corresponding label, skip this concept
            print ("did not find label in target language, skipping concept")
            NotFoundArray.append(label)
        else:
          #skipping, already seen this label for this item
          print ("skipping this concept, already seen for this item")

  
  return(conceptsArray)

#----------------------------------------------------
path = 'publications.json'
target = 'enriched-publications-fr.json'
language = 'fr'

with open(path,'r',encoding='utf-8') as jsonfile:

  jsonText = jsonfile.read()
  #iterate on the biblio records
  jsonRecords = json.loads(str(jsonText),strict=False)

  #print(list(jsonRecords.items()))
  result = []
  for record in jsonRecords.values():
    print ("\n=====================\n")
    #print (record)
    #print (record.get('Abstract'))
    #print (record.get('Title')
    queryString="";
    if record.get('Title') != "":
      queryString=queryString+record.get('Title')
    if record.get('Abstract') != "":
      queryString=queryString+record.get('Abstract')
    if record.get('AuthorKeywords') !="":
      queryString=queryString+record.get('AuthorKeywords')
    if queryString != "":
      concepts = getConcepts(queryString, language)
      #print (concepts)
      record['concepts'] = concepts
      result.append(record)

  print ("Following Labels were Not Found in Target Language")
  unique_labels = list(set(NotFoundArray))
  print(unique_labels)

  print ("Following Labels Found Multiple WikiData Links from DBPedia Entity to WikiData")
  unique_labels = list(set(MultipleWikiDataLinksFoundArray))
  print(unique_labels)

  print ("Following Entities had no DBPedia Entity link to WikiData")
  if (language != "en"):
    print ("These concepts were skipped since language is not EN, WikiData link needed for translation of label into target language")
  else:
    print ("These concepts were still included, WikiData URI is set to NotFound for these, and English labels come from DBPedia")
  unique_labels = list(set(NotFoundWikiDataLink))
  print(unique_labels)

  jsonld = {}
  #jsonld["@context"] = "http://schema.org"
  jsonld["graph"] = result

  with open(target, "w") as data_file:
    json.dump(jsonld, data_file, ensure_ascii=False)


