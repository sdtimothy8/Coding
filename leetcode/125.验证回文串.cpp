/*
 * @lc app=leetcode.cn id=125 lang=cpp
 *
 * [125] 验证回文串
 */

// @lc code=start
#include <string>
class Solution {
public:
    bool isPalindrome(string s) {
        if (s.empty())
            return true;
        //使用双指针方法比较前后两部分字符是否相等
        for (size_t i = 0, j = s.size() - 1; i < j; ++i, --j) {
            while (!isalnum(s[i]) && i < j) ++i;
            while (!isalnum(s[j]) && i < j) --j;
            if (tolower(s[i]) != tolower(s[j])) return false;
        }
        return true;
    }
};
// @lc code=end

