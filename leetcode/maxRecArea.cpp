/*
 * @lc app=leetcode.cn id=84 lang=cpp
 *
 * [84] 柱状图中最大的矩形
 */

// @lc code=start
#include <stack>
#include <vector>
#include <iostream>

using std::vector;

// 暴力解法：枚举矩形的高
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int maxArea = 0;
        int mid = 0;
        for (; mid != heights.size(); ++mid) {
            int left = mid;
            int right = mid;
            //注意边界情况
            while (left - 1 >= 0 && heights[left-1] >= heights[mid])
                --left;
            while (right + 1 < heights.size() && heights[right+1] >= heights[mid])
                ++right;
            
            maxArea = std::max(maxArea, heights[mid]*(right - left + 1));
        }
        return maxArea;
    }
};

int main(int argc, char** argv) {
    vector<int> iVec = {2, 1, 5, 6, 2, 3};
    Solution s;
    std::cout << "Max Area is: " << s.largestRectangleArea(iVec) << std::endl;

    return 0;
}
// @lc code=end

