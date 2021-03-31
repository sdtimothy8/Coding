/*
 * @lc app=leetcode.cn id=144 lang=cpp
 *
 * [144] 二叉树的前序遍历
 */

// 使用迭代的思路求解
// @lc code=start
#include <iostream>
#include <vector>
#include <stack>

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
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> result;
        stack<TreeNode*> stk;
        if (root != nullptr)
            stk.push(root);
            
        while (!stk.empty()) {
            TreeNode* node = stk.top();
            stk.pop();
            result.push_back(node->val);
            if (node->right)
                stk.push(node->right);
            if (node->left)
                stk.push(node->left);
        }

        return result;
    }
};
// @lc code=end
