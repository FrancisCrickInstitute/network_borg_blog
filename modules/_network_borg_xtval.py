#!/usr/bin/env python3

# extract_value() module courteous of Todd Birchard. Given a key name, it searches
# the JSON response and extracts the value. Designed to be flexible and agnostic
# https://hackersandslackers.com/extract-data-from-complex-json-python/

__author__      = 'Todd Birchard'
__copyright__   = 'See URL'

def xtval(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results
