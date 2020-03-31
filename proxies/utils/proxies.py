from random import choice
from bs4 import BeautifulSoup
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from .user_agents import user_agents


def get_user_agent():
    return choice(user_agents)


def requests_retry_session(
    retries=4, backoff_factor=0.1,
    status_forcelist=(500, 502, 504),
    session=None
):
    session = session or Session()
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


def get_proxies():
    proxies = []
    url     = 'https://www.sslproxies.org/'
    headers = {'User-Agent': get_user_agent()}

    try:
        response = requests_retry_session().get(
            url=url,
            headers=headers,
        )
    except Exception as e:
        raise e

    proxies_doc = response.text
    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    for row in proxies_table.tbody.find_all('tr'):
        if row.find_all('td')[4].string == 'elite proxy':
            proxies.append(':'.join([
                row.find_all('td')[0].string,
                row.find_all('td')[1].string
            ]))

    return proxies


def proxy_was_successful(proxy):
    url     = 'https://httpbin.org/ip'
    headers = {'User-Agent': get_user_agent()}
    proxies = {'http': proxy, 'https': proxy}

    try:
        response = requests_retry_session(retries=0).get(
            url=url,
            headers=headers,
            proxies=proxies,
            timeout=3
        )
    except Exception as e:
        raise e

    if (
        response.status_code == 200 and
        response.json()['origin'] == proxy.split(':')[0]
    ):
        return proxy
    else:
        raise RuntimeError('Proxy was not viable.')