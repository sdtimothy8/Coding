/*
 * @lc app=leetcode.cn id=145 lang=cpp
 *
 * [145] 二叉树的后序遍历
 */

// @lc code=start

// 使用迭代的思路求解
// @lc code=start
#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>

using std::vector;
using std::stack;

//Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

class Solution {
public:
    vector<int> postorderTraversal(TreeNode* root) {
        vector<int> result;
        TreeNode* current = root;
        stack<TreeNode*> stk; 
        while (!stk.empty() || current != nullptr) {
            if (current != nullptr) {
                result.push_back(current->val);
                stk.push(current);
                current = current->right;
            }
            else
            {
                TreeNode* temp = stk.top();
                current = temp->left;
                stk.pop();
            }
        }
        // 对reuslt中的结果作逆序操作
        std::reverse(result.begin(), result.end());
        return result;
    }
};
// @lc code=end

