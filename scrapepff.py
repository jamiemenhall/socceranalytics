from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except:
        log_error("Error during requests to {0} : {1}".format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)

if __name__ == "__main__":
    print(simple_get("https://www.profootballfocus.com/data/signature.php?tab=signature&season=2017&pos=wrr&teamid=-1&filter=75&conf=-1&yr=-1&wk=1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17"))
