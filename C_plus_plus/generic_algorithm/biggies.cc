#include <iostream>
#include <algorithm>
#include <vector>
#include <string>

using namespace std;

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
	auto ret = find_if(words.begin(), words.end(), [sz](const string& s){ return s.size() >= sz; });
	auto count = words.end() - ret;
	for_each(ret, words.end(), [](const string& s){cout << s << " ";});
	cout << endl;
}

void biggies2(vector<string>& words, vector<string>::size_type sz, ostream& os = std::cout, char c = ' ')
{
	elimDups(words);
	stable_sort(words.begin(), words.end(), isShorter);
	auto ret = find_if(words.begin(), words.end(), [sz](const string& s){ return s.size() >= sz; });
	auto count = words.end() - ret;
	for_each(ret, words.end(), [](const string& s){cout << s << " ";});
	cout << endl;
	// 默认引用捕获方式，c显式值捕获
	for_each(words.begin(), words.end(), [&, c](const string& s) { os << s << c; });
	cout << endl;

	// 默认值捕获方式，os显式引用捕获
	for_each(words.begin(), words.end(), [=, &os](const string& s) { os << s << c; });
	cout << endl;
}

int main() {
	vector<string> svec{"the", "quick", "red", "fox", "jump", "over", "the", "slow", "red", "turtle"};
	elimDups(svec);
	print_svector(svec);
	stable_sort(svec.begin(), svec.end(), isShorter);
	print_svector(svec);
	//biggies(svec, 4);
	biggies2(svec, 4, cout, '=');

	return 0;
}
