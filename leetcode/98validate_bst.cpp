/*
 * @lc app=leetcode.cn id=98 lang=cpp
 *
 * [98] 验证二叉搜索树
 */

// @lc code=start
#include <iostream>
#include <vector>

using std::vector;

// Definition for a binary tree node.
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
    bool isValidBST(TreeNode* root) {
        vector<int> result;
        if (root == nullptr)
            return true;
        return inorder(root, result);
    }
    bool inorder(TreeNode* node, vector<int>& result) {
        bool isValid = true;
        if (node == nullptr)
            return true;
        if (!inorder(node->left, result)) return false;
        // 不符合升序排列的性质，退出
        if (!result.empty() && (node->val <= result.back() )) {
            isValid = false;
            return isValid;
        }
        result.push_back(node->val);
        if (!inorder(node->right, result)) return false;
        return isValid;
    }
};
// @lc code=end

