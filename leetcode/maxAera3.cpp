/*
 * @lc app=leetcode.cn id=11 lang=cpp
 *
 * [11] 盛最多水的容器
 */

// @lc code=start
#include <cstdio>
#include <vector>
#include <algorithm>
using std::vector;

class Solution {
public:
    int maxArea(vector<int>& height) {
        int maxVal = 0;
        // 双指针两边收敛法，使用stl的max函数
        for (int i = 0, j = height.size() - 1; i < j; ) {
            int minHeight = height[i] < height[j]? height[i++]:height[j--];
            maxVal = std::max(minHeight * (j - i + 1), maxVal); // 记得+1，因为前面内移了一位
        }
        return maxVal;
    }
};
// @lc code=end

