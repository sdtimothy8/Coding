#include <iostream>
#include <string>

using std::string;

int main() {
	string line;
	std::cout << "Please input some words:" << std::endl;
	while ( getline(std::cin, line) )
	{
		std::cout << line << std::endl;
	}

	return 0;
}
