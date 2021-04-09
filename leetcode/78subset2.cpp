/*
 * @lc app=leetcode.cn id=78 lang=cpp
 *
 * [78] 子集
 */

// @lc code=start
#include <vector>
#include <iostream>

using std::vector;

// 回溯法思路
// 回溯法的基本模板
result = []
def backtrack(路径，选择列表):
    if 满足条件：
        result.add(路径)
        return
    for 选择 in 选择列表：
        做选择
        backtrack(路径，选择列表)
        撤销选择


// 思路1：回溯法
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
            backtrack(i + 1, track, nums);
            track.pop_back(nums[i]);
        }
    }
private:
    vector<vector<int>> result;
};

// 思路2：迭代法
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result;
        result.push_back(vector<int>());
        if (nums.empty())
            return result;

        vector<int> track;
        for (int i = 0; i < nums.size(); ++i) {
            int n = result.size();
            for (int j = 0; j < result.size(); ++j) {
                result.push_back(result[j]);
                result.back().push_back(nums[i]);
            }
        }
        return result;
    }
};
// @lc code=end

