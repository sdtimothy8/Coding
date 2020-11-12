#include <string>
#include <iostream>
#include <vector>
#include <algorithm>

using std::cout;
using std::string;
using std::vector;
using std::sort;
using std::endl;
using std::to_string;


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
		HasPtr& operator=(const HasPtr &rhs);
		// 赋于新的string
		HasPtr& operator=(const string& rhs);
		// 解引用运算符
		string& operator*() { return *ps; }
		// 重载小于运算符
		bool operator<( const HasPtr& ) const;

		string getStr() const { return *ps; }
		int getValue() const { return i; }
		
	private:
		string *ps;
		int i;
};

typedef std::vector<HasPtr>  PtrVec;

HasPtr& HasPtr::operator=(const HasPtr &rhs)
{
	//这里要考虑将左侧对象ps指向的原有资源先释放掉。
	auto newp = new string(*(rhs.ps));
	delete ps;
	ps = newp;
	i = rhs.i;
	//swap(*this, rhs);
	return *this;
}

HasPtr& HasPtr::operator=(const string& rhs)
{
	*ps = rhs;
	return *this;
}

bool HasPtr::operator<( const HasPtr& rhs ) const
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

void print(const PtrVec& vec)
{
	//传统的for
	//auto iter = vec.begin();
	//for (; iter != vec.end(); ++iter)
	//	std::cout << iter->getStr() << "||" << iter->getValue() << std::endl;
	//范围for
	//iter是vec中的元素类型，即HasPtr
	for (auto iter : vec )
		std::cout << iter.getStr() << "||" << iter.getValue() << std::endl;
		
}

int main(int argc, char** argv)
{
	string str1("love"), str2("jiale");
	HasPtr test1(str1),test2(str2), test3("huimin");
	swap(test1, test2);
	print(test1);
	print(test2);

	//sort the vector 
	PtrVec vec1;
	int n = atoi(argv[1]);
	for (int j = 0; j < argc; ++j)
		cout << argv[j] << endl;
	for ( int i = 0; i < n; ++i )
		vec1.push_back(HasPtr(to_string(i)));
	//print the elements in vector
	print(vec1);
	// Sort the elements in vectors
	sort(vec1.begin(), vec1.end());
	//print the elements in vector
	print(vec1);
	
	return 0;
}
