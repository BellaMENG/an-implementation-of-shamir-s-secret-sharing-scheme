from utilitybelt import secure_randint as randint
from pyfinite import ffield
import time

# we can utilize pyfinite package
#TODO: get input from keyboard/download shares


def random_polynomials_coeff(degree, field_base=8):
    """
    :param degree: degree of the parameter, which is k-1
    :param field_base: the base of the finite field
    :return: return the coefficients
    """
    if degree < 0:
        raise ValueError("Degree cannot be a negative number.")
    coefficients = []
    upper_bound = 2**field_base - 1
    for i in range(degree):
        random_coeff = randint(0, upper_bound)
        coefficients.append(random_coeff)
    return coefficients


def generate_x_values(intercept):
    x_values = []
    for i in range(intercept):
        x_values.append(i)
    return x_values


def calculate_shares(x_value, coefficients, secret, field_base=8):
    """
    :param x_value: the x value
    :param coefficients: coefficients of the polynomial, coefficient[i] is the coefficient of x^(i+1)
    :param field_base: field base
    :param secret: the character secret
    :return: return the y value correspond to the x value
    """
    F = ffield.FField(field_base)
    s0 = ord(secret)
    result = 0
    for i in reversed(range(len(coefficients))):
        result = F.Add(F.Multiply(result, x_value),coefficients[i])

    result = F.Add(F.Multiply(result, x_value), s0)
    return result


def convert_dec_to_hex(dec):
    """
    :param dec: decimal value
    :return: return the corresponding hex value of the dec
    """
    return hex(dec).split('x')[-1]


def convert_dec_array_to_hex_array(decs, field_base=8):
    """
    :param decs: list of decimal values
    :return: list of hex values
    """
    result = []
    for dec in decs:
        hex_v = convert_dec_to_hex(dec)
        length = len(hex_v)
        if length < field_base/4:
            hex_v = (int(field_base/4)-length)*'0' + hex_v
        result.append(hex_v)
    return result


def encrypt_char(coefficients, x_values, secret, intercept, degree, field_base=8):
    """
    :param x_values: list of x_values. eg. x_values = [145, 51, 167, 212, 64, 42, 127, 96, 236, 52]
    :param secret: a character. eg. 's'
    :param intercept: how many shares we want to generate. eg. n = 10
    :param degree: degree of the polynomial. eg. k-1 = 2
    :param field_base: base of the field. eg. field_base = 8
    :return: array of hex values of corresponding y values
    """
    # coefficients = random_polynomials_coeff(degree, field_base)
    y_results = []
    for i in range(intercept):
        y_result = calculate_shares(x_values[i], coefficients, secret, field_base)
        y_results.append(y_result)
    y_hexs = convert_dec_array_to_hex_array(y_results, field_base)
    return y_hexs


def encrypt_string(secret_str, intercept, degree, field_base=8):
    """
    :param secret_str: string secret. eg. 'this is secret'
    :param intercept: number of shares we want to generate. eg. n = 10
    :param degree: degree of the polynomial. eg. degree = 2 = k-1
    :param field_base: 9
    :return: return the shares.
    """
    if type(intercept) is str:
        intercept = int(intercept)

    if type(degree) is str:
        degree = int(degree)

    if type(field_base) is str:
        field_base = int(field_base)

    x_values = generate_x_values(intercept)
    y_shares = []
    coefficients = random_polynomials_coeff(degree, field_base)
    for i in range(intercept):
        y_shares.append('')
    for c in secret_str:
        y_hexs = encrypt_char(coefficients, x_values, c, intercept, degree, field_base)
        for i in range(intercept):
            y_shares[i] += y_hexs[i]

    x_hexs = convert_dec_array_to_hex_array(x_values)
    for i in range(intercept):
        y_shares[i] = x_hexs[i] + '-' + y_shares[i]
    return y_shares


def encrypt_string_str(secret_str, intercept, degree, field_base=8):
    shares = encrypt_string(secret_str, intercept, degree, field_base)
    shares_str = ''
    for i in range(len(shares)):
        shares_str += shares[i] + '\n'

    return shares_str


if __name__ == "__main__":
    secret = 'seCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEtseCrEt'
    intercept = 10
    field_base = 8
    degree = 2

    for i in range(1, 11):
        t1 = time.time()
        encrypt_string(secret[0:i*10], intercept, degree, field_base)
        t2 = time.time()
        print("length: " + str(i*10) + ",",  "time:", t2-t1)

    # y_shares = encrypt_string_str(secret, intercept, degree, field_base)

    # print(y_shares)
