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

class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> track;
        backtrack(0, nums, track, result);
        return result;
    }
    
    void backtrack(int start, vector<int>& nums, vector<vector<int>>& result) {
        result.push_back()
    }
};
// @lc code=end

