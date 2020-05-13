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

