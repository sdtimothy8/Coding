/*
 * @lc app=leetcode.cn id=125 lang=cpp
 *
 * [125] 验证回文串
 */

// @lc code=start
#include <string>
#include <algorithm>
#include <cctype>

using std::string;
class Solution {
public:
    bool isPalindrome(string s) {
        string newstr = s;
        transformToLowerCase(newstr);
        filterNonAlphaNum(newstr);
        return newstr == reverseStr(newstr);
    } 
    void transformToLowerCase(string& s) {
        std::transform(s.begin(), s.end(), s.begin(), ::tolower);
    }
    void filterNonAlphaNum(string& s) {
        s.erase(std::remove_if(s.begin(), s.end(), [](char c) {return !isalnum(c);}), s.end());
    }
    string reverseStr(const string& s) {
        return string(s.rbegin(), s.rend());
    }
};