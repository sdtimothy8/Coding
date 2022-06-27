#include <string>
#include <memory>
#include <iostream>

using namespace std;

class StrVec {
	public:
		typedef pair<string*, string*> strpair;
		StrVec() : _elements(nullptr), _end(nullptr), _cap(nullptr) { }
		StrVec(const StrVec& s);
		// 移动构造函数
		StrVec(StrVec&& s) noexcept : _elements(s.elements), _end(s._end), _cap(s._cap)
		{ s._elements = s._end = s._cap = nullptr; }
		StrVec& operator=(const StrVec& rhs);
		~StrVec() { free(); }

		// Main interface
		size_t size() { return _end - _elements; }
		size_t capacity() { return _cap - _elements; }
		bool empty() { return _elements == _end; }
		void push_back(const string& s);
		void pop_back();
		string* begin() const { return _elements; }
		string* end() const { return _end; }
		static void initial_alloc();
		

	private:
		/*Tool function*/
		void chk_n_alloc() { if (size() == capacity()) reallocate();}
		void reallocate();
		strpair alloc_n_copy(const string*, const string*);
		void free();

		/*Data member*/
		string* _elements;
		string* _end;
		string* _cap;
		static allocator<string> alloc;
};

void StrVec::initial_alloc()
{
	alloc = allocator<string>();
}

void StrVec::push_back(const string& s)
{
	chk_n_alloc();
	alloc.construct(_end++, s);
}

StrVec::strpair StrVec::alloc_n_copy(const string* b, const string* e)
{
	auto data = alloc.allocate(e - b);
	return {data, uninitialized_copy(b, e, data)};
}

void StrVec::free()
{
	while (_end != _elements)
		alloc.destroy(--_end);
	alloc.deallocate(_elements, capacity());
}

StrVec::StrVec(const StrVec& s)
{
	auto p = alloc_n_copy(s.begin(), s.end());
	_elements = p.first;
	_end = _cap = p.second;
}

StrVec& StrVec::operator=(const StrVec& rhs)
{
	auto p = alloc_n_copy(rhs.begin(), rhs.end());
	free();
	_elements = p.first;
	_end = _cap = p.second;
	return *this;
}

void StrVec::reallocate()
{
	size_t newsize = empty()? 1 : 2*size();
	auto data = alloc.allocate(newsize);
	// copy the olddata to new space
	_end = uninitialized_copy(begin(), end(), data);
	_elements = data;
	_cap = _elements + newsize;
}

int main() {
	StrVec::initial_alloc();

	StrVec svec;
	svec.push_back("love");
	svec.push_back("jiaen");
	svec.push_back("love God");
	string* iter;
	for (iter = svec.begin(); iter != svec.end(); iter++)
		std::cout << *iter << std::endl;
	std::cout << "svec's size is: " << svec.size() << std::endl;
	std::cout << "svec's cap is: " << svec.capacity() << std::endl;
	return 0;
}
