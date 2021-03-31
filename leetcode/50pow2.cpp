/*
 * @lc app=leetcode.cn id=50 lang=cpp
 *
 * [50] Pow(x, n)
 */

//
// @lc code=start
#include <iostream>
#include <string>

class Solution {
public:
    double myPow(double x, int n) {
        if (n == 0)
            return 1.0;
        
        long long N = n;
        if (n < 0) {
            x = 1.0 / x;
            N = N * -1;
        }
        double ans = 1.0;
        while (N > 0) {
            if (N % 2 == 1) {
                ans *= x;
            }
            x *= x;
            // 右移一位相当于除以2
            N >>= 1;
        }
        return ans;
    }
};
// @lc code=end

