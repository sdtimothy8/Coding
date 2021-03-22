/*
 * @lc app=leetcode.cn id=15 lang=cpp
 *
 * [15] 三数之和
 */

// @lc code=start
#include <vector>
#include <algorithm>
#include <iostream>
using std::vector; 
class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> resVecVec;
        if (nums.size() < 3) return resVecVec;
        //排序+双指针的解法
        // 1）对数组进行排序
        std::sort(nums.begin(), nums.end());
        // 2) 固定最左边的k，对剩余通过i，j双指针移动
        for (int k = 0; k < nums.size() - 2; ++k) {
            if (nums[k] > 0) break;
            //去重
            if (k > 0 && nums[k] == nums[k-1]) continue;
            int i = k+1, j = nums.size() - 1;
            while (i < j) {
                int sum = nums[k] + nums[i] + nums[j];
                if (sum == 0) {
                    resVecVec.push_back(vector<int>({nums[k], nums[i], nums[j]}));
                    ++i;
                    --j;
                    while (i < j && nums[i] == nums[i-1]) ++i;
                    while (i < j && nums[j] == nums[j+1]) --j;
                }
                else if (sum < 0) {
                    ++i;
                    while (i < j && nums[i] == nums[i]) ++i;
                }
                else {
                    --j;
                    while (i < j && nums[j] == nums[j+1]) --j;
                }
            }
        } // for

        return resVecVec;
    }
};

// 优化循环自增自减
class Solution2 {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> resVecVec;
        //排序+双指针的解法
        // 1）对数组进行排序
        std::sort(nums.begin(), nums.end());
        // 2) 固定最左边的k，对剩余通过i，j双指针移动
        for (int k = 0; k < nums.size() - 2; ++k) {
            if (nums[k] > 0) break;
            //去重
            if (k > 0 && nums[k] == nums[k-1]) continue;
            int i = k+1, j = nums.size() - 1;
            while (i < j) {
                int sum = nums[k] + nums[i] + nums[j];
                if (sum == 0) {
                    resVecVec.push_back(vector<int>({nums[k], nums[i], nums[j]}));
                    while (i < j && nums[i] == nums[++i]) ;
                    while (i < j && nums[j] == nums[--j]) ;
                }
                else if (sum < 0) {
                    while (i < j && nums[i] == nums[++i]) ;
                }
                else {
                    while (i < j && nums[j] == nums[--j]) ;
                }
            }
        } // for

        return resVecVec;
    }
};
void printIntVecVec(const vector<vector<int>>& resVec) {
    if (resVec.empty()) {
        std::cout << "[ ]" << std::endl;
        return;
    }

    std::cout << "[";
    for (auto iter1 = resVec.begin(); iter1 != resVec.end(); ++iter1) {
        std::cout << "[";
        for (auto iter2 = (*iter1).begin(); iter2 != (*iter1).end(); ++iter2) {
            std::cout << *iter2;
        }
        std::cout << "]";
    }
    std::cout << "]" << std::endl;
}

int main (int argc, char** argv) {
    Solution obj;
    vector<int> iVec = {-1,0,1,2,-1,-4};
    vector<vector<int>> resVecVec = obj.threeSum(iVec);
    printIntVecVec(resVecVec);
    return 0;
}
// @lc code=end

