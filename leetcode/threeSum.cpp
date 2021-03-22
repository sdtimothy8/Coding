/*
 * @lc app=leetcode.cn id=15 lang=cpp
 *
 * [15] 三数之和
 */

// @lc code=start
#include <vector>
using std::vector; 
class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> resVecVec;
        //3重循环遍历数组, 这个解法有问题，没有考虑去重
        for (size_t i = 0; i < nums.size() - 2; ++i)
            for (size_t j = i + 1; j < nums.size() - 1; ++j)
                for (size_t k = j + 1; k < nums.size(); ++k) {
                    if (0 == nums[i] + nums[j] + nums[k]) {
                        vector<int> tmpVec = {nums[i], nums[j], nums[k]};
                        resVecVec.push_back(tmpVec);
                    }
                }
        return resVecVec;
    }
};
// @lc code=end

