/*
 * create_lut_.hpp
 *
 *  Created on: Apr 30, 2020
 *      Author: уеру
 */

#ifndef CREATE_LUT__HPP_
#define CREATE_LUT__HPP_

#include <iostream>
#include <fstream>
#include <cmath>
#include <string>
#include <sstream>

using namespace std;


#define FIELD_SIZE 256


void create_lut(int* lut, string file_name) {
	ifstream ifile;
	ifile.open(file_name);
	if(!ifile.is_open()) throw std::runtime_error("Could not open file");
	string line;
	getline(ifile,line);
	stringstream ss(line);
	string token;
	int i = 0;
	while (getline(ss,token,',')) {
		int num = std::stoi(token);
		lut[i] = num;
		i++;
	}
	ifile.close();
	ifile.clear();
}


void create_2dlut(int* lut, string file_name) {
	ifstream ifile;
	ifile.open(file_name);
	if(!ifile.is_open()) throw std::runtime_error("Could not open file");
	string line;
	int i = 0;
	while(getline(ifile,line)) {
		stringstream ss(line);
		string token;
		int j = 0;
		while (getline(ss,token,',')) {
			int num = std::stoi(token);
			lut[i*FIELD_SIZE+j] = num;
			j++;
		}
		i++;
	}
	ifile.close();
	ifile.clear();
}





#endif /* CREATE_LUT__HPP_ */
