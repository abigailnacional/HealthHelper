from flask import Flask, redirect, render_template, request
from appmodels import create_app
import os
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
import requests
from requests.structures import CaseInsensitiveDict
import json
from typing import Optional


app = create_app()
db = SQLAlchemy(app)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)


#Class for entity mentions
class medEntity:
     def __init__(
               self,
               id: int,
               med_type: str,
               med_content: str,
               linked_ents: Optional[str] = "None", #not allowed to use list, so concatenate all as one string
               med_time: Optional[str] = "None",
               med_cert: Optional[str] = "None",
               med_subj: Optional[str] = "None"
     ):
          self.id = id
          self.med_type = med_type
          self.med_content = med_content
          self.linked_ents = linked_ents
          self.med_time = med_time
          self.med_cert = med_cert
          self.med_subj = med_subj

#Directs to home page
@app.route("/")
def home():
     return render_template("home.html")

#Directs to contact us page
@app.route("/contact_us")
def contact_us():
     return render_template("contact_us.html")

#Directs to text input page; takes text input from user and generates results
@app.route("/upload", methods = ['GET', 'POST'])
def upload():
     if request.method == 'POST':
          givenText = request.form['doctext']
          jsonData = requestHealthAPI(givenText)
          if jsonData == None:
               return "Something broke."
          else:
               entity_list = split_entmen(jsonData)
               #Then generate linked entity list
          return render_template("results.html", entity_list = entity_list)
     return render_template("upload.html")

#"Insulin regimen human 5 units IV administered."

#Sends API request and returns JSON data
def requestHealthAPI(docData):
     url = "https://healthcare.googleapis.com/v1/projects/healthhelper-344619/locations/us-central1/services/nlp:analyzeEntities"
     headers = CaseInsensitiveDict()
     headers["Authorization"] = "Bearer ya29.c.b0AXv0zTMuXXdQyeodhpQN851ucHS8OK8pQnMKiHl0ZkSMtOmz9SM0TPgWiWhTgE9kGNpGZBGzwsTF0W4Dz0-rNaYsyS_A20jQFf37agWR6gomL_q6YBdFxmSelrfyG_cJtOG_9t1GIp7xUud1buifZTzygkTeqnIXw-lf5dNFiWkxkG7FYe4oX4YRXf0dXVB89PKRNDctXueEDzm8ucZIXuPhbyl_DtA"
     headers["Content-Type"] = "application/json"
     data = '{"nlpService":"projects/healthhelper-344619/locations/us-central1/services/nlp","documentContent":"' + docData + '","licensedVocabularies":["SNOMEDCT_US","ICD10CM"]}'
     resp = requests.post(url, headers=headers, data=data)
     print(resp.status_code)
     if resp.status_code == 200:
          data = json.loads(resp.text)
          return data
     else:
          return None

#Create entity objects from json file, put them in a list. Return list
#When this list is inputted, we will iterate over all the objects and display each part
def split_entmen(data):
     entMens = data['entityMentions']
     entm_list = []
     for x in range(len(entMens)):
          entm_list.append(create_entmen(entMens[x]))
     return entm_list

#Creates an individual entity object
def create_entmen(entmen) -> medEntity:
     #Initialize attributes
     entmed_id = entmen['mentionId']
     entmed_type = entmen['type']
     entmed_content = entmen['text']['content']
     le_string = "None"
     ent_temporal = "None"
     ent_cert = "None"
     ent_subj = "None"

     if 'linkedEntities' in entmen:
          linkedEntities = entmen['linkedEntities']
          le_string = ""
          #Iterate through linked entities
          for y in range(len(linkedEntities)):
               le_string = le_string + linkedEntities[y]['entityId'] + " "
     if 'temporalAssessment' in entmen:
          ent_temporal = entmen['temporalAssessment']['value']
     if 'certaintyAssessment' in entmen:
          ent_cert = entmen['certaintyAssessment']['value']
     if 'temporalAssessment' in entmen:
          ent_subj = entmen['subject']['value']
     return medEntity(
          id = entmed_id,
          med_type = entmed_type,
          med_content = entmed_content,
          linked_ents = le_string,
          med_time = ent_temporal,
          med_cert = ent_cert,
          med_subj = ent_subj
     )

if __name__ == "__main__":
  app.run()