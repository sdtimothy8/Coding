#include <string>
#include <iostream>
#include <vector>

using namespace std;

class HasPtr
{
	// swap函数
	friend void swap( HasPtr& lhs, HasPtr& rhs );
	public:
		HasPtr(const string &s = string()):
			ps(new string(s)),i(0){}
		//这个类需要析构函数，那它也需要拷贝构造函数
		~HasPtr(){ delete ps; }
		//Copy constructor
		HasPtr(const HasPtr &s):
			ps(new string(*(s.ps))),i(s.i){}
		// Copy operator
		HasPtr &operator=(const HasPtr &rhs);
		bool operator<( const HasPtr& );

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

bool HasPtr::HasPtr( const HasPtr& rhs )
{
	return *this->ps < *rhs.ps;
}

inline
void swap( HasPtr& lhs, HasPtr& rhs )
{
	//print message
	std::cout << "call swap function!!" << std::endl;
	using std::swap;
	swap(lhs.ps, rhs.ps);
	swap(lhs.i, rhs.i);
}

void print(const HasPtr& test)
{
	std::cout << test.getStr() << "||" << test.getValue() << std::endl;
}

int main(int argc, char** argv)
{
	string str1("love"), str2("jiale");
	HasPtr test1(str1),test2(str2);
	swap(test1, test2);
	print(test1);
	print(test2);
	
	return 0;
}
