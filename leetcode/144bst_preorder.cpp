/*
 * @lc app=leetcode.cn id=144 lang=cpp
 *
 * [144] 二叉树的前序遍历
 */

// 使用递归的思路
// @lc code=start
#include <iostream>
#include <vector>

using std::vector;
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
        preorder(root, result);
        return result;
    }
    void preorder(TreeNode* root, vector<int>& result) {
        if (root == nullptr)
            return;
        result.push_back(root->val);
        preorder(root->left, result);
        preorder(root->right, result);
    }
};
// @lc code=end

