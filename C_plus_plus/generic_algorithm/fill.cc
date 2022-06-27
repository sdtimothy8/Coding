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

int main() {
	vector<int> ivec{1, 8, 22, 9, 45, 22, 7, 33};
	int sval = 22;
	fill(ivec.begin(), ivec.end(), sval );
	print_vector(ivec);
	return 0;
}
