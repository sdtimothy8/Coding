#include <iostream>
#include <cstdio>
#include <cstring>
#include <string>

int main ()
{
	char c1[] = {'l', 'o', 'v', 'e'};
	char c2[] = {'l', 'o', 'v', 'e','h','u','i','m','i','n','\0'};
	char c3[] = "love";
	int i1[] = {'5','6','7','8'};
	
	std::cout << "Size of c1: " << sizeof(c1) << std::endl;
	std::cout << "Strlen of c1: " << strlen(c1) << std::endl;
	std::cout << "Size of c2: " << sizeof(c2) << std::endl;
	std::cout << "Size of c3: " << sizeof(c3) << std::endl;
	std::cout << "Size of i1: " << sizeof(i1) << std::endl;
	
	char *b = c2;
	char *e = &c2[sizeof(c2)];
	for (;b != e; ++b)
		std::cout << *b << std::endl;

	std::string s1(10,'c');
	std::cout << s1.length() << std::endl; 
	std::cout << s1.size() << std::endl; 
	
	// Usage string::length(), string::length and strlen()
	char buf[256] = {0};
	buf[0] = 'a';
	buf[1] = 'b';	
	buf[3] = 'd';	
	buf[4] = 'e';	
	std::string sbuf(buf, 6);
	std::cout << "length of sbuf: " << sbuf.length() << std::endl;
	std::cout << "strlen of sbuf: " << strlen(sbuf.c_str()) << std::endl;
	std::cout << "strlen of buf: " << strlen(buf) << std::endl;
	std::cout << "sizeof of buf: " << sizeof(buf) << std::endl;

	return 0;
}
