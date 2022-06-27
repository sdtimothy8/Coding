#include <map>
#include <set>
#include <string>
#include <cstdio>
#include <iostream>

using std::map;
using std::set;
using std::string;

void world_process(string& world)
{
	for (auto& c : world) {
		c = tolower(c);
		if (ispunct(c))
			c = '\0';
	}
}

int main() {
	set<string> exclude = {"the", "a", "an", "but", "and"};
	auto iter = exclude.begin();
	while (iter != exclude.end()) {
		std::cout << *iter << std::endl;
		*iter = "66";
		++iter;
	}

	return 0;
}
