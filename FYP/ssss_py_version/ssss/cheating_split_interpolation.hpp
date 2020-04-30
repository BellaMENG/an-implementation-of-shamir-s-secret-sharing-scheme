/*
 * cheating_split_interpolation.hpp
 *
 *  Created on: Apr 30, 2020
 *      Author: уеру
 */

#ifndef CHEATING_SPLIT_INTERPOLATION_HPP_
#define CHEATING_SPLIT_INTERPOLATION_HPP_

#include <iostream>
#include <string>
#include "create_lut_.hpp"
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <iomanip>
#include <cstring>
#include <vector>

using namespace std;
#define FIELD_SIZE 256

string inverse_f = "/Users/zhangyi/fyp_lastversion/csv_files/inverse_lut.csv";
string multi_f = "/Users/zhangyi/fyp_lastversion/csv_files/multiply_lut.csv";
string add_f = "/Users/zhangyi/fyp_lastversion/csv_files/add_lut.csv";
string sub_f = "/Users/zhangyi/fyp_lastversion/csv_files/sub_lut.csv";

int inverse_lut[FIELD_SIZE];
int multi_lut[FIELD_SIZE*FIELD_SIZE];
int add_lut[FIELD_SIZE*FIELD_SIZE];
int sub_lut[FIELD_SIZE*FIELD_SIZE];

void initialize_interpolation() {
	create_lut(inverse_lut, inverse_f);
	create_2dlut(multi_lut, multi_f);
	create_2dlut(add_lut, add_f);
	create_2dlut(sub_lut, sub_f);
}

void generate_f_coeff(int* coeff, int degree, char secret) {

	int upper_bound = pow(2,8);
	int s0 = int (secret);
	coeff[0] = s0;
//	cout << "the 0th coefficient of f is: " << coeff[0] << endl;
	for (int i = 1; i < degree + 1; ++i) {
		int random_coeff = rand() % upper_bound;
		coeff[i] = random_coeff;
//		cout << "the" << i << "th coefficient of f is :" << coeff[i] << endl;
	}
}

void generate_g_coeff(int* coeff_f, int* coeff_g, int degree) {

	int upper_bound = pow(2,8);
	int r = rand() % upper_bound;
//	cout << "we choose r = " << r << endl;
//	for (int i = 0; i < degree+1 ; i++){
//		cout << "Generation: the " << i << "th coefficient of f(x) is " << coeff_f[i] << endl;
//	}
	int rs0 = multi_lut[r*FIELD_SIZE+coeff_f[0]];
	coeff_g[0] = sub_lut[rs0];
//	int test_0 = add_lut [coeff_g[0]*FIELD_SIZE + multi_lut[r*FIELD_SIZE+coeff_f[0]]];
//	cout << "test 0 is " << test_0 << endl;
//	cout << "rs0 = " << rs0 << endl;
//	cout << "Generation: the 0st coefficient of g is: " << coeff_g[0] << endl;
	int rs1 = multi_lut[r*FIELD_SIZE+coeff_f[1]];
	coeff_g[1] = sub_lut[rs1];
//	cout << "rs1 = " << rs1 << endl;
//	cout << "Generation: the 1st coefficient of g is: " << coeff_g[1] << endl;
	for (int i = 2; i < degree + 1; ++i) {
		int random_coeff = rand() % upper_bound;
		coeff_g[i] = random_coeff;
//		cout << "Generation: the" << i << "th coefficient of g is :" << coeff_g[i] << endl;
	}
}


int calculate_shares(int x, int* coeff, int degree) {
	int result = 0;
	for (int i = degree; i >= 0; --i) {
		int multi_v = multi_lut[result*FIELD_SIZE + x];
		result = add_lut[multi_v*FIELD_SIZE + coeff[i]];
	}
	return result;
}


void encrypt_char(string* y_hexs, int* coeff,  int intercept, int degree) {
	for (int i = 1; i <= intercept; ++i) {
		int y_result = calculate_shares(i, coeff, degree);
		std::stringstream stream;
		stream << std::hex << y_result;
		std::string result( stream.str() );
		if (result.length() == 1)
			result = "0" + result;
		y_hexs[i-1] = result;
	}
}

void encrypt_string(string* shares_f, string* shares_g, string secret, int intercept, int degree) {
	initialize_interpolation();
	srand(time(NULL));
	vector<string> y_shares_f;
	vector<string> y_shares_g;
	for (int i = 0; i < intercept; ++i) {
		y_shares_f.push_back("");
		y_shares_g.push_back("");
	}
	char * secret_arr = new char [secret.length()+1];
	strcpy (secret_arr, secret.c_str());
	for (int i = 0; i < secret.length(); ++i) {
		int coeff[degree+1];
		int coeff_g[degree+1];
		char ch = secret_arr[i];
		generate_f_coeff(coeff, degree, ch);
		generate_g_coeff(coeff, coeff_g, degree);
		string y_hexs_f[intercept];
		string y_hexs_g[intercept];
		encrypt_char(y_hexs_f, coeff, intercept, degree);
		encrypt_char(y_hexs_g, coeff_g, intercept, degree);
		for (int j = 0; j < intercept; ++j) {
			y_shares_f[j] += y_hexs_f[j];
			y_shares_g[j] += y_hexs_g[j];
		}
	}
	for (int i = 0; i < intercept; ++i) {
		std::stringstream stream;
		stream << std::hex << i+1;
		std::string x_result( stream.str() );
		if (x_result.length() == 1)
			x_result = "0" + x_result;
		shares_f[i] = x_result + "-" + y_shares_f[i];
		shares_g[i] = x_result + "-" + y_shares_g[i];

	}
}


