#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
#include <sstream>
#include <ctime>


#include "split_interpolation.hpp"

using namespace std;


void test_create_lut() {
	string inverse_f = "/Users/zmeng/eclipse-workspace/ssss_cpp/ssss/csv_files/inverse_lut.csv";
	string add_f = "/Users/zmeng/eclipse-workspace/ssss_cpp/ssss/csv_files/add_lut.csv";
	string sub_f = "/Users/zmeng/eclipse-workspace/ssss_cpp/ssss/csv_files/sub_lut.csv";
	string multi_f = "/Users/zmeng/eclipse-workspace/ssss_cpp/ssss/csv_files/multiply_lut.csv";

	int test_inverse_lut[FIELD_SIZE];
	create_lut(test_inverse_lut, inverse_f);
	cout << "Inverse of F(80) is " << test_inverse_lut[80] << endl;

	int test_add_lut[FIELD_SIZE*FIELD_SIZE];
	create_2dlut(test_add_lut, add_f);
	cout << "F(9)+F(33) is " << test_add_lut[9*FIELD_SIZE+33] << endl;

	int test_sub_lut[FIELD_SIZE*FIELD_SIZE];
	create_2dlut(test_sub_lut, sub_f);
	cout << "F(9)-F(33) is " << test_sub_lut[9*FIELD_SIZE+33] << endl;

	int test_multi_lut[FIELD_SIZE*FIELD_SIZE];
	create_2dlut(test_multi_lut, multi_f);
	cout << "F(9)*F(33) is " << test_multi_lut[9*FIELD_SIZE+33] << endl;

}


void test_split(string secret, int intercept, int degree) {
//	void encrypt_string(string* shares, string secret, int intercept, int degree)
//	cout << "secret is: " << secret << endl;
	string shares[intercept];
	clock_t t1 = clock();
	encrypt_string(shares, secret, intercept, degree);
	clock_t t2 = clock();
	cout << "time: " << float(t2-t1)/CLOCKS_PER_SEC << endl;
	for (int i = 0; i < intercept; ++i) {
		cout << shares[i] << endl;
	}
}

void test_get_points(string shares[], int degree) {
	vector< vector<int> > xy_values;
	get_points(xy_values, shares, degree);
	for (int i = 0; i < xy_values.size(); ++i) {
		for (int j = 0; j < xy_values[0].size(); ++j) {
			cout << xy_values[i][j] << " ";
		}
		cout << endl;
	}
}

void test_interpolation(string shares[], int degree) {
	clock_t t1 = clock();
	string secret = reconstruct_secret(shares, degree);
	clock_t t2 = clock();
	cout << "time: " << float(t2-t1)/CLOCKS_PER_SEC << endl;
	cout << secret << endl;

}

void test_random_coeff(int degree) {
	int coeff[degree];
	random_polynomial_coeff(coeff, degree);
	for (int j = 0; j < 10; ++j) {
		for (int i = 0; i < degree; ++i){
			cout << coeff[i] << endl;
		}
	}
}

void test_copy(string share) {
	string cpy = share;
	cout << cpy << endl;
}

int main() {
	cout << "-------- Text secret --------" << endl;
	string secret = "secret";
	int intercept = 10;
	int degree = 2;

	string shares[intercept];
	clock_t t1 = clock();
	encrypt_string(shares, secret, intercept, degree);
	clock_t t2 = clock();
	cout << "time: " << float(t2-t1)/CLOCKS_PER_SEC << endl;
	for (int i = 0; i < intercept; ++i) {
		cout << shares[i] << endl;
	}

	string new_shares[degree+1];
	for (int i = 0; i < 3; ++i) {
		new_shares[i] = shares[i+3];
	}

	t1 = clock();
	string new_secret = reconstruct_secret(new_shares, degree);
	t2 = clock();
	cout << "time: " << float(t2-t1)/CLOCKS_PER_SEC << endl;
	cout << "secret is: " << new_secret << endl;

	cout << endl;
	cout << "-------- Vector secret --------" << endl;
	//void encrypt_pic(vector<vector<int>>& shares, vector<int>& pixels, int intercept, int degree)

	vector<vector<int>> px_shares;
	static const int arr[] = {244, 19, 37, 255, 8, 244, 19, 37, 255, 8};
	vector<int> pxs (arr, arr+sizeof(arr)/sizeof(arr[0]));
	encrypt_pic(px_shares, pxs, 10, 2);

	for (int i = 0; i < intercept; ++i) {
		for (int j = 0; j < pxs.size(); ++j) {
			cout << px_shares[i][j] << " ";
		}
		cout << endl;
	}
	cout << endl;

	cout << "-------- Test Reconstruct --------" << endl;
	vector<vector<int>> xy_values;
	static const int xs[] = {1,2,3};
	vector<int> xs_vect (xs, xs+sizeof(xs)/sizeof(xs[0]));
	vector<vector<int>> y_values;
	for (int i = 0; i <= 2; ++i) {
		y_values.push_back(px_shares[i]);
	}

//	get_int_points(xy_values, xs_vect, y_values, 2);
//
//	for (int i = 0; i < xy_values.size(); ++i) {
//		for (int j = 0; j < degree+1; ++j) {
//			cout << xy_values[i][j] << " ";
//		}
//		cout << endl;
//	}
//	cout << endl;

	vector<int> px_secret;
	reconstruct_vect(px_secret, xs_vect, y_values, 2);
	for (int i = 0; i < px_secret.size(); ++i) {
		cout << px_secret[i] << " ";
	}
	cout << endl;


	return 0;
}
