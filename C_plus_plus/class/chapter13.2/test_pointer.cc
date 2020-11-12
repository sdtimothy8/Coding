#include <iostream>
#include <cstdio>
#include <string>

using namespace std;

/*
 * class HasPtr的行为表现的像指针一样
 * 即：每个HasPtr对象共享同一份 string* ps
 */

class HasPtr
{
public:
	//构造函数
	HasPtr(const string& s = string()):
	ps(new string(s)),i(0), use(new size_t(1)){}
	// 析构函数
    ~HasPtr();
	//拷贝构造函数
	HasPtr(const HasPtr& c):
	ps(c.ps),i(c.i),use(c.use){ ++*use; }
    //拷贝赋值运算符
    HasPtr& operator=(const HasPtr& rhs);
private:
	std::string* ps;
	int 		i; 
	size_t*		use;
};

HasPtr& HasPtr::operator=(const HasPtr& rhs)
{
	// 为了保证同一个对象自我赋值是安全的，需要先创建新的对象
	++*rhs.use;
	if(0 == --*use)
	{
		std::cout << "release resources here!!" << std::endl;
		delete ps;
		delete use;
	}
	ps = rhs.ps;
	i = rhs.i;
	use = rhs.use;
	
	return *this; 
}

HasPtr::~HasPtr()
{
	std::cout << "~Has();" << *ps << "||" << *use << std::endl;
	if( 0 == --*use )
	{
		delete ps;
		delete use;
	}
}

int main(int argc, char** argv)
{
	string str("love"), str1 = "jiaen";
	HasPtr p1(str);
	HasPtr p2(str1);
	p2 = p1;
	std::cout << "=================" << std::endl;
	return 0;
}
