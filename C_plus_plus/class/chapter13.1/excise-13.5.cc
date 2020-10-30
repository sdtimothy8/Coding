#include <iostream>
#include <string>

using std::string;

class HasPtr {
public:
	// Constructor
	HasPtr(const string& s = string()):
    ps(new string(s)),
	i(0)
	{}
	// Copy constructor
	HasPtr(const HasPtr& obj);
private:
	string *ps;
	int i;
};

HasPtr::HasPtr(const HasPtr& obj):
	ps( new string(*(obj.ps)) ),
	i(obj.i)
	{}


// Main Function
int main( int argc, char** argv )
{
	return 0;
}
