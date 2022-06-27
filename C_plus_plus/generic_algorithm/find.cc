#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

int main() {
	vector<int> ivec{1, 8, 14, 9, 45, 22, 7, 33};
	int sval = 22;
	auto ret = find(ivec.cbegin(), ivec.cend(), sval );
	cout << "The value: " << sval << (ret == ivec.cend()? " is not present." :
		" is present.") << endl;
	return 0;
}
