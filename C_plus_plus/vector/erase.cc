#include <vector>
#include <iostream>

using namespace std;

int main(int argc, char** argv)
{
	vector<int> ivec = {1, 2, 3, 4, 5, 6, 7, 8, 9, 0};
	vector<int>::iterator iter = ivec.begin();

	while(iter != ivec.end())
	{
		//Copy the odd number 
		if (*iter % 2)
		{
			iter = ivec.insert(iter, *iter);
			iter += 2;
		}
		else // Delete the even number
		{
			iter = ivec.erase(iter);
		}
	}
	//Print the numbers in vector
	for (iter = ivec.begin(); iter != ivec.end(); ++iter)
		cout << *iter << endl;
	
	return 0;
}
