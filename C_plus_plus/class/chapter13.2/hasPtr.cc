#include <string>
#include <iostream>
#include <vector>

using namespace std;

class HasPtr
{
	public:
		HasPtr(const string &s = string()):
			ps(new string(s)),i(0){}
		//这个类需要析构函数，那它也需要拷贝构造函数和拷贝赋值运算符
		~HasPtr(){ delete ps; }
		//Copy constructor
		HasPtr(const HasPtr &s):
			ps(new string(*(s.ps))),i(s.i){}
		// Copy operator
		HasPtr &operator=(const HasPtr &rhs);
		string getStr() const { return *ps; }
		int getValue() const { return i; }
		
	private:
		string *ps;
		int i;
};

HasPtr& HasPtr::operator=(const HasPtr &rhs)
{
	//这里要考虑将左侧对象ps指向的原有资源先释放掉。
	auto newp = new string(*(rhs.ps));
	delete ps;
	ps = newp;
	i = rhs.i;
	return *this;
}

int main(int argc, char** argv)
{
	HasPtr test;
	HasPtr test1;
	test1 = test;

	return 0;
}
