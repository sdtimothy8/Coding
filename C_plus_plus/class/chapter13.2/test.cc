#include <iostream>
#include <cstdio>
#include <string>

using namespace std;


/*
 * class HasPtr的行为表现的像值一样
 * 即：每个HasPtr对象都有自己的一份string* ps
 */

class HasPtr
{
public:
	//构造函数
	HasPtr(const string& s = string()):
	ps(new string(s)),i(0){}
	// 析构函数
    ~HasPtr(){ delete ps; }
	//拷贝构造函数
	HasPtr(const HasPtr& c):
	ps(new string(*c.ps)),i(c.i){}
    //拷贝赋值运算符
    HasPtr& operator=(const HasPtr& rhs);
private:
	std::string* ps;
	int 	i; 
};

HasPtr& HasPtr::operator=(const HasPtr& rhs)
{
	// 为了保证同一个对象自我赋值是安全的，需要先创建新的对象
	// 再析构左侧对象的资源
	auto newp = new string(*rhs.ps);
	delete ps;
	ps = newp;
	i = rhs.i;
	
	return *this; 
}

int main(int argc, char** argv)
{
	return 0;
}
