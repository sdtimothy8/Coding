#include <iostream>
#include <memory>
#include <string>

using namespace std;

/*行为像指针的类*/

class HasPtr {
	public:
		HasPtr( string s = string(), int ival = 0) : ps(new string(s)), i(ival), use(new int(1)){ }
		HasPtr(const HasPtr& s);
		HasPtr& operator=(const HasPtr&);
		~HasPtr();
		string& getStr() const { return *ps; }
		int getVal() const { return i; }

	private:
		void free();
		string* ps;
		int i;
		int* use;
};

void HasPtr::free()
{
	if (--(*use) == 0) {
		//For debug
		std::cout << "Delete obj: " << *ps << std::endl;
		delete ps;
		delete use;
	}
}

HasPtr::~HasPtr()
{
	free();
}

HasPtr::HasPtr(const HasPtr& has)
	: ps(has.ps)
	, i(has.i)
	, use(has.use)
{
	(*use)++;
}

HasPtr& HasPtr::operator=(const HasPtr& rhs)
{
	(*rhs.use)++;
	free();
	ps = rhs.ps;
	i = rhs.i;
	use = rhs.use;

	return *this;
}

int main()
{
	HasPtr hp("jiaen");
	HasPtr tt("love", 88);
	HasPtr hc(hp);
	std::cout << hc.getStr() << " " << hc.getVal() << std::endl;
	tt = hc;
	std::cout << hc.getStr() << " " << hc.getVal() << std::endl;
	return 0;
}
