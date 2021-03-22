/*
 * @lc app=leetcode.cn id=15 lang=cpp
 *
 * [15] 三数之和
 */

// @lc code=start
#include <vector>
#include <algorithm>
using std::vector; 
class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> resVecVec;
        //3重循环遍历数组
        for (size_t i = 0; i < nums.size() - 1; ++i)
            for (size_t j = i + 1; j < nums.size(); ++j)
                for (size_t k = j + 1; k < nums.size(); ++k) {
                    if (0 == nums[i] + nums[j] + nums[k]) {
                        vector<int> tmpVec = {nums[i], nums[j], nums[k]};
                        resVecVec.push_back(tmpVec);
                    }
                }
        return resVecVec;
    }
};

class Solution1 {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> resVecVec;
        //双指针法
        // 1) 对数组进行排序
        // 2）固定最左边的值，对右边的剩余数组进行双指针移动
        if (nums.size() < 3) return resVecVec;
        std::sort(nums.begin(), nums.end());
        for (int k = 0; k < nums.size() - 2; ++k) {
            if (nums[k] > 0) break;
            if (k > 0 && nums[k] == nums[k-1]) continue;
            for (int i = k + 1, j = nums.size() - 1; i < j;) {
                int sum = nums[k] + nums[i] + nums[j];
                if (sum == 0) {
                    resVecVec.push_back(vector<int>{nums[k], nums[i], nums[j]});
                    i++;
                    j--;
                    while (nums[i] == nums[i-1] && nums[j] == nums[j+1] && i < j) {
                        i++;
                        j--;
                    }
                }
                else if (sum < 0) {
                    i++;
                    while (nums[i] == nums[i-1] && i < j) {
                        i++;
                    }
                } else //sum > 0
                {
                    j--;
                    while (nums[j] == nums[j+1] && i < j) {
                        j--;
                    }
                }
            }
        }
        return resVecVec;
    }
};
// @lc code=end

