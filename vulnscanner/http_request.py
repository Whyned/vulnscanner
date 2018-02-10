import urllib

def request(host, port, path, method, options={}):
    url = craft_url(host, port, path)
    print(url)


def craft_url(host, port, path='/', ssl=None):
    if ssl is None and port == 443:
        ssl = True
    prot = 'https' if ssl else 'http'
    return '%s://%s:%s%s' %(prot, host, port, path)
