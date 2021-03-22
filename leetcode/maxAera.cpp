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
        // 枚举方法：罗列出所有可能的情况。
        // 时间复杂度：O(n*2)
        int maxVal = 0;
        for (size_t i = 0; i < height.size() - 1; ++i) {
            for (size_t j = i + 1; j < height.size(); ++j) {
                int maxHeight = (height[i] > height[j])? height[i]:height[j];
                int value = maxHeight * (j - i);
                if (maxVal < value) maxVal = value;
            }
        }
        return maxVal;
    }
};

// Solution1
class Solution1 {
public:
    int maxArea(vector<int>& height) {
        // 枚举法
        int maxValue = 0;
        for (size_t i = 0; i < height.size(); ++i) {
            for (size_t j = i + 1; j < height.size(); +j) {
                int minHeight = height[i] < height[j] ? height[i] : height[j];
                int value = minHeight * (j -i);
                if (value > maxValue)
                    maxValue = value;
            }
        }
};

// Solution2
class Solution2 {
public:
    int maxArea(vector<int>& height) {
        // 双指针收敛法
        int maxValue = 0;
        for (int i = 0, j = height.size() - 1; i < j;) {
            int minHeight = height[i] < height[j] ? height[i++] : height[j--];
            int value = minHeight * (j - i + 1); // 记得+1
            if ( value > maxValue) maxValue = value;
        }
        return maxValue;
};
// @lc code=end

