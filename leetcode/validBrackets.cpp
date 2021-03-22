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
        std::stack<char> st;
        for (size_t i = 0; i < s.size(); ++i) {
            if (st.empty())
                st.push(s[i]);
            else
            {
                // 括号可以匹配，从栈中移除相应的括号
                if (isMatched(st.top(), s[i])) {
                    st.pop();
                }
                else 
                {
                    st.push(s[i]);
                }
            }
        }
        if (st.empty())
            return true;
        else
            return false;
    }

    bool isMatched(const char& ch1, const char& ch2) {
        if ((ch1 == '(' && ch2 == ')') ||
            (ch1 == '{' && ch2 == '}') ||
            (ch1 == '[' && ch2 == ']'))
            return true;
        else
            return false;
    }
};
// @lc code=end

