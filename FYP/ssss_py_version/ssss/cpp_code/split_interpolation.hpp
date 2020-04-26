
#include <iostream>
#include <string>
#include "create_lut.hpp"
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <iomanip>
#include <vector>


namespace bp = boost::python;
using namespace std;


string inverse_f = "/Users/zmeng/eclipse-workspace/ssss_cpp/ssss/csv_files/inverse_lut.csv";
string multi_f = "/Users/zmeng/eclipse-workspace/ssss_cpp/ssss/csv_files/multiply_lut.csv";
string add_f = "/Users/zmeng/eclipse-workspace/ssss_cpp/ssss/csv_files/add_lut.csv";
string sub_f = "/Users/zmeng/eclipse-workspace/ssss_cpp/ssss/csv_files/sub_lut.csv";

int inverse_lut[FIELD_SIZE];
int multi_lut[FIELD_SIZE*FIELD_SIZE];
int add_lut[FIELD_SIZE*FIELD_SIZE];
int sub_lut[FIELD_SIZE*FIELD_SIZE];

void initialize_interpolation() {
	create_lut(inverse_lut, inverse_f);
	create_2dlut(multi_lut, multi_f);
	create_2dlut(add_lut, add_f);
	create_2dlut(sub_lut, sub_f);
	Py_Initialize();
}


void random_polynomial_coeff(int* coeff, int degree) {
	int upper_bound = pow(2,8);
	for (int i = 0; i < degree; ++i) {
		int random_coeff = rand() % upper_bound;
		coeff[i] = random_coeff;
	}
}

int calculate_shares(int x, int* coeff, int degree, char secret) {
	int result = 0;
	int s0 = int(secret);
	for (int i = degree-1; i >= 0; --i) {
		int multi_v = multi_lut[result*FIELD_SIZE + x];
		result = add_lut[multi_v*FIELD_SIZE + coeff[i]];
	}
	int multi_v = multi_lut[result*FIELD_SIZE + x];
	result = add_lut[multi_v*FIELD_SIZE + s0];
	return result;
}

void encrypt_char(string* y_hexs, int* coeff, char secret, int intercept, int degree) {
	for (int i = 1; i <= intercept; ++i) {
		int y_result = calculate_shares(i, coeff, degree, secret);
		std::stringstream stream;
		stream << std::hex << y_result;
		std::string result( stream.str() );
		if (result.length() == 1)
			result = "0" + result;
		y_hexs[i-1] = result;

	}
}

void encrypt_string(string* shares, string secret, int intercept, int degree) {
	initialize_interpolation();
	srand(time(NULL));
	vector<string> y_shares;
	for (int i = 0; i < intercept; ++i) {
		y_shares.push_back("");
	}
	char * secret_arr = new char [secret.length()+1];
	strcpy (secret_arr, secret.c_str());
	for (int i = 0; i < secret.length(); ++i) {
		int coeff[degree];
		random_polynomial_coeff(coeff, degree);
		char ch = secret_arr[i];
		string y_hexs[intercept];
		encrypt_char(y_hexs, coeff, ch, intercept, degree);
		for (int j = 0; j < intercept; ++j) {
			y_shares[j] += y_hexs[j];
		}
	}
	for (int i = 0; i < intercept; ++i) {
		std::stringstream stream;
		stream << std::hex << i+1;
		std::string x_result( stream.str() );
		if (x_result.length() == 1)
			x_result = "0" + x_result;
		shares[i] = x_result + "-" + y_shares[i];
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

char lagrange_interpolation(vector< vector<int> > points) {
	vector<int> x_values = points[0];
	vector<int> y_values = points[1];
	int f_x = 0;
	for(int i = 0; i < x_values.size(); ++i) {
		int numerator = 1;
		int denominator = 1;
		for (int j = 0; j < x_values.size(); ++j) {
			if (i == j)
				continue;
			int sub_v = sub_lut[x_values[j]];
			numerator = multi_lut[numerator*FIELD_SIZE + sub_v];
			sub_v = sub_lut[x_values[i]*FIELD_SIZE + x_values[j]];
			denominator = multi_lut[denominator*FIELD_SIZE + sub_v];
		}
		int inverse_v = inverse_lut[denominator];
		int lagrange_polynomial = multi_lut[numerator*FIELD_SIZE+inverse_v];
		int multi_v = multi_lut[y_values[i]*FIELD_SIZE+lagrange_polynomial];
		f_x = add_lut[f_x*FIELD_SIZE + multi_v];
	}
	return char(f_x);
}

string reconstruct_secret(string shares[], int degree) {
	initialize_interpolation();
	vector< vector<int> > xy_value;
	get_points(xy_value, shares, degree);
	vector<int> x_values = xy_value[0];
	string secret = "";
	for (int i = 1; i < xy_value.size(); ++i) {
		vector<int> y_values = xy_value[i];
		vector< vector<int> > points;
		points.push_back(x_values);
		points.push_back(y_values);
		char s = lagrange_interpolation(points);
		secret += s;
	}
	return secret;
}

