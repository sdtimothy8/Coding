#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

int main() {
	vector<int> ivec{1, 8, 22, 9, 45, 22, 7, 33};
	int sval = 22;
	auto ret = count(ivec.cbegin(), ivec.cend(), sval );
	cout << "The value: " << sval << " appears in ivec " << ret << " time(s)" << endl;
	return 0;
}
