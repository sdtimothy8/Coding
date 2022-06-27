#include <map>
#include <unordered_map>
#include <set>
#include <string>
#include <cstdio>
#include <iostream>

using std::map;
using std::unordered_map;
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
	unordered_map<string, size_t> word_count;
	set<string> exclude = {"the", "a", "an", "but", "and"};
	string world;
	while (std::cin >> world) {
		//world_process(world);
		if (exclude.find(world) == exclude.end())
			++word_count[world];
	}

	for (const auto& w : word_count)
		std::cout << w.first << " occurs: " << w.second << ((w.second > 1)? " times" : " time")
			       << std::endl;

	return 0;
}
