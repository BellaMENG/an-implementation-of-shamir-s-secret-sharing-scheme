from utilitybelt import secure_randint as randint
from pyfinite import ffield
# we can utilize pyfinite package
#TODO: get input from keyboard/download shares

def random_polynomials_coeff(degree, field_base):
    '''
    :param degree: degree of the parameter, which is k-1
    :param field_base: the base of the finite field
    :return: return the coefficients
    '''
    if degree < 0:
        raise ValueError("Degree cannot be a negative number.")
    coefficients = []
    upper_bound = 2**field_base - 1
    for i in range(degree):
        random_coeff = randint(0, upper_bound)
        coefficients.append(random_coeff)
    return coefficients


def random_x_values(intercept, field_base):
    '''
    :param intercept: number of shares, n
    :param field_base: the base of finite field
    :return: n X_i's we need
    '''
    upper_bound = 2**field_base - 1
    x_values = []
    for i in range(intercept):
        value_x = randint(0, upper_bound)
        while value_x in x_values:
            value_x = randint(0, upper_bound)
        x_values.append(value_x)
    return x_values


def calculate_shares(x_value, coefficients, field_base, secret):
    '''
    :param x_value: the x value
    :param coefficients: coefficients of the polynomial, coefficient[i] is the coefficient of x^(i+1)
    :param field_base: field base
    :param secret: the character secret
    :return: return the y value correspond to the x value
    '''
    F = ffield.FField(field_base)
    s0 = ord(secret)
    result = 0
    for i in reversed(range(len(coefficients))):
        result = F.Add(F.Multiply(result, x_value),coefficients[i])

    result = F.Add(F.Multiply(result, x_value), s0)
    return result


def convert_dec_to_hex(dec):
    '''
    :param dec: decimal value
    :return: return the corresponding hex value of the dec
    '''
    return hex(dec).split('x')[-1]


def convert_dec_array_to_hex_array(decs):
    '''
    :param decs: list of decimal values
    :return: list of hex values
    '''
    result = []
    for dec in decs:
        hex_v = convert_dec_to_hex(dec)
        if len(hex_v) == 1:
            hex_v = '0' + hex_v
        result.append(hex_v)
    return result


def encrypt_char(x_values, secret, intercept, degree, field_base=8):
    '''
    :param x_values: list of x_values. eg. x_values = [145, 51, 167, 212, 64, 42, 127, 96, 236, 52]
    :param secret: a character. eg. 's'
    :param intercept: how many shares we want to generate. eg. n = 10
    :param degree: degree of the polynomial. eg. k-1 = 2
    :param field_base: base of the field. eg. field_base = 8
    :return: array of hex values of corresponding y values
    '''
    coefficients = random_polynomials_coeff(degree, field_base)
    y_results = []
    for i in range(intercept):
        y_result = calculate_shares(x_values[i], coefficients, field_base, secret)
        y_results.append(y_result)
    y_hexs = convert_dec_array_to_hex_array(y_results)
    return y_hexs


def encrypt_string(secret_str, intercept, degree, field_base=8):
    '''
    :param secret_str: string secret. eg. 'this is secret'
    :param intercept: number of shares we want to generate. eg. n = 10
    :param degree: degree of the polynomial. eg. degree = 2 = k-1
    :param field_base: 9
    :return: return the shares.
    '''
    x_values = random_x_values(intercept, field_base)
    y_shares = []
    for i in range(intercept):
        y_shares.append('')
    for c in secret_str:
        y_hexs = encrypt_char(x_values, c, intercept, degree, field_base)
        for i in range(intercept):
            y_shares[i] += y_hexs[i]

    x_hexs = convert_dec_array_to_hex_array(x_values)
    for i in range(intercept):
        y_shares[i] = x_hexs[i] + '-' + y_shares[i]
    return y_shares


if __name__ == "__main__":
    secret = 'seCrEt'
    intercept = 10
    field_base = 8
    degree = 2


    y_shares = encrypt_string(secret, intercept, degree, field_base)
    print("The shares are:", y_shares)