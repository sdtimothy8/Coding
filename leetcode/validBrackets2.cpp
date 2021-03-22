/*
 * @lc app=leetcode.cn id=20 lang=cpp
 *
 * [20] 有效的括号
 */

// @lc code=start
#include <iostream>
#include <string>
#include <stack>

using std::string;

class Solution {
public:
    bool isValid(string s) {
        // 如果字符串个数为奇数个，返回false
        if (s.size() % 2 != 0)
            return false;

        std::stack<char> stk;
        for (const auto& c: s) {
            switch (c) {
                case '(': stk.push(')'); break;
                case '{': stk.push('}'); break;
                case '[': stk.push(']'); break;
                default:
                    if (stk.empty() || c != stk.top())
                        return false;
                    else
                        stk.pop();    
            }
        }
        return stk.empty();
    }
};
// @lc code=end

