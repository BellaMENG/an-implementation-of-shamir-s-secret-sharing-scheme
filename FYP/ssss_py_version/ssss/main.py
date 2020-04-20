from split import encrypt_string
import getpass
from interpolation import reconstruct_secret


# remember to check the inputs
if __name__ == "__main__":
    # print("Please input the secret:")
    secret = getpass.getpass('Secret(Not visible on the console):')
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

    new_shares = []
    print("Now we need", degree+1, "shares to reconstruct the original secret.")
    for i in range(degree+1):
        print("Please input share " + str(i+1) + ":")
        new_shares.append(input())

    secret = reconstruct_secret(shares, degree, field_base)
    print("The original secret is:")
    print(secret)
