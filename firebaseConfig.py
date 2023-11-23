from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

FirebaseConfig = {
    "type": getenv("TYPE"),
    "project_id": getenv("project_id"),
    "private_key_id": getenv("private_key_id"),
    "private_key": getenv("private_key"),
    "client_email": getenv("client_email"),
    "client_id": getenv("client_id"),
    "auth_uri": getenv("auth_uri"),
    "token_uri": getenv("token_uri"),
    "auth_provider_x509_cert_url": getenv("auth_provider_x509_cert_url"),
    "client_x509_cert_url": getenv("client_x509_cert_url"),
    "universe_domain": getenv("universe_domain"),
}
