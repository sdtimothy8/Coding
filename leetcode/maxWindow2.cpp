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

// 2、单调队列
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    deque<int> windows;
    vector<int> results;
    int right = 0;
    for (int i = 0; i < nums.size(); ++i) {
        // 判断队列的首元素是不是移除了窗口
        if (!windows.empty() && windows.front() == i - k) {
            windows.pop_front();
        }
        while (!windows.empty() && nums[windows.back()] < nums[i]) {
            windows.pop_back();
        }
        windows.push_back(i);
        if (i >= k - 1) results.push_back(nums[windows.front()]);
    }
    return results;
    }
};

int main(int argc, char** argv) {
    //vector<int> iVec = {1, 3, -1, -3, 5, 3, 6, 7};
    vector<int> iVec = {7, 2, 4};
    Solution s;
    vector<int> results = s.maxSlidingWindow(iVec, 2);
    for (auto iter = results.begin(); iter != results.end(); ++iter) {
        std::cout << *iter << ",";
    }
    std::cout << std::endl;
    return 0;
}
// @lc code=end

