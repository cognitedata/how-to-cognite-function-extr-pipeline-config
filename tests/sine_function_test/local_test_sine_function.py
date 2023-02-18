import os

from cognite.client import ClientConfig, CogniteClient
from cognite.client.credentials import OAuthClientCredentials
from dotenv import load_dotenv

from sine_function import handler

load_dotenv()

CDF_PROJECT = os.environ["COGNITE_PROJECT"]
TENANT_ID = os.environ["TENANT_ID"]
CLIENT_ID = os.environ["CLIENT_ID"]

COGNITE_PROJECT = os.environ["COGNITE_PROJECT"]
CLIENT_NAME = "DEMO CLIENT"
BASE_URL = os.environ["COGNITE_BASE_URL"]

client = None
SCOPES = [f"{BASE_URL}/.default"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]  # store secret in env variable
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"


creds = OAuthClientCredentials(
    token_url=TOKEN_URL, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scopes=SCOPES
)

cnf = ClientConfig(
    client_name=CLIENT_NAME, project=CDF_PROJECT, credentials=creds, base_url=BASE_URL
)

client = CogniteClient(cnf)
print(client.iam.token.inspect())

data = {
    "ExtractionPipelineExtId": "sine-function",
}


# Code used for local Test & Debug
def main():
    handler.handle(client, data)


if __name__ == "__main__":
    main()
