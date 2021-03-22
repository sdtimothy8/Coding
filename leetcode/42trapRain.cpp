/*
 * @lc app=leetcode.cn id=42 lang=cpp
 *
 * [42] 接雨水
 */

// @lc code=start
#include <iostream>
#include <stack>
#include <vector>

using std::stack;
using std::vector;

// 思路：单调栈的思路
class Solution {
public:
    int trap(vector<int>& height) {
        int res = 0;
        //
        stack<int> stk;
        for (int i = 0; i < height.size(); ++i) {
            while (!stk.empty() && height[i] > height[stk.top()]) {
                int h = height[stk.top()];
                stk.pop();
                if (!stk.empty()) {
                    int index = stk.top();
                    res += (std::min(height[i], height[index]) - h) * (i - index - 1);
                }
            }
            stk.push(i);
        }
        return res;
    }
};

int main (int argc, char** argv) {
    vector<int> iVec = {0,1,0,2,1,0,1,3,2,1,2,1};
    Solution s;
    int result = s.trap(iVec);
    std::cout << "result is: " << result << std::endl;
    return 0;
}
// @lc code=end

