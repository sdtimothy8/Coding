#include <cstdio>
#include <iostream>
#include <fstream>
#include <map>
#include <set>
#include <string>
#include <cctype>

using std::map;
using std::set;
using std::string;
using std::ifstream;
using std::ofstream;

typedef map<string, string> StrStrMap;

const string& transform(const string& word, const StrStrMap& ruleMap) {
    auto iter = ruleMap.find(word);
    if (iter != ruleMap.end())
        return iter->second;
    else
        return word;
}

void buildMap (ifstream& rules, StrStrMap& ruleMap) {
    string keyStr, valueStr;
    string line;
    while (getline(rules, line)) {
        // 构造rules规则map
        string::size_type pos = line.find_first_of(" ", 0);
        if (pos != string::npos) {
            keyStr = line.substr(0, pos);
            valueStr = line.substr(pos + 1);
            ruleMap.insert({keyStr, valueStr});
        }
    }
}

int main (int argc, char** argv) {
    // input: rules, origFile
    // output: resultFile
    map<string, string> ruleMap;
    ifstream rules;
    rules.open("D:\\coding\\Coding\\C_plus_plus\\rules.txt");
    // 建立规则map
    buildMap(rules, ruleMap);

    // 进行真正的单词转换
    ifstream inputFile("D:\\coding\\Coding\\C_plus_plus\\input.txt");
    string inputStr;
    bool isFirstWord = true;
    while (inputFile >> inputStr) {
        if (isFirstWord)
            isFirstWord = false;
        else
            std::cout << " ";
        
        std::cout << transform(inputStr, ruleMap);
    }
    std::cout << std::endl;
    return 0;
}