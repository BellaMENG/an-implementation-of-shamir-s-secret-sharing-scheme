# -*- coding: utf-8 -*-


from pyfinite import ffield
from utilitybelt import secure_randint as randint
from split import random_polynomials_coeff, encrypt_string,random_x_values, convert_dec_array_to_hex_array, calculate_shares, encrypt_char

def generate_g_polynomial(degree, field_base, f_coefficients, secret):
    '''
    To detect cheating, we generate another polynomial g(x) = a0 + a1x + ... + ak-1x^(k-1), which 
    satisfies a0 + s0*r = 0, a1 + s1*r = 0, r belongs to GF(2^8). 
    Here we denote f(x) = s0 + s1x + ... + sk-1*x^(k-1)
    This function returns [a0, a1, ... , ak-1]
    
    '''
    F = ffield.FField(field_base) 
    if degree < 0:
        raise ValueError("Degree cannot be a negative number.")
    g_coefficients = []
    upper_bound = 2**field_base - 1
    random_r = randint(0, upper_bound)
    s0 = ord(secret)
    a0 = F.Subtract(0,F.Multiply(random_r,s0))
    g_coefficients.append(a0)
    a1 = F.Subtract(0,F.Multiply(random_r,f_coefficients[0]))
    g_coefficients.append(a1)
    for i in range (1, degree):
        random_coeff = randint(0, upper_bound)
        g_coefficients.append(random_coeff)
    return g_coefficients


def calculate_g_shares(x_value, g_coefficients, field_base):
    '''
     function aims to generate the y value corresponding to the x value in polynomial g(x)   
  
    '''
    #print ("g_coefficients[0]:", g_coefficients[0])
    F = ffield.FField(field_base)   
    result = 0
    for i in reversed(range(1, len(g_coefficients)-1)):
        result = F.Add(F.Multiply(result, x_value),g_coefficients[i])

    result = F.Add(F.Multiply(result, x_value), g_coefficients[0])
    return result


def encrypt_char_cheating(x_values, secret, intercept, degree, field_base=8):
    '''
    This function aims to return encrypted value for a single char for polynomials f(x) and g(x)
    '''
    f_coefficients = random_polynomials_coeff(degree, field_base)
    g_coefficients = generate_g_polynomial(degree, field_base, f_coefficients, secret)
    y_results_f = []
    y_results_g = []
    for i in range(intercept):
        y_result_f = calculate_shares(x_values[i], f_coefficients, field_base, secret)
        y_result_g = calculate_g_shares (x_values[i], g_coefficients, field_base)
        y_results_f.append(y_result_f)
        y_results_g.append(y_result_g)
    y_hexs_f = convert_dec_array_to_hex_array(y_results_f)
    y_hexs_g = convert_dec_array_to_hex_array(y_results_g)
    return y_hexs_f, y_hexs_g


def encrypt_string_cheating(secret_str, intercept, degree, field_base=8):
    x_values = random_x_values(intercept, field_base)
    y_shares_f = []
    y_shares_g = []
    for i in range(intercept):
        y_shares_f.append('')
        y_shares_g.append('')
    for c in secret_str:
        y_hexs_f, y_hexs_g = encrypt_char_cheating(x_values, c, intercept, degree, field_base)
        for i in range(intercept):
            y_shares_f[i] += y_hexs_f[i]
            y_shares_g[i] += y_hexs_g[i]

    x_hexs = convert_dec_array_to_hex_array(x_values)
    for i in range(intercept):
        y_shares_f[i] = x_hexs[i] + '-' + y_shares_f[i]
        y_shares_g[i] = x_hexs[i] + '-' + y_shares_g[i]
    return y_shares_f, y_shares_g

if __name__ == "__main__":
    secret = 'seCrEt test'
    intercept = 10
    field_base = 8
    degree = 2


    y_shares_f, y_shares_g = encrypt_string_cheating(secret, intercept, degree, field_base)
    print("y_shares_f:", y_shares_f, '\n', "y_shares_g:", y_shares_g)

    
    

    
    
