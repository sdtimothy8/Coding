#include <vector>
#include <iostream>

using namespace std;

typedef vector<int>::const_iterator vecIt;


vecIt binary_search(const vector<int>& ivec, int sval)
{
	auto beg = ivec.begin();
	auto end = ivec.end();
	auto mid = beg + (end - beg) / 2;
	while (mid != end) {
		if (*mid == sval)
			return mid;
		else if (*mid > sval)
			end = mid;
		else
			beg = mid + 1;

		mid = beg + (end - beg) / 2;
	}
	return ivec.end();
}

int main(int argc, char** argv)
{
	vector<int> ivec{1, 2, 4, 6, 18, 23, 34, 45, 56, 77, 88};
	int sval = 1;
	auto ret =  binary_search(ivec, sval);
	if (ret != ivec.end())
		cout << "Find value: " << sval << " .It's pos is: " << ret - ivec.begin() << endl;
	else
		cout << "Not find value: " << sval << endl;

	return 0;
}
