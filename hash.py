"""
Hash file viewing/keys deleting tool

Written by Maksym Trineyev
"""

import argparse
import pickle
import pprint
from sys import version_info
import textwrap


def read_hash() -> dict:
    try:
        with open('hash.pickle', 'rb') as f:
            hash = pickle.load(f)
    except FileNotFoundError:
        print('File "hash.pickle" not found')
        exit(1)
    if not isinstance(hash, dict):
        print('Error in "hash.pickle" file content')
        exit(2)
    return hash

def parse_args() -> tuple:
    parser = argparse.ArgumentParser(
        prog=f'python3 hash.py',
        usage='%(prog)s [options]',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Hash file viewing/keys deleting tool',
        epilog=textwrap.dedent('''
        Examples:
            %(prog)s
                just to print list of the hash
            %(prog)s --delete lastbp LastBP
                to delete "lastbp" and "LastBP" keys
        
        Note:
          1. will be used "hash.pickle" file
          2. the keys are case sensitive''')
    )
    parser.add_argument('-d', '--delete',
        type=str, nargs='+', help='delete records for the first level keys')
    parser.add_argument('-s', '--sort',
        action='store_true', help='print result sorted by keys (from v3.8+)')
    return parser.parse_args().delete, parser.parse_args().sort

def delete_keys(hash: dict, keys_to_delete: list) -> None:
    for key in keys_to_delete:
        try:
            hash.pop(key)
        except KeyError:
            print('Key not found:', key)
            exit(3)
    with open('hash.pickle', 'wb') as f:
        pickle.dump(hash, f)
    return

def print_hash(hash: dict, sort: bool) -> None:
    version = 10 * version_info[0] + version_info[1]
    if version >= 38:
        pprint.pprint(hash, sort_dicts=sort)
    else:
        pprint.pprint(hash)
    print('Total', len(hash), 'record(s)')
    return


if __name__ == '__main__':
    hash = read_hash()
    keys_to_delete, sort = parse_args()
    if keys_to_delete:
        delete_keys(hash, keys_to_delete)
    else:
        print_hash(hash, sort)
