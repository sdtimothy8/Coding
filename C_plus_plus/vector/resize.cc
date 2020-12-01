#include <vector>
#include <cstdio>
#include <iostream>

using std::string;
using std::vector;

void printVecInfo(const vector<int>& ivec)
{
	//output the size and capacity
	std::cout << "size() is: " << ivec.size() << std::endl;
	std::cout << "capacity() is: " << ivec.capacity() << std::endl;

	//Print the values in vector
	for ( auto iter = ivec.begin(); iter != ivec.end(); ++iter)
		std::cout << *iter << std::endl;	
}

int main()
{
	//Initialize the vector value
	vector<int> iVec;	
	for (int i = 0; i < 10; ++i)
		iVec.push_back(i);	
		//iVec[i] = i;  //Error!!
	printVecInfo(iVec);

	// reisze the iVec to 8
	iVec.resize(5, 88);
	printVecInfo(iVec);
	// reisze the iVec to 12
	iVec.resize(0);
	printVecInfo(iVec);

	return 0;
}
