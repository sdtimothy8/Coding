#include <iostream>
#include <algorithm>
#include <list>
#include <iterator>

using namespace std;

//void print_container()
void print_list(const list<int>& ilist)
{
	for (const auto &iter : ilist)
		cout << iter << " ";
	cout << endl;
}

int main() {
	list<int> lst = {1, 2, 3, 4};
	list<int> lst1, lst2;

	//Use front_inserter
	copy(lst.cbegin(), lst.cend(), front_inserter(lst1));
	print_list(lst1);

	// Use inserter
	copy(lst.cbegin(), lst.cend(), inserter(lst2, lst2.begin()));
	print_list(lst2);
	return 0;
}
