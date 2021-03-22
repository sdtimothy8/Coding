/*
 * @lc app=leetcode.cn id=239 lang=cpp
 *
 * [239] 滑动窗口最大值
 */

// @lc code=start
#include <iostream>
#include <deque>
#include <vector>
#include <cassert>
#include <algorithm>

using std::vector;
using std::deque;

// 1、暴力解法，时间超时，如何在常数时间内求出窗口元素的最大值
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    // 1) set a window vector, first push k's values.
    // 2) slid window push_back new element and pop_front the head element.
    // 3) eval the max value in the window vector and save value into the output values.
    deque<int> windows;
    vector<int> results;
    int maxVal = 0;
    if (k <= nums.size()) {
        windows.assign(nums.begin(), nums.begin() + k);
        maxVal = *(std::max_element(windows.begin(), windows.end()));
        results.push_back(maxVal);
        for (int i = k; k < nums.size(); k++) {
            windows.push_back(nums[k]);
            windows.pop_front();
            maxVal = *(std::max_element(windows.begin(), windows.end()));
            results.push_back(maxVal);
        }
    }
    return results;
    }
};

int main(int argc, char** argv) {
    vector<int> iVec = {1, 3, -1, -3, 5, 3, 6, 7};
    Solution s;
    vector<int> results = s.maxSlidingWindow(iVec, 3);
    for (auto iter = results.begin(); iter != results.end(); ++iter) {
        std::cout << *iter << ",";
    }
    std::cout << std::endl;
    return 0;
}
// @lc code=end

