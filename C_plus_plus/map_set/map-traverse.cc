#include <map>
#include <set>
#include <utility>
#include <string>
#include <cstdio>
#include <iostream>

using std::map;
using std::set;
using std::pair;
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
	map<string, size_t> word_count;
	set<string> exclude = {"the", "a", "an", "but", "and"};
	string world;
	while (std::cin >> world) {
		world_process(world);
		if (exclude.find(world) == exclude.end()) {
			//auto ret = word_count.insert({world, 1});
			auto ret = word_count.insert(map<string, size_t>::value_type(world, 1));
			if (!ret.second)
				++ret.first->second;
		}
	}
	auto map_it = word_count.cbegin();
	while (map_it != word_count.cend()) {
		std::cout << map_it->first << " occurs: " << map_it->second << ((map_it->second > 1)? " times" : " time")
			       << std::endl;
		++map_it;
	}

	return 0;
}
