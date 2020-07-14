#include <string>
#include <iostream>
#include <vector>

using namespace std;

class HasPtr
{
	public:
		// 构造函数分配新的string和计数器，将计数器置为1
		HasPtr(const string &s = string()):
			ps(new string(s)),i(0),use(new std::size_t(1)){}
		//这个类需要析构函数，那它也需要拷贝构造函数
		~HasPtr()
		{ 
			if(0 == --*use)
			{
				delete ps;
				delete use;
			}
		}
		//Copy constructor
		HasPtr(const HasPtr &s):
			ps(s.ps),i(s.i),use(s.use){++*use;}
		// Copy operator
		HasPtr &operator=(const HasPtr &rhs);
		
	private:
		string *ps;
		int i;
		std::size_t *use;
};

HasPtr& HasPtr::operator=(const HasPtr &rhs)
{
	//这里要考虑将左侧对象ps指向的原有资源先释放掉。
	++*rhs.use;
	if(--*use == 0)
	{
		delete ps;
		delete use;
	}
	ps = rhs.ps
	i = rhs.i;
	use = rhs.use;
	return *this;
}

int main(int argc, char** argv)
{
	HasPtr test;
	HasPtr test1;
	test1 = test;

	return 0;
}
