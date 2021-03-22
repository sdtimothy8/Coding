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

// 使用单调栈的方法
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int maxArea = 0;
        stack<int> stk;
        int n = heights.size();
        // 注意：右边界的初始值设置为heights的size。
        // 主要针对默认单调递增的情况。
        vector<int> left(n), right(n, n);

        // 遍历一遍数组，确定每个高度的左右边界
        for (int i = 0; i < n; ++i) {
            while (!stk.empty() && (stk.top() >= 0) && heights[stk.top()] >= heights[i]) {
                right[stk.top()] = i;
                stk.pop();
            }
            left[i] = stk.empty() ? -1 : stk.top();
            stk.push(i); //入栈的是index
        }
        // 通过左右边界计算每个高度对应的面积，并确定最大面积
        for (int i = 0; i < n; ++i) {
            maxArea = std::max(maxArea, heights[i] * (right[i] - left[i] - 1));
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

