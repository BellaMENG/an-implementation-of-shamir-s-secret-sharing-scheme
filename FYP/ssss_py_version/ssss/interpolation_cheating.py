# -*- coding: utf-8 -*-

from pyfinite import ffield
from interpolation import get_points



def lagrange_interpolation_getcoefficients(points, field_base=8):
    '''
    :param points: a list of two lists. the first list element is the list of x values, the second list element is the list of y values
    :param field_base: base of the field. usually 8
    :return: a0, a1, a0 is the constant term of polynomial g(x), while a1 is the coefficient of x in polynomial g(x)
    '''
    x_values, y_values = points
    F = ffield.FField(field_base)
    a1 = 0
    a0 = 0
    for i in range(len(x_values)):
        a1_numerator, denominator = 0, 1
        a0_numerator= 1
        for j in range(len(x_values)):
            if i == j:
                continue
            a1_numerator = F.Add(a0_numerator, F.Multiply(a1_numerator, F.Subtract(0, x_values[j])))
            a0_numerator = F.Multiply(a0_numerator, F.Subtract(0, x_values[j]))
            denominator = F.Multiply(denominator, F.Subtract(x_values[i], x_values[j]))

        lagrange_polynomial_a0 = F.Multiply(a0_numerator, F.Inverse(denominator))
        lagrange_polynomial_a1 = F.Multiply(a1_numerator, F.Inverse(denominator))
        a0 = F.Add(a0, F.Multiply(y_values[i], lagrange_polynomial_a0))
        a1 = F.Add(a1, F.Multiply(y_values[i], lagrange_polynomial_a1))

    return a0, a1


def reconstruct_secret_cheating(shares_f, shares_g, degree, field_base=8):
    '''
    :param shares: shares. eg. shares = ['52-4cb1787cc758426bc82aebb44050', 'e1-31770e32acb4091ca4e43c000316', 'e2-078f51a8d8e4f2f2b2b00529de62']
    :param degree: the degree of the polynomial
    :param field_base: usually 8
    :return: return the original secret in string or give a cheating notification
    '''
    F = ffield.FField(field_base)
    if len(shares_f) <= degree or len(shares_g) <= degree:
        raise ValueError("The number of shares must be ")
    if len(shares_f) != len(shares_g):
        raise ValueError("Please enter equal number of shares from f and g")
    xy_value_f = get_points(shares_f)
    x_values_f = xy_value_f[0]
    xy_value_g = get_points(shares_g)
    x_values_g = xy_value_g[0]
    secret = ''
    for i in range(1, len(xy_value_f)):
        y_values_f = xy_value_f[i]
        y_values_g = xy_value_g[i]
        s_f, a1_f = lagrange_interpolation_getcoefficients([x_values_f, y_values_f], field_base)
        s_g, a1_g = lagrange_interpolation_getcoefficients([x_values_g, y_values_g], field_base)
        secret += chr(s_f)
    for r in range (2**field_base):
        test1 = F.Add(s_g, F.Multiply(s_f, r))
        test2 = F.Add(a1_g, F.Multiply(a1_f, r))
        if test1 == 0 and test2 == 0:
            print("No cheating detected!")
            return secret
    print ("Cheating detected!")
    return 0


if __name__ == "__main__":
    field_base = 8
    degree = 2
    num_of_shares = 10
    shares_f = []
    shares_g = []
    for i in range(degree+1):
        print("Please input share " + str(i+1) + " for f(x): ")
        shares_f.append(input())
    
    for i in range(degree+1):
        print("Please input share " + str(i+1) + " for g(x): ")
        shares_g.append(input())

    secret = reconstruct_secret_cheating(shares_f, shares_g, degree, field_base)
    print("The secret is:", secret)

    