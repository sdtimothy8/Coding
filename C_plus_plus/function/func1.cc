#include <iostream>
#include <cassert>
#include <cstdio>

using std::string;
int fact(int);

bool isShorter(const string& str1, const string& str2)
{
	return str1.size() < str2.size();
}

int main() {
	
	int value = 5;
	int result = fact(value);
	std::cout << "Result is: " << result << std::endl;
	
	std::string str1("love"), str2("huimin");
	if (isShorter(str1, str2))
		std::cout << "Str1 is shorter than str2!" << std::endl;
	else
		std::cout << "Str1 is longer than str2!" << std::endl;

	return 0;
}

int fact(int value) 
{
	assert(value >= 1);
	int result = 1;
	for (int i = 1; i <= value; ++i)
		result *= i;

	return result;
}

