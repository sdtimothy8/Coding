#include <iostream>
#include <string>
#include <cstring>

using namespace std;

int main() {
	string str1 = "love jiale";
	string str2 = "love JIAle";

	if (0 == strcasecmp(str1.c_str(), str2.c_str()))
		cout << "str1 is equals to str2!" << endl;
	else
		cout << "str1 is not equals to str2!" << endl;

	return 0;
}
