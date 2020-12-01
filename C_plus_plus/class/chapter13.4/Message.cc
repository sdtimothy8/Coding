#include <cstdio>
#include <string>
#include <iostream>
#include <set>

using std::set;
using std::string;

class Folder;

class Message
{
friend class Folder;
public:
	Message(const string& str = string()):
	text(str) {}
	Message(const Message& copy);
	~Message();
	Message& operator=(const Message& rhs);
	// save message into folder
	void save(Folder* fd);
	// remove message from folder
	void remove(Folder* fd);
private:
	//Private tool function
	
	string 				text;
    std::set<Folder*>	folders;  
};

void Message::save(Folder* fd)
{
	folders.insert(fd);
	fd->addMsg(this);
}

void Message::remove(Folder* fd)
{
	folders.erase(fd);
	fd->removeMsg(this);
}

int main(int argc, char** argv)
{

	return 0;
}
