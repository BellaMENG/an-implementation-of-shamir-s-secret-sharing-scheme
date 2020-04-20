from split import encrypt_string


if __name__ == "__main__":
    print("Please input the secret:")
    secret = input()
    print("Please input the field base for finite field:")
    field_base = int(input())
    print("How many shares do you want:")
    intercept = int(input())
    print("How many shares do you need to reconstruct:")
    degree = int(input()) - 1


    shares = encrypt_string(secret, intercept, degree, field_base)
    print("The shares are:")
    for share in shares:
        print(share)


