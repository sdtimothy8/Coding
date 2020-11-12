#include <string>
#include <iostream>
#include <vector>

using namespace std;

class HasPtr
{
	public:
		HasPtr(const string &s = string()):
			ps(new string(s)),i(0),refCount(new size_t(1)){}
		//这个类需要析构函数，那它也需要拷贝构造函数
		~HasPtr();
		//Copy constructor
		HasPtr(const HasPtr &s):
			ps(s.ps),i(s.i),refCount(s.refCount){ increaseRefCount(); }
		// Copy operator
		HasPtr &operator=(const HasPtr &rhs);
		string getStr() const { return *ps; }
		int getValue() const { return i; }
		void increaseRefCount() {  ++*refCount; }
		void decreaseRefCount() {  --*refCount; }
		
	private:
		string *ps;
		int i;
		size_t* refCount;
};

HasPtr& HasPtr::operator=(const HasPtr &rhs)
{
	//这里要考虑将左侧对象ps指向的原有资源先释放掉。
	++*rhs.refCount;
	if( 0 == --*refCount )
    {
		delete ps;
		delete refCount;
	}
	ps = rhs.ps;
	i = rhs.i;
	refCount = rhs.refCount;
	
	return *this;
}

HasPtr::~HasPtr()
{
	if( 0 == --*refCount)
	{
		delete ps;
		delete refCount;
	}
}


int main(int argc, char** argv)
{
	HasPtr test;
	HasPtr test1;
	test1 = test;

	return 0;
}
