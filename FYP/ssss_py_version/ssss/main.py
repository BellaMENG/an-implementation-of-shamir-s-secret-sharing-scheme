from split import encrypt_string


if __name__ == "__main__":
    print("Please input the secret:")
    secret = input()
    intercept = 10
    field_base = 8
    degree = 2


    shares = encrypt_string(secret, intercept, degree, field_base)
    print("The shares are:")
    for share in shares:
        print(share)
