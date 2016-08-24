import gspread
import json
import requests

from config import carecenter_config
from oauth2client.service_account import ServiceAccountCredentials


def import_data():
    print "Import All Data"

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(carecenter_config["API_KEY_FILE"], scope)
    gc = gspread.authorize(credentials)
    document = gc.open("CareCenterDataLoad")

    import_tags(document.worksheet("Tags"))
    import_organizations(document.worksheet("Organizations"))
    import_services(document.worksheet("Services"))


def import_organizations(worksheet):
    print "Importing Organizations"
    url = carecenter_config["API_BASE_URL"] + "api/organizations/"
    response = requests.get(url)
    currentOrgs = response.json()

    # print currentOrgs

    rows = worksheet.get_all_records()
    for row in rows:
        exsists_in_current_orgs = False
        mapped_org = {
            "name": row["Name"],
            "description": row["Description"],
            "web_url": row["WebUrl"]
        }
        for org in currentOrgs:
            if org["name"] == row["Name"]:
                exsists_in_current_orgs = True
                break

        if not exsists_in_current_orgs:
            response = requests.post(url, data=mapped_org)
            print "Added Org [%s]", mapped_org["name"]


def import_services(worksheet):
    print "Importing Services"


def import_tags(worksheet):
    print "Importing Tags"


if __name__ == "__main__":
    import_data()
