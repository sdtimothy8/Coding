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

int main() {
	vector<string> svec{"the", "quick", "red", "fox", "jump", "over", "the", "slow", "red", "turtle"};
	elimDups(svec);
	print_svector(svec);
	stable_sort(svec.begin(), svec.end(), isShorter);
	print_svector(svec);

	return 0;
}
