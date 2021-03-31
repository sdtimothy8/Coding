/*
 * @lc app=leetcode.cn id=22 lang=cpp
 *
 * [22] 括号生成
 */

// @lc code=start
#include <iostream>
#include <vector>
#include <string>

using std::vector;
using std::string;

class Solution {
public:
    vector<string> generateParenthesis(int n) {
        vector<string> result;
        int left = 0;
        int right = 0;
        string str;
        _generate(left, right, n, str, result);
        return result;
    }

    void _generate(int left, int right, int n, string str, vector<string>& result) {
        //终止条件
        if (left == n && right == n) {
            result.push_back(str);
            return;
        }
        string str1 = str + "(";
        string str2 = str + ")";
        if (left < n) _generate(left + 1, right, n, str1, result);
        if (left > right) _generate(left, right + 1, n, str2, result);
    }
};
// @lc code=end

