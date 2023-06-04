import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "vacaition-8be20",
  "private_key_id": "78cb438c854ff18bf09862424423ea3ce4d49c0f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCNEcwgKgtVsLsd\nQMq4mcuLPR11lUBvqpzot1sOazSOwPHU2GP4aMbxa6nkldWMxnifAAnaZaRMdjnt\nzaDssgFkLMDcYSyb9PJ+521OFy5rQEaEFKww4a968+Tls3QcWV8I4qoFfzZ9++2u\nYLVHSPLm6ecO3RxiKpcrGw38S+EXlLwUNaZ+mQOeqWtc8dQbrn3kiRTGW9BNNY/n\n/PLKkEIXSw6H9gUV/CfZfGwRVbIpDwpdGtjN7N3e13GMPP1iwNAWOaLAsPaxNzsO\neStULeRIBiU9Madt6jDb2LuDukyUE7XHMMI6D567bbGtZ0pFFjUXupldlzQf6ozR\nDQExJIJ7AgMBAAECggEACWJHMVaKpXsZn1MJiSkV3J/Gn2U7wZHYWTSlNnrUJrDY\nBWAVmlch8LpINV/wMiqbqHwAq8n6GWn95X85trUKmabOd3pxVLiBDwcHAtxQ5qqC\nZlPXtnK00Rl7PvpmfWJGi5lEVRRGxC+nemONe33zRoAFsjvsIO2TW7czgXZstTxC\n04oyKzQHkzIRq0kqF/ZvH9wY1ZCb08tOmzgIZsSOvaMiAc+Ta/tBY/YuS9g4h9+G\nNBaa0ZbjT+qwaAyK82ApEqrV/E8RX/sG9Gk4m4UvEXoXmkaz4miCcCPF/V7pbbyQ\nywhr2V0RIq8xJOWIQcjOGDQ1fIVTogqRyggOJ3Gi8QKBgQDA0Kp7PRSvSB0baNPK\nIWTm8VBI2KWv5XEXVU4RwdFQ60bG6zhrNUwd/yGG82GwIj9WLcv71ahJsspwauG6\ne9gHI3L3YmM6F/jD2dcQsRecFsNhLCUZEEq6K80Sl2m2jaYmjAv/PqlljYNcAigl\nrEpZrj4BceGeV9boFmacPWG20QKBgQC7TCysKEi1vsWTFOxs+d/xbId5Ht2JHOr/\nqYSXhogQyFBJjaxpQJIggcwvQKCwMQeLVjkNo6MKGRVadlwr6r/FOsZla+yR4BGi\ni9rbrCwBCncctzce0O4wn4g7TzV/WX201j789B9nfxvvi6xMeucricQiqwmjFwRb\nM+u0hWAPiwKBgQCdN0dat0IvbdB18fKGpNX+TJMW4reuhZnB2cePSQbgQQbz2QWm\nvM10w/vVaoujrzkPjsX9cIgIl6TjJvMpOCO8JlZuiiW4T6WCJBRtQsiqeBEVIYaa\nOiOES4Sp/RWwSS1JzvVVSQWcjVenZQbROPtixmU+jlnV32+Wy/Ucvhv3kQKBgHsp\nKQr/5mgUjWkdTiaO3VKs8hyUTkr2SBVcDENzhI+8mQb08VW4zx4vG+xKjB+v7e0T\nAqtUWkaundsBj7SVRgtUjddtc3+tHwuK+ZyQB9ObZR3t4IIUEzzH+tY9TMl0OHQs\nmfjOMsRk0iLf7qnP+6kmi2HcpJao8QVkC++F8NfnAoGAPDxrkkffRkWHw37arwDw\nO4CC8TpANhsK0TaJeG1Mbdjp/DEDr6X8+C4lD3QBObC50LhFo9LbPkUxhqDKwcVW\nS2S4iUqoIeNhttphvyToFeuf0aZpR+GuECVjL/WBcCDi7zz/jw7PkshEnYLs8x4S\n43H4nNp8aLoYD5RM3NXSOTk=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-4298q@vacaition-8be20.iam.gserviceaccount.com",
  "client_id": "104116296895869296820",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-4298q%40vacaition-8be20.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

firebase_admin.initialize_app(cred)
db = firestore.client()
collection = db.collection('data')

def getUserInfo(u_id: str):
  doc = collection.document(u_id)
  print("doc in getUserInfo:", doc)
  infos = doc.collection('info')
  for info in infos.stream():
    print("\ninfo in stream:", info.to_dict())
    return info.to_dict()

def getAllUserInfo(except_id: str = None):
  res = []
  for doc in collection.stream():
    if doc.id != except_id:
      doc2 = collection.document(doc.id)
      infos = doc2.collection('info')
      # res.append(infos.stream()[0].to_dict())
      for info in infos.stream():
        dict = info.to_dict()
        dict['u_id'] = doc.id
        res.append(dict)
        break
  return res
  
# def getQuestionnaire(u_id: str):
#   doc = collection.document(u_id)
#   infos = doc.collection('quest').order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1)
#   for info in infos.stream():
#     print("info:", info.to_dict())
#     return info.to_dict()