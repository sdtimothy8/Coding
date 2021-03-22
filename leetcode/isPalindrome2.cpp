/*
 * @lc app=leetcode.cn id=125 lang=cpp
 *
 * [125] 验证回文串
 */

// @lc code=start
#include <string>
#include <iostream>
using std::string;

class Solution {
public:
    bool isPalindrome(string s) {
        if (s.empty()) 
            return true;

        for (size_t i = 0, j = s.size() - 1; i < j; i++, j-- ) {
            while (!isalnum(s[i]) && i < j) ++i;
            while (!isalnum(s[j]) && i < j) --j;
            if (tolower(s[i]) != tolower(s[j]))
                return false;
        } //for
        return true;
    }
};

int main (int argc, char** argv) {
    Solution obj;
    string teststr1 = ".";
    string teststr2 = "a.";
    //std::cout << "teststr1 is huiwen: " << obj.isPalindrome(teststr1) << std::endl;
    std::cout << "teststr2 is huiwen: " << obj.isPalindrome(teststr2) << std::endl;
    // test
    size_t tval = 0;
    int ival = 0;
    std::cout << "--tval is: " << --tval << std::endl;
    std::cout << "--ival is: " << --ival << std::endl;

    return 0;
}

// @lc code=end

