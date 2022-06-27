#include <iostream>
#include <algorithm>
#include <vector>
#include <iterator>

using namespace std;

//void print_container()
void print_vector(const vector<int>& ivec)
{
	for (auto iter : ivec)
		cout << iter << " ";
	cout << endl;
}

int main() {
	vector<int> ivec;
	int sval = 22;
	fill_n(back_iterator(ivec), 8, sval);
	print_vector(ivec);
	return 0;
}