void get_points(vector< vector<int> > &xy_values, string shares[], int degree) {
	vector<int> x_values;
	vector<string> y_shares;
	int length = 0;
	for (int i = 0; i < degree+1; ++i) {
		string x;
		string y;
		string share = shares[i];
		size_t pos = 0;
		string token;
		string delimiter = "-";
		while ((pos = share.find(delimiter)) != std::string::npos) {
		    token = share.substr(0, pos);
		    x = token;
		    share.erase(0, pos + delimiter.length());
		}
		y = share;
		int x_value;
		std::stringstream ss;
		ss << std::hex << x;
		ss >> x_value;

		x_values.push_back(x_value);
		y_shares.push_back(y);
		if (i == 0)
			length = int(y.length()/2);
	}

	xy_values.push_back(x_values);
	int num_n = x_values.size();
	for (int i = 0; i < length; ++i) {
		vector<int> y_values;
		for (int j = 0; j < num_n; ++j) {
			string y_hex;
			string y_share = y_shares[j];
			y_hex = y_share.substr(2*i,2);
			int y_value;
			std::stringstream ss;
			ss << std::hex << y_hex;
			ss >> y_value;
			y_values.push_back(y_value);
		}
		xy_values.push_back(y_values);
	}
}


void  lagrange_interpolation(vector< vector<int> > points, int* coeff) {
	vector<int> x_values = points[0];
	vector<int> y_values = points[1];
	int a1 = 0;
	int a0 = 0;
	for(int i = 0; i < x_values.size(); ++i) {
		int a0_numerator = 1;
		int a1_numerator = 0;
		int denominator = 1;
		for (int j = 0; j < x_values.size(); ++j) {
			if (i == j)
				continue;

			int sub_v = sub_lut[x_values[j]];
			int multi_a1 = multi_lut[a1_numerator*FIELD_SIZE + sub_v];
			a1_numerator = add_lut[a0_numerator*FIELD_SIZE + multi_a1];
			a0_numerator = multi_lut[a0_numerator*FIELD_SIZE + sub_v];
			sub_v = sub_lut[x_values[i]*FIELD_SIZE + x_values[j]];
			denominator = multi_lut[denominator*FIELD_SIZE + sub_v];
		}
		int inverse_v = inverse_lut[denominator];
		int lagrange_polynomial = multi_lut[a0_numerator*FIELD_SIZE+inverse_v];
		int lagrange_polynomial_a1 = multi_lut[a1_numerator*FIELD_SIZE+inverse_v];
		int multi_v = multi_lut[y_values[i]*FIELD_SIZE+lagrange_polynomial];
		int multi_v_a1 = multi_lut[y_values[i]*FIELD_SIZE+lagrange_polynomial_a1];
		a0 = add_lut[a0*FIELD_SIZE + multi_v];
		a1 = add_lut[a1*FIELD_SIZE + multi_v_a1];

	}
//	cout << "a0: " << a0 << endl;
//	cout << "a1: " << a1 << endl;
	coeff[0] = a0;
	coeff[1] = a1;
}

string reconstruct_secret(string shares_f[], string shares_g[],  int degree) {
	initialize_interpolation();
	vector< vector<int> > xy_value_f;
	vector< vector<int> > xy_value_g;
	get_points(xy_value_f, shares_f, degree);
	get_points(xy_value_g, shares_g, degree);
	vector<int> x_values = xy_value_f[0];
	string secret = "";

	bool tests[xy_value_f.size()-1];
	for (int i = 1; i < xy_value_f.size(); ++i) {
		tests[i-1] = false;
		vector<int> y_values_f = xy_value_f[i];
		vector<int> y_values_g = xy_value_g[i];
		vector< vector<int> > points_f;
		vector< vector<int> > points_g;
		points_f.push_back(x_values);
		points_f.push_back(y_values_f);
		points_g.push_back(x_values);
		points_g.push_back(y_values_g);
		int coeff_f[2];
		int coeff_g[2];
		lagrange_interpolation(points_f, coeff_f);
		lagrange_interpolation(points_g, coeff_g);
		secret += char(coeff_f[0]);
//		cout << "The coefficients for f(x) are: " << coeff_f[0] << "   " << coeff_f[1] << endl;
//		cout << "The coefficients for g(x) are: " << coeff_g[0] << "   " << coeff_g[1] << endl;
		for (int r = 0; r < FIELD_SIZE; r++){
			int a0 = coeff_f[0];
			int ra0  = multi_lut[r*FIELD_SIZE + a0];
			int s0 = coeff_g[0];
			int test_1 = add_lut[ra0*FIELD_SIZE + s0];
			int a1 = coeff_f[1];
			int s1 = coeff_g[1];
			int ra1  = multi_lut[r*FIELD_SIZE + a1];
			int test_2 = add_lut[ra1*FIELD_SIZE + s1];
			if (test_1 == 0 && test_2 == 0){
				tests[i-1] = true;
//				cout << "At " << i << "th iteration,  r: " << r << endl;
			}
		}
	}
	for (int i = 0; i < xy_value_f.size() - 1; i++){
		if (tests[i] == false){
			//cout << "At" << i << "th iteration: Cheating detected!!!" << endl;
			return "";
		}
	}

	cout << "No cheating behavior detected!!!" << endl;
	return secret;
}


#endif /* CHEATING_SPLIT_INTERPOLATION_HPP_ */
