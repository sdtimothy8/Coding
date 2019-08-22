#include <vector>
#include <cstdio>
#include <iostream>

using std::string;
using std::vector;

int main()
{
	//Initialize the vector value
	vector<int> iVec;	
	for (int i = 0; i < 10; ++i)
		iVec.push_back(i);	
		//iVec[i] = i;  //Error!!

	//Print the values in vector
	for (vector<int>::iterator iter = iVec.begin(); iter != iVec.end(); ++iter)
		std::cout << *iter << std::endl;	

	return 0;
}
