#include <algorithm>
#include <iostream>
#include <vector>

using namespace std;

bool isShorter(const string &str1, const string &str2)
{
	return str1.size() < str2.size();
}

bool isShorterThanNc(const string &str)
{
	int N = 5;
	return str.size() >= N;
}

void elimDups(vector<string> &words)
{
	// Use lambda expression
	stable_sort(words.begin(), words.end(), [](const string &a, const string &b){return a.size() < b.size();});
	auto end_unique = unique(words.begin(), words.end());
	words.erase(end_unique, words.end());
}

void printWords(const vector<string> &words)
{
	for(auto iter = words.cbegin(); iter != words.cend(); ++iter)
		cout << *iter << endl;
}

void biggies(vector<string> &words, vector<string>::size_type sz)
{
	elimDups(words);
	stable_sort(words.begin(), words.end(), isShorter);
	auto wc = find_if(words.begin(), words.end(), [sz](const string &str){return str.size() >= sz;});
	auto num = words.end() - wc;
	for_each(wc, words.end(), [](const string &str){cout << str << " ";});
	cout << endl;
}

// Main function
int main( int argc, char** argv )
{
	vector<int> intVec = {1,5,3,4,5};
	int val = 5;
	auto result = find(intVec.cbegin(), intVec.cend(), val);
	cout << "The val " << val << (result == intVec.cend()? " is not present" : " is present")
		<< endl;

	// using count alg
	auto result_cnt = count(intVec.cbegin(), intVec.cend(), val);
	cout << "There are " << result_cnt << " times " << val << " in intVec." << endl;

	// accumulate alg
	int sum = accumulate(intVec.cbegin(), intVec.cend(), 0);
	cout << "Sum of intVec is: " << sum << endl;

	// Erase the duplicated words
	vector<string> words{"I", "love", "Godyesu", "I", "love", "Jiale"};
	//auto result_p = partition(words.begin(), words.end(), isShorterThanNc);
	//for (auto iter = words.begin(); iter != result_p; ++iter)
	//	cout << *iter << endl;
	//elimDups(words);
	//printWords(words);
	biggies(words, 5);

	return 0;
}


