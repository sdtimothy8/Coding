#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

//void print_container()
void print_vector(const vector<int>& ivec)
{
	for (auto iter : ivec)
		cout << iter << " ";
	cout << endl;
}

typedef vector<int>::iterator vecIter;

vecIter myunique(vector<int>& ivec)
{
	if (ivec.empty())
		return ivec.end();

	vecIter retit = ivec.begin();
	vecIter posit = ivec.begin();
	while (++posit != ivec.end()) {
			if (*posit != *retit)
				*(++retit) = *posit;
	}
	return ++retit;
}

int main() {
	vector<int> ivec{1, 1};
	int sval = 22;
	auto ret = myunique(ivec);
	ivec.erase(ret, ivec.end());
	print_vector(ivec);
	return 0;
}
