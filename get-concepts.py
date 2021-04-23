import requests
import json
import io
import os
import urllib

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def requests_retry_session(
    retries=3,
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

def getWikidataLabels(uri):
  
  entity = extractEntity(uri)
  jsonUri = 'https://www.wikidata.org/wiki/Special:EntityData/'+entity+'.json'
  response = requests_retry_session().get(jsonUri)
  wdJson = response.json()
  print (wdJson)
  labels = wdJson.get('entities').get(entity).get('labels')

  return labels


def getConcepts(text):
  print (text)
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
    #print (candidates)

  #print ("=====================")
  #print (candidates)
  #print ("=====================")

  if (not candidates is None):
    for candidate in candidates:
      concept = {}
      if (not candidate is None): 
        print (candidate)
        label=candidate.get('resource').get('@label')
        if (label not in seen):
          seen.append(label)
          concept['label'] = label
          dbpediaURI = 'http://dbpedia.org/resource/' + candidate.get('resource').get('@uri')
          concept['dbpediaURI'] = dbpediaURI

          #Dereference dbpedia URI and get the wikidata uri on the under the owl#sameas predicate
          dbpediaJsonURI = 'http://dbpedia.org/data/' + candidate.get('resource').get('@uri') + '.json'
          response2 = requests.get(dbpediaJsonURI)
          dbpediaObj = response2.json()
          if (not dbpediaObj.get(dbpediaURI) is None):
            dbpediaPredicates = dbpediaObj.get(dbpediaURI).get('http://www.w3.org/2002/07/owl#sameAs')

            wikidata = []
            if not dbpediaPredicates is None:
              foundWikiData=0
              for value in dbpediaPredicates:
                wikidataPredicate = {}
                strValue = value.get('value')
                if strValue.count('wikidata.org') > 0 :
                  wikidataPredicate['uri'] = strValue
                  #get the labels from wikidata
                  #wikidataPredicate['labels'] = getWikidataLabels(strValue)
                  concept['wikidataURI']=strValue
                  wikidata.append(wikidataPredicate)
                  foundWikiData=1
              if (not foundWikiData):
                wikidataPredicate['uri']="NotFound"
                concept['wikidataURI']="NotFound"
                wikidata.append(wikidataPredicate)
            conceptsArray.append(concept)

  
  return(conceptsArray)

#----------------------------------------------------
path = 'publications.json'
target = 'enriched-publications.json'

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
      concepts = getConcepts(queryString)
      #print (concepts)
      record['concepts'] = concepts
      result.append(record)

  jsonld = {}
  #jsonld["@context"] = "http://schema.org"
  jsonld["graph"] = result

  with open(target, "w") as data_file:
    json.dump(jsonld, data_file, ensure_ascii=False)


