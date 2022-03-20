from flask import Flask, render_template
from appmodels import create_app
import os
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
import requests
from requests.structures import CaseInsensitiveDict
import json

app = create_app()
db = SQLAlchemy(app)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)

@app.route("/")
def home():
     #request()
     return render_template("home.html")

@app.route("/upload")
def upload():
     #request()
     return render_template("upload.html")

@app.route("/contact_us")
def contact_us():
     #request()
     return render_template("contact_us.html")

#Make form for text intake

def request():
     url = "https://healthcare.googleapis.com/v1/projects/healthhelper-344619/locations/us-central1/services/nlp:analyzeEntities"
     headers = CaseInsensitiveDict()
     headers["Authorization"] = "Bearer ya29.c.b0AXv0zTO_To8DxLoDxnm56FPPLMmwnbYRLSShoxRvFe3pa_AUJcyQl7tbLb_H-Bvjt-lP9sUegdR2XtZJcSEOMPLLq3NmDF3mGBFE2OPBBvhUDCgCqajuhEWhhi_W_KA2VITxD1skoEhBC_ddJKr-RkZ-Td-2RUWo-RuxiETkvIqJmC4qXkKdBZghUoaiVZErtOU8bCKGWwWiYsG9-bFbx7bGBvZvuvg"
     headers["Content-Type"] = "application/json"
     data = '{"nlpService":"projects/healthhelper-344619/locations/us-central1/services/nlp","documentContent":"Insulin regimen human 5 units IV administered.","licensedVocabularies":["SNOMEDCT_US","ICD10CM"]}'
     resp = requests.post(url, headers=headers, data=data)
     print(resp.status_code)
     if resp.status_code == 200:
          data = json.loads(resp.text)
          print(data['entityMentions'])
          #Get every mention
          print(len(data['entityMentions']))
     return None

if __name__ == "__main__":
  app.run()