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

	///// initialize
	const char* cp = "Hello World!!!";
	char noNull[] = {'H', 'i'};
	string s11(cp);
	string s12(noNull, 2);
	string s13(noNull);
	string s14(s11, 6, 5);
	cout << "s14:" << s14 << endl;
	string s15(s11, 6);
	cout << "s15:" << s15 << endl;
	// string s16(s11, 20); //Error: out of range
	
	/////substr() function
	string s22("Hello world");
	string s23(s22.substr(0,5));
	cout << "s23:" << s23 << endl;
	string s24(s22.substr(6));
	cout << "s24:" << s24 << endl;

	/////append() function
	string s33("C++ Primer"), s34 = s33;
	s33.insert(s33.size(), " 4th Edition.");
	s34.append(" 4th Edition.");
	cout << "s33:" << s33 << endl;
	cout << "s34:" << s34 << endl;

	/////replace() function
	s33.replace(11, 3, "5th");
	s34.replace(11, 3, "Fifth");
	cout << "s33:" << s33 << endl;
	cout << "s34:" << s34 << endl;
	
	/////find() function
	string name("AnnaBelle");
	string::size_type pos1 = name.find("Anna");//CaseSensitive
	string numbers("1234567890"), name2("r2d2");
	pos1 = name2.find_first_of(numbers);
	cout << "pos1:" << pos1 << endl;
	pos1 = name2.find_first_not_of(numbers);
	cout << "pos1:" << pos1 << endl;

	return 0;
}
