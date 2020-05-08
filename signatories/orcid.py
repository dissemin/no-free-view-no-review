# Most functions here are taken from Dissemin (by the same authors)

def jpath(path, js, default=None):
    """
    XPath for JSON!

    :param path: a list of keys to follow in the tree of dicts, written in a string,
                separated by forward slashes
    :param default: the default value to return when the key is not found

    >>> jpath('message/items', {'message':{'items':'hello'}})
    'hello'
    """
    def _walk(lst, js):
        if js is None:
            return default
        if lst == []:
            return js
        else:
            return _walk(lst[1:], js.get(lst[0], {} if len(lst) > 1 else default))
    r = _walk(path.split('/'), js)
    return r

def urlize(val):
    """
    Ensures a would-be URL actually starts with "http://" or "https://".

    :param val: the URL
    :returns: the cleaned URL

    >>> urlize('gnu.org')
    'http://gnu.org'
    >>> urlize(None) is None
    True
    >>> urlize(u'https://gnu.org')
    'https://gnu.org'
    """
    if val and not val.startswith('http://') and not val.startswith('https://'):
        val = 'http://'+val
    return val

def homepage(js):
    """
    Extract an URL for that researcher (if any)
    """
    lst = jpath(
        'person/researcher-urls/researcher-url', js, default=[])
    for url in lst:
        val = jpath('url/value', url)
        name = jpath('url-name', url)
        if name is not None and ('home' in name.lower() or 'personal' in name.lower()):
            return urlize(val)
    if len(lst):
        return urlize(jpath('url/value', lst[0])) or None

def institution(js):
    """
    The name and identifier of the latest institution associated
    with this researcher
    """
    lst = jpath(
        'activities-summary/employments/employment-summary',
        js, default=[])
    lst += jpath(
        'activities-summary/educations/education-summary',
        js, default=[])

    for affiliation in lst:
        name = jpath('organization/name', affiliation)
        return name

    return None

def name(js):
    """
    Returns the name of the researcher
    """
    name_item = jpath('person/name', js)
    name = jpath('credit-name/value', name_item)
    if name:
        return name
    return (jpath('given-names/value', name_item, '') + ' ' +
            jpath('family-name/value', name_item, '')).strip()

def form_data_from_orcid_json(orcid_profile, email):
    return {
        'name': name(orcid_profile),
        'affiliation': institution(orcid_profile),
        'homepage': homepage(orcid_profile),
        'email': email,
        'send_updates': False
    }

