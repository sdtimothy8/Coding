#include <cstdio>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <cctype>

using std::map;
using std::set;
using std::string;

string toLowerAndfilterPun(const string& word) {
    string resultStr;
    for (auto ch : word) {
        if (!ispunct(ch))
            resultStr += tolower(ch);
    }
    return resultStr;
}

int main(int argc, char** argv)
{
    map<string, size_t> word_count;
    set<string> exclude = {"a", "an", "the", "and", "but", "or"};
    string word;
    string preProcessedWord;
    while (std::cin >> word) {
        preProcessedWord = toLowerAndfilterPun(word);
        if (!exclude.count(preProcessedWord)) {
            //++word_count[preProcessedWord];
            //使用insert函数来向map中插入元素
            // map's insert 函数返回一个pair，pair的first是一个map的iterator，
            // second 是bool值，true代表插入成功，false代表插入失败
            auto ret = word_count.insert(make_pair(preProcessedWord, 1));
            // word is already in the map, increase word count 
            if (!ret.second) {
                ++ret.first->second;
            }
        }
    }
    // map's erase操作
    string removal_word("love");
    if (word_count.erase(removal_word)) {
        std::cout << "OK: " << removal_word << " removed!" << std::endl;
    }
    else
        std::cout << "Oops: " << removal_word << " not found!" << std::endl;

    // map's find操作
    string searchStr("test");
    if (word_count.find(searchStr) != word_count.end())
        std::cout << searchStr << " is in the word_count map!" << std::endl;
    else
        std::cout << searchStr << " is not in the word_count map!" << std::endl;


    // 使用迭代器来访问map
    for (auto iter = word_count.begin(); iter != word_count.end(); ++iter) {
        std::cout << iter->first << " occurs " << iter->second
                  << ((iter->second > 1)? "times" : "time") << std::endl; 
    }

    // print the word info in the map
    for (const auto& w : word_count) {
        std::cout << w.first << " occurs " << w.second
                  << ((w.second > 1)? "times" : "time") << std::endl; 
    }
    return 0;
}