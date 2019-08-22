//#include <cstdlib>
#include <cstdio>
#include <iostream>

int main()
{
	// Const pointer and pointer point to const value
	int length = 100;
	int width = 200;
	//const int *len_ptr = &length;
	//int *const len_ptr = &length;
	//int *len_ptr = &length;
	*len_ptr = 400;
	len_ptr = &width;
	*len_ptr = 500;
	std::cout << "Length is: " << length << std::endl;
	std::cout << "Width is: " << width << std::endl;

	const double pi = 3.14;
	const double &ri = pi;
	std::cout << &pi << std::endl;
	std::cout << "Size of int is: " << sizeof(int) << std::endl;
	std::cout << "Size of double is: " << sizeof(double) << std::endl;
	
	return 0;
}
