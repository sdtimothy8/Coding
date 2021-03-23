//#include <cstdlib>
#include <cstdio>
#include <iostream>
#include <string>
#include <cctype>

using std::string;
using std::cout;
using std::cin;
using std::endl;

int main()
{
	/////substr() function
	string s22("Hello world");
    string::size_type pos = s22.find_first_of(" ", 0);
	string keyStr(s22.substr(0, pos));
	cout << "keyStr:" << keyStr << endl;
	string valueStr(s22.substr(pos + 1));
	cout << "valueStr:" << valueStr << endl;

    return 0;
}
