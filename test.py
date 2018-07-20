import requests
from requests.auth import HTTPBasicAuth
print(requests.get("https://www.profootballfocus.com/data/by_team.php", auth=HTTPBasicAuth("JamiePats", "791PEAsGkuNp")).content)
