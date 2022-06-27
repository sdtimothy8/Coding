#include <iostream>
#include <vector>
#include <string>
#include <memory>
#include <exception>
#include <stdexcept>

using std::vector;
using std::string;
using std::shared_ptr;

class StrBlob {
	public:
		typedef vector<string>::size_type size_type;

		StrBlob(): data(std::make_shared<vector<string>>()) {}
		bool empty() { return data->empty(); }
		size_type size() const { return data->size(); }

		//添加和删除元素
		void push_back(const string &t) { data->push_back(t); }
		string pop_back();

		//元素访问
		string& back();
		string& front();


	private:
		shared_ptr<vector<string>> data;
		void check(size_type i, const string& msg);
};

void StrBlob::check(size_type i, const string& msg)
{
	if (i >= data->size())
		throw std::out_of_range(msg);
}

string& StrBlob::back()
{
	check(0, "back on empty StrBlob");
	return data->back();
}

string& StrBlob::front()
{
	check(0, "front on empty StrBlob");
	return data->front();
}

void StrBlob::pop_back()
{
	check(0, "pop back on empty StrBlob");
	data->pop_back();
}

int main(int argc, char** argv)
{
	return 0;
}
