/*
 * @lc app=leetcode.cn id=70 lang=cpp
 *
 * [70] 爬楼梯
 */

// @lc code=start
class Solution {
public:
    int climbStairs(int n) {
        if (n <= 2) return n;
        int first = 1;
        int second = 2;
        int third = 3;
        for (int i = 3; i <= n; ++i) {
            third = first + second;
            first = second;
            second = third;
        }
        return second;
    }
};
// @lc code=end

