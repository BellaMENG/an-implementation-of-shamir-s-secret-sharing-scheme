from pyfinite import ffield


def convert_hex_to_dec_array(hex_array):
    '''
    :param hex_array: array of hexadecimal values
    :return: the corresponding of decimal values
    '''
    dec_array = []
    for hex_v in hex_array:
        dec_array.append(int(hex_v, 16))

    return dec_array


def get_points(shares, field_base=8):
    '''
    :param shares: a list of shares. before '-', it is the hex value of x's; after '-', hex values of y's concatenated to one string
    so we determine the number of characters in the original secret by the length of the string after '-'
    :return: return a list of list. xy_values[0] contains all the integer value of the x_i's
    the following lists contains y_values of each character in the secret, following the order
    '''
    len_of_hex = int(field_base / 4)
    x_hex = []
    y_shares = []
    length = 0
    for i in range(len(shares)):
        x, y = shares[i].split('-')
        x_hex.append(x)
        y_shares.append(y)
        if i == 0:
            length = int(len(y)/len_of_hex)

    num_n = len(x_hex)
    x_values = convert_hex_to_dec_array(x_hex)
    y_values_list = []
    for i in range(length):
        y_hexs = []
        for j in range(num_n):
            # TODO: change 2 to a number according to field_base
            y_hex = y_shares[j][len_of_hex*i: len_of_hex*i+len_of_hex]
            y_hexs.append(y_hex)

        y_values_list.append(y_hexs)
    # print("y_values_list:", y_values_list)
    xy_values = [x_values]
    for y_value in y_values_list:
        y_dec = convert_hex_to_dec_array(y_value)
        xy_values.append(y_dec)

    return xy_values


def lagrange_interpolation(points, field_base=8, x0=0):
    '''
    :param points: a list of two lists. the first list element is the list of x values, the second list element is the list of y values
    :param field_base: base of the field. usually 8
    :param x0: f(x0) is the secret. We set x0 to be 0
    :return: s0, which is also the constant term of the polynomial
    '''
    x_values, y_values = points
    F = ffield.FField(field_base)
    f_x = 0
    for i in range(len(x_values)):
        numerator, denominator = 1, 1
        for j in range(len(x_values)):
            if i == j:
                continue
            numerator = F.Multiply(numerator, F.Subtract(x0, x_values[j]))
            denominator = F.Multiply(denominator, F.Subtract(x_values[i], x_values[j]))

        lagrange_polynomial = F.Multiply(numerator, F.Inverse(denominator))
        f_x = F.Add(f_x, F.Multiply(y_values[i], lagrange_polynomial))

    return chr(f_x)


def reconstruct_secret(shares, degree, field_base=8):
    '''
    :param shares: shares. eg. shares = ['52-4cb1787cc758426bc82aebb44050', 'e1-31770e32acb4091ca4e43c000316', 'e2-078f51a8d8e4f2f2b2b00529de62']
    :param degree: the degree of the polynomial
    :param field_base: usually 8
    :return: return the original secret in string
    '''
    if len(shares) <= degree:
        raise ValueError("The number of shares must be ")
    xy_value = get_points(shares, field_base)
    x_values = xy_value[0]
    secret = ''
    for i in range(1, len(xy_value)):
        y_values = xy_value[i]
        s = lagrange_interpolation([x_values, y_values], field_base, 0)
        secret += s

    return secret


'''
x_values: [170, 0, 121, 213, 109, 252, 117, 15, 118, 112]
secret: 2 ; and y_results: [231, 50, 89, 227, 91, 69, 70, 33, 74, 37]
secret: 3 ; and y_results: [244, 51, 148, 193, 210, 117, 124, 37, 130, 16]
y_shares: ['aa-e7f4', '00-3233', '79-5994', 'd5-e3c1', '6d-5bd2', 'fc-4575', '75-467c', '0f-2125', '76-4a82', '70-2510']
'''
'''
shares = ['52-4cb1787cc758426bc82aebb44050', 'e1-31770e32acb4091ca4e43c000316', 'e2-078f51a8d8e4f2f2b2b00529de62',
          '3d-adc0e36c837091a03687dbc7afa7', 'a3-bd2ffde3f390d32cbaab5f9b49e7', 'b1-976f0bc0ff3e82d17b22498b617e',
          '37-162c0bd022e9838743a75c4710dc', '97-e993c0da8540d8659c3d5987e13b', '9c-fa466301e4328b2a9bc01a63c478',
          '16-1441857bfd71ab89405b2fd66685']
shares for 'this is secret'
'''
'''
shares = ['7a-c5032b508d42', 'e0-bc0400d54d36', '95-0c2f931d6bd3', 
            '2f-ac4569a98f19', '12-3c865bcd615f', 'e5-709d46d2b8e2', 
                'bc-349202152469', 'f6-ce34a32bea79', 'f4-147aa3b9ecca', 'c2-bf27d1766f3b']
shares for 'seCrEt'
'''
if __name__ == "__main__":
    field_base = 8
    x0 = 0
    degree = 2
    num_of_shares = 10
    shares = []
    for i in range(degree+1):
        print("Please input share " + str(i+1) + ": ")
        shares.append(input())

    secret = reconstruct_secret(shares, degree, field_base)
    print("The secret is:", secret)