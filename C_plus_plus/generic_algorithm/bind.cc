#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <functional>

using namespace std;
using namespace std::placeholders;

void print_svector(const vector<string>& ivec)
{
	for (const auto &iter : ivec) //避免对象拷贝
		cout << iter << " ";
	cout << endl;
}

bool isShorter(const string& s1, const string& s2)
{
	return s1.size() < s2.size();
}

bool check_size(const string& s, string::size_type sz)
{
	return s.size() >= sz;
}

void elimDups(vector<string>& svec)
{
	sort(svec.begin(), svec.end());
	auto uni_end = unique(svec.begin(), svec.end());
	svec.erase(uni_end, svec.end());
}

void biggies(vector<string>& words, vector<string>::size_type sz)
{
	elimDups(words);
	stable_sort(words.begin(), words.end(), isShorter);
	//auto ret = find_if(words.begin(), words.end(), [sz](const string& s){ return s.size() >= sz; });
	auto ret = find_if(words.begin(), words.end(), bind(check_size, _1, sz));
	auto count = words.end() - ret;
	for_each(ret, words.end(), [](const string& s){cout << s << " ";});
	cout << endl;
}

int main() {
	vector<string> svec{"the", "quick", "red", "fox", "jump", "over", "the", "slow", "red", "turtle"};
	elimDups(svec);
	print_svector(svec);
	stable_sort(svec.begin(), svec.end(), isShorter);
	print_svector(svec);

	biggies(svec, 5);

	// 使用bind函数
	auto check6 = bind(check_size, _1, 6);
	string s = "hello";
	check6(s);

	return 0;
}
