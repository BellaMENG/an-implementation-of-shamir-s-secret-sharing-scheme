import ssss

# print(ssss.encrypt_str("secret",10,2))

def fetch_shares(secret, intercept, degree):
    shares = ssss.encrypt_str(secret, intercept, degree)
    result = ''
    for share in shares:
        result += share + '\n'

    return result


def fetch_secret(shares, degree):
    secret = ssss.decrypt_str(shares, degree)
    return secret