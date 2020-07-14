#include <iostream>
#include <string>
#include <vector>
#include <memory>

using namespace std;

class StrVec
{
	public:
		StrVec():
			elements(nullptr), first_free(nullptr), cap(nullptr){}
		StrVec(const StrVec&);
		StrVec& operator=(const StrVec& rhs);
		~StrVec(){ free(); }

		void push_back(const string &str);
		size_t size() {return first_free - elements;}
		size_t capacity() {return cap - elements;}
		string* begin() const {return elements;}
		string* end() const {return first_free;}

	private:
		static std::allocator<string> alloc;	//分配元素
		void chk_n_alloc() {if(size() == capacity()) reallocate(); }
		//分配足够的内存来保存给定范围的元素
		pair<string*, string*> alloc_n_copy
			(const string*, const string*);
		void free();
		void reallocate();
		string *elements;	//指向数组首元素指针
		string *first_free;	//指向数组第一个空闲元素的指针
		string *cap;		//指向数组尾后位置的指针
};

// 初始化静态成员alloc
//std::allocator<string> StrVec::alloc = allocator<string>();

void StrVec::reallocate()
{
	//确定新申请空间的大小
	auto newcapacity = size()? 2 * size() : 1;
	//申请新的内存空间
	auto newdata = StrVec::alloc.allocate(newcapacity);
	auto dest = newdata;
	auto elem = elements;
	// 使用移动构造函数拷贝原有的数据到新的内存
	for(auto i = 0; i < size(); ++i)
		alloc.construct(dest++, std::move(*elem++));

	free(); //释放原有的内存
	//给指针成员赋值
	elements = newdata;
	first_free = dest;
	cap = elements + newcapacity;
}

void StrVec::push_back(const string &str)
{
	chk_n_alloc();
	alloc.construct(first_free++, str);
}

void StrVec::free()
{
	if (elements)
	{
		for (auto p = first_free; p != elements;)
			alloc.destroy(--p);
		alloc.deallocate(elements, cap - elements);
	}
}

pair<string*, string*>
StrVec::alloc_n_copy(const string *b, const string *e)
{
	auto data = alloc.allocate(e - b);
	//return make_pair(data, uninitialized_copy(b, e, data));
	//C++11新标准中的列表初始化
	return {data, uninitialized_copy(b,e,data)};
}

StrVec::StrVec(const StrVec &str):
	elements(nullptr), first_free(nullptr), cap(nullptr)
{
	//基于str的指针构造一个新的内存
	auto newdata = alloc_n_copy(str.begin(), str.end());
	elements = newdata.first;
	first_free = cap = newdata.second;
}

StrVec &StrVec::operator=(const StrVec &rhs)
{
	auto newdata = alloc_n_copy(rhs.begin(), rhs.end());
	free();
	elements = newdata.first;
	first_free = cap = newdata.second;

	return *this;
}

int main(int argc, char **argv)
{
	return 0;
}
