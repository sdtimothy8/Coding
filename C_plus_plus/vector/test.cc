#include <string>
#include <deque>
#include <vector>
#include <list>
#include <forward_list>
#include <iostream>

using namespace std;

int main( int argc, char** argv )
{
	list<string> authors = {"ligm","huimin","jiale"};
	vector<const char*> articles = { "a", "an", "the" };
	list<string> list2(authors);
	//vector<string> words(articles); // ERROR
	forward_list<string> words( articles.begin(), articles.end() );
	//
	vector<int> ivec(10, -1);
	list<string> svec( 10, "test" );
	forward_list<int> ivec2(10);
	deque<string> svec2(10);

	//
	list<string> names;
	vector<const char*> oldstyles;
	//names = oldstyles;
	names.assign(oldstyles.begin(), oldstyles.end());

	//
	vector<string> svec11(10);
	vector<string> svec22(20);
	swap(svec11, svec22);
	svec11.swap(svec22);
	cout << "svec11's size is:" << svec11.size() << endl;
	
	//insert 
	vector<string> sv = {"I", "love", "god", "forever"};
	list<string> slist;
	slist.insert(slist.begin(), sv.end() - 2, sv.end());

	string word;
	list<string>::iterator it = slist.begin();
	//while(cin >> word)
	//	it = slist.insert(it, word);

	for(it = slist.begin(); it != slist.end(); ++it)
		cout << *it << endl;

	//vector out of range
	vector<int> ivec1;
	//cout << ivec1[0];  // Error!
	//cout << ivec1.at(0); // Error!

	/////erase()
	list<int> ilist = {1, 2, 3, 4, 5, 6, 7, 8, 9, 0};
	list<int>::iterator iter = ilist.begin();
	while(iter != ilist.end())
	{
		if (*iter % 2)
			iter = ilist.erase(iter);
		else
			++iter;
	}

	for( iter = ilist.begin(); iter != ilist.end(); ++iter)
		cout << *iter << endl;

	/////resize()
	list<int> ilist11(10, 8);
	ilist11.resize(12, -1);
	for (iter = ilist11.begin(); iter != ilist11.end(); ++iter)
		cout << *iter << endl;

	/////capacity() and size()
	vector<int> ivec22;
	cout << "ivec22's size：" << ivec22.size() << endl;
	cout << "ivec22's capacity：" << ivec22.capacity() << endl;
	
	ivec22.assign(20, 10);
	cout << "ivec22's size：" << ivec22.size() << endl;
	cout << "ivec22's capacity：" << ivec22.capacity() << endl;

	ivec22.reserve(50);
	cout << "ivec22's size：" << ivec22.size() << endl;
	cout << "ivec22's capacity：" << ivec22.capacity() << endl;

	for (int i = 0; i < 30; ++i)
		ivec22.push_back(i);

	cout << "ivec22's size：" << ivec22.size() << endl;
	cout << "ivec22's capacity：" << ivec22.capacity() << endl;

	ivec22.push_back(100);
	cout << "ivec22's size：" << ivec22.size() << endl;
	cout << "ivec22's capacity：" << ivec22.capacity() << endl;

	ivec22.shrink_to_fit();
	cout << "ivec22's size：" << ivec22.size() << endl;
	cout << "ivec22's capacity：" << ivec22.capacity() << endl;

	///// reverse_interator
	vector<int> ivec33 = {1, 2, 3, 4, 5, 6};
	cout << "ivec33's reverse contents:" << endl;
	auto iter33 = ivec33.rbegin();
	for (; iter33 != ivec33.rend(); ++iter33)
		cout << *iter33 << endl;
	return 0;
}
