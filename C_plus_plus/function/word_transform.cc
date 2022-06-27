#include <map>
#include <unordered_map>
#include <set>
#include <string>
#include <iostream>
#include <sstream>
#include <fstream>
#include <exception>
#include <stdexcept>

using std::map;
using std::unordered_map;
using std::set;
using std::string;
using std::cout;
using std::istringstream;
using std::ifstream;

void build_map(ifstream& map_file, map<string, string>& rule_map)
{
	string key;
	string value;
	while (map_file >> key && std::getline(map_file, value)) {
		if (value.size() > 1)
			//rule_map[key] = value.substr(1);
			rule_map.insert({key, value.substr(1)});
		else
			throw std::runtime_error("no rules for " + key);
	}
}

const string& transform(const string& s, const map<string, string>& rule_map)
{
	auto iter = rule_map.find(s);
	//if ((auto iter = rule_map.find(s)) != rule_map.end())
	if (iter != rule_map.end())
		return iter->second;
	else
		return s;
}

void word_transform(ifstream& map_file, ifstream& input)
{
	map<string, string> rule_map;
	build_map(map_file, rule_map);
	string text;
	while (std::getline(input, text)) {
		std::istringstream stream(text);
		string word;
		bool firstword = true;
		while (stream >> word) {
			if (firstword)
				firstword = false;
			else
				cout << " ";
			cout << transform(word, rule_map);
		}
		cout << std::endl;
	}
}

int main() {
	
	ifstream map_file;
	map_file.open("map_file.txt");
	ifstream input_file;
	input_file.open("input.txt");

	word_transform(map_file, input_file);
	map_file.close();
	input_file.close();

	return 0;
}
