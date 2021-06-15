from dotenv import load_dotenv
from os import environ
import json

load_dotenv()

def get_creds():
    data_set = {
        "type": environ.get("type"),
        "project_id": environ.get("project_id"),
        "private_key_id": environ.get("private_key_id"),
        "private_key": environ.get("private_key").replace('\\n', '\n'),
        "client_email": environ.get("client_email"),
        "client_id": environ.get("client_id"),
        "auth_uri": environ.get("auth_uri"),
        "token_uri": environ.get("token_uri"),
        "auth_provider_x509_cert_url": environ.get("auth_provider_x509_cert_url"),
        "client_x509_cert_url": environ.get("client_x509_cert_url")
    }
    return json.loads(json.dumps(data_set))