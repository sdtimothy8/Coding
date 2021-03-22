/*
 * @lc app=leetcode.cn id=11 lang=cpp
 *
 * [11] 盛最多水的容器
 */

// @lc code=start
#include <cstdio>
#include <vector>
using std::vector;

class Solution {
public:
    int maxArea(vector<int>& height) {
        int maxVal = 0;
        // 双指针两边收敛法
        for (int i = 0, j = height.size() - 1; i < j; ) {
            int minHeight = height[i] < height[j]? height[i++]:height[j--];
            int area = minHeight * (j - i + 1); // 记得+1，因为前面内移了一位
            if (area > maxVal) maxVal = area;
        }
        return maxVal;
    }
};
// @lc code=end

