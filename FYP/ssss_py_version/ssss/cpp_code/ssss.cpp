#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
#include <boost/python/args.hpp>
#include <boost/python/list.hpp>
#include <boost/python/extract.hpp>
#include <iostream>
#include <string>
#include "split_interpolation.hpp"

using namespace boost::python;

char const* foo(int x, int y) {return "foo";}

boost::python::list encrypt_str(std::string secret, int intercept, int degree) {
    string shares[intercept];
    encrypt_string(shares, secret, intercept, degree);
    boost::python::list list_shares;
    for (int i = 0; i < intercept; ++i) {
        list_shares.append(shares[i]);
    }
    return list_shares;
}

string decrypt_str(boost::python::list shares, int degree) {
    string shares_arr[degree+1];
    for (int i = 0; i < degree+1; ++i)
        shares_arr[i] = boost::python::extract<std::string>(shares[i]);
    return reconstruct_secret(shares_arr, degree);
}

BOOST_PYTHON_MODULE(ssss)
{
    def("foo", foo, args("x", "y"), "foo's docstring");
    def("encrypt_str", encrypt_str, args("secret", "intercept", "degree"), "encrypt_function");
    def("decrypt_str", decrypt_str, args("shares", "degree"), "decrypt_function");
}