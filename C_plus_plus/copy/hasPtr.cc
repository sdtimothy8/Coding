#include <iostream>
#include <memory>
#include <string>

using namespace std;

/*行为像值的类*/

class HasPtr {
	public:
		HasPtr( string s = string(), int ival = 0) : ps(new string(s)), i(ival) { }
		HasPtr(const HasPtr& s) : ps(new string(*s.ps)), i(s.i) { }
		HasPtr& operator=(const HasPtr&);
		~HasPtr() { delete ps; }
		string& getStr() const { return *ps; }
		int getVal() const { return i; }

	private:
		string* ps;
		int i;
};

HasPtr& HasPtr::operator=(const HasPtr& rhs)
{
	// 考虑自我赋值的问题
	auto newp = new string(*rhs.ps);
	delete ps;
	ps = newp;
	i = rhs.i;
	return *this;
}

int main()
{
	HasPtr hp("jiaen");
	HasPtr tt("love", 88);
	HasPtr hc(hp);
	std::cout << hc.getStr() << " " << hc.getVal() << std::endl;
	hc = tt;
	std::cout << hc.getStr() << " " << hc.getVal() << std::endl;
	return 0;
}
