/*
 * @lc app=leetcode.cn id=84 lang=cpp
 *
 * [84] 柱状图中最大的矩形
 */

// @lc code=start
#include <stack>
#include <vector>
#include <iostream>
#include <algorithm>

using std::vector;
using std::stack;

// 使用单调栈的方法，不用左右边界数组
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int maxArea = 0;
        stack<int> stk;
        // treak: 通过在高度数组的最后添加0，保证最后所有的高度都能出栈。
        // 缺点：改变了输入参数的内容和结构
        heights.push_back(0);
        for (int i = 0; i < heights.size(); ++i) {
            while (!stk.empty() && heights[stk.top()] >= heights[i]) {
                int h = heights[stk.top()];
                stk.pop();
                if (stk.empty())
                    maxArea = std::max(maxArea, h * i);
                else
                {
                    maxArea = std::max(maxArea, h * (i - stk.top() - 1));
                }
            }
            stk.push(i);
        }
        return maxArea;
    }
};

int main(int argc, char** argv) {
    vector<int> iVec = {2, 4};
    Solution s;
    std::cout << "Max Area is: " << s.largestRectangleArea(iVec) << std::endl;

    return 0;
}
// @lc code=end

