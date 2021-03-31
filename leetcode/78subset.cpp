/*
 * @lc app=leetcode.cn id=78 lang=cpp
 *
 * [78] 子集
 */

// @lc code=start
#include <vector>
#include <iostream>

using std::vector;

// 迭代的思路
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result;
        result.push_back(vector<int>());
        for (int i = 0; i < nums.size(); ++i) {
            // 遍历子集
            int n = result.size();
            for (int j = 0; j < n; ++j) {
                result.push_back(result[j]);
                result.back().push_back(nums[i]);
            }
        }
        return result;
    }
};

// 采用回溯的方法
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<int> track;
        backtrack(0, track, nums);
        return result;
    }
    void backtrack(int start, vector<int>& track, vector<int>& nums) {
        result.push_back(track);
        for (int i = start; i < nums.size(); ++i) {
            track.push_back(nums[i]);
            backtrack(start + 1, track, nums);
            track.pop_back();
        }
    }

private:
    vector<vector<int>> result;
};
// @lc code=end

