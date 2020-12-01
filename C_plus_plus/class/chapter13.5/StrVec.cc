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
	~StrVec() { free(); }
	//member function
	void push_back(const string&);
	string pop_back();
	size_t size() const;
	size_t capacity() const;
	bool empty() const;
	string* begin() const { return elements; }
	string* end() const { return first_free; }
	
private:
	// tool functions
	void chk_n_alloc() { if (size() == capacity()) reallocate(); }
	void free();
	void reallocate();
	std::pair<string*, string*> alloc_n_copy(const string*, const string*);

	string* elements;
	string* first_free;
	string* cap;
	static std::allocator<string> alloc;
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

//Copy constructor function
StrVec::StrVec(const StrVec& str)
{
	auto data = alloc_n_copy(str.begin(), str.end());
	elements = data.first;
	// copy过程中，一共分配了str.size()个空间，所以cap和first_free
	// 指向同一个位置
	first_free = cap = data.second;
}

//Copy operator = 
StrVec& StrVec::operator=(const StrVec& rhs)
{
	//自赋值问题处理
	auto newdata = alloc_n_copy(rhs.begin(), rhs.end());
	free();
	elements = newdata.first;
	first_free = cap = newdata.second;

	return *this;
}

bool StrVec::empty() const
{
	return elements == first_free;
}

size_t StrVec::size() const
{
	return first_free - elements;
}

size_t StrVec::capacity() const
{
	return cap - elements;
}

void StrVec::push_back(const string& str)
{
	chk_n_alloc();
	alloc.construct(first_free++, str);
}

//
std::pair<string*, string*> StrVec::alloc_n_copy(const string* b, const string* e)
{
	auto data = alloc.allocate(e - b);
	return {data, uninitialized_copy(b, e, data)};
	//return make_pair(data, uninitialized_copy(b, e, data));
}


void StrVec::free()
{
	//不能传递一个空指针给deallocate函数，所以要检查elements是否为空
	//1, destroy the elements
	//2, release the mem of StrVec 
	if (elements)
	{
		for (auto p = first_free; p != elements;)
			alloc.destroy(--p);
		alloc.deallocate(elements, cap - elements);
	}
}

// Reallocate function
void StrVec::reallocate()
{
	size_t newcap_num = size()? capacity() * 2 : 1;
	auto newdata = alloc.allocate(newcap_num);
	//copy the elements to new address
	string *src = elements;
	string *dst = newdata;
	for (size_t i = 0; i != size(); ++i)
		alloc.construct(dst++, std::move(*src++));
	free(); //release the old memory
	//更新数据结果
	elements = newdata;
	first_free = dst;
	cap = elements + newcap_num;
}


int main(int argc, char** argv)
{
	//testing code
	vector<string> strVec(10, string("jiaen"));
	for(auto iter : strVec)
		std::cout << iter << std::endl;
	std::cout << strVec.size() << std::endl;
	std::cout << strVec.capacity() << std::endl;
	
	

	return 0;
}

