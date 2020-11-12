#include <cstdio>
#include <string>
#include <iostream>
#include <set>

using std::set;
using std::string;

class Message
{
	friend class Folder;
public:
private:
	string* 			text;
    std::set<Folder*>	folders;  
};

int main(int argc, char** argv)
{

	return 0;
}
