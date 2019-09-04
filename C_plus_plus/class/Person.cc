#include <iostream>
#include <string>
using std::string;

class Person {
	//Member function
	string getName() const { return _name; }
	string getAddr() const { return _address; }
	
	//Data Member
	string		_name;
	string		_address;
};


int main (int argc, char* argv[])
{
	return 0;
}
