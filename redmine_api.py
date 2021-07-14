import requests

_get_json = lambda _url, _hdr : requests.get(_url, headers = _hdr)


# Since failing at this point is totally developer issue (as the
# user is not going to give the issue webpage), hence this function
# just exit the code.
def get_json(_url, _hdr):
    try:
        _json = _get_json(_url, _hdr)
        _json.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
    
    return _json.json()

def post_data(_url, _hdr, _data):
    try:
        _ret = requests.post(url = _url, data = _data, headers = _hdr)
        return _ret
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)
