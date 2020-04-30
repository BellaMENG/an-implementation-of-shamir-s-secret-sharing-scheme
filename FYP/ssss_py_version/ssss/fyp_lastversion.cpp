//============================================================================
// Name        : fyp_lastversion.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <string>
#include "cheating_split_interpolation.hpp"
#include <cmath>
#include <sstream>
#include <ctime>

using namespace std;

int main() {
	string secret = "sEcReT Testing See the average time!!! So we can know whether this is okay.";
	int intercept = 10;
	int degree = 2;

	string shares[intercept];
	string shares_g[intercept];
	clock_t t1 = clock();
	encrypt_string(shares, shares_g, secret, intercept, degree);
	clock_t t2 = clock();
	cout << "time: " << float(t2-t1)/CLOCKS_PER_SEC << endl;
	for (int i = 0; i < intercept; ++i) {
		cout << shares[i] << endl;
		cout << shares_g[i] << endl;
	}
	//shares_g[5] = "06-b4346b85";
	string new_shares_f[degree+1];
	string new_shares_g[degree+1];
	for (int i = 0; i < 3; ++i) {
		new_shares_f[i] = shares[i+4];
		new_shares_g[i] = shares_g[i+4];
	}
	for (int i = 0; i < degree + 1; i++){
		if ((new_shares_f[i].length() != secret.length()*2 + 3) || (new_shares_g[i].length() != secret.length()*2 + 3)){
			cout << "The length of the share is incorrect!!! Cheating detected! " << endl;
			return 0;
		}
	}
	t1 = clock();
	string new_secret = reconstruct_secret(new_shares_f, new_shares_g, degree);
	t2 = clock();
	cout << "time: " << float(t2-t1)/CLOCKS_PER_SEC << endl;
	cout << new_secret << endl;
	return 0;
}
