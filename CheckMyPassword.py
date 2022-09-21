import requests
import hashlib
import os
import sys


def request_data(char):
    # Requesting api data
    url = 'https://api.pwnedpasswords.com/range/' + char
    res = requests.get(url)
    if res.status_code != 200:
        return "Failed to fetch the data"
    return res


def get_password_leak_counts(result, trail):
    # splitting the api data and checking for trail
    result = (line.split(':') for line in result.text.splitlines())
    for h, c in result:
        if trail == h:
            return c
    return 0


def pwned_password_check(password):
    # hash the password using hashlib's sha1 method
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest()
    head, trail = sha1password[:5], sha1password[5:]
    result = request_data(head)
    return get_password_leak_counts(result, trail.upper())


if __name__ == '__main__':
    try:
        # reading passwords from the text file
        with open(os.path.join(sys.path[0], 'Passwords.txt'), 'r') as my_file:
            passwords = my_file.read().split('\n')
            for password in passwords:
                count = pwned_password_check(password)
                if count:
                    print(f'{password} was hacked {count} times.', end='\n')
                else:
                    print(f'{password} was not hacked.', end='\n')

    except:
        print("Something went wrong")
