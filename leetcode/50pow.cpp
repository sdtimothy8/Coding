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
        long long N = n;
        if (n < 0) {
            x = 1.0 / x;
            N = N * -1;
        }
        return fastPow(x, N);
    }

    double fastPow(double x, long long n) {
        if (n == 0) 
            return 1.0;

        double half = fastPow(x, n/2);
        return n % 2 == 0 ? half * half : half * half * x;
    }
};
// @lc code=end

