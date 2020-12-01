#include <iostream>
#include <string>
#include <memory>
#include <vector>

using std::string;
using std::vector;


class StrVec
{
public:
	StrVec();
	StrVec(size_t n, const string&);
	StrVec(const StrVec&);
	StrVec& operator=(const StrVec&);
	~StrVec();
	//member function
	void push_back(const string&);
	string pop_back();
	size_t size();
	size_t capacity();
	bool empty();
	
private:
	string* elements;
	string* first_free;
	string* cap;
	static allocator<string> alloc;
};

StrVec::StrVec():
elements(nullptr),
first_free(nullptr),
cap(nullptr)
{}

StrVec::StrVec(size_t n, const string& str):
elements(nullptr),
first_free(nullptr),
cap(nullptr)
{
	elements = alloc.allocate(n);
	first_free = elements + n;
	cap = first_free;
}

StrVec::~StrVec()
{
	delete [] elements;
}

bool StrVec::empty()
{
	return elements == first_free;
}

size_t StrVec::size()
{
	return first_free - elements;
}

size_t StrVec::capacity()
{
	return cap - elements;
}


int main(int argc, char** argv)
{
	string* pstr1 = new string("love");
	string* const pstr2 = new string[10]{"I", "love", "God", string(3,'!')};
	std::cout << "pstr2 + 2: " << *(pstr2 + 2) << std::endl;
	string* pstr3 = pstr2;
	++pstr3;
	++pstr3;
	std::cout << "pstr3 - pstr2: " << pstr3 - pstr2 << std::endl; 
	
	vector<string> strVec(10, string("jiaen"));
	for(auto iter : strVec)
		std::cout << iter << std::endl;
	std::cout << strVec.size() << std::endl;
	std::cout << strVec.capacity() << std::endl;

	return 0;
}

