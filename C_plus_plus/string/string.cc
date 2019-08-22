//#include <cstdlib>
#include <cstdio>
#include <iostream>
#include <string>
#include <cctype>

using std::string;

int main()
{
	// string initialization
	string s1 = "love ";
	string s2("Jiale");
	//string s3(5, '!');
	string s3;
	std::cout << s1 << s2 << s3 << std::endl;
	if (!s3.empty())
		std::cout << "string s3 size is: " << s3.size() << std::endl;
	else
		printf("String s3 is empty!\n");
	
	//Some functions to process string
	string s4("Hello Word!");
	for (auto &c: s4)
		c = toupper(c);
	std::cout << s4 << std::endl;
	
	//usage of []
	string s5("love huimin");
    for (string::size_type index = 0; index < s5.size(); ++index)
		s5[index] = toupper(s5[index]);
	std::cout << s5 << std::endl;
	
	//
	string word;
    std::cout << "Please input a string:" << std::endl;
	std::cin >> word;
	for (auto &c : word)
		if (!ispunct(c))
			std::cout << c;
	std::cout << std::endl;
	
	return 0;
}
