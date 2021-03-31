/*
 * @lc app=leetcode.cn id=98 lang=cpp
 *
 * [98] 验证二叉搜索树
 */

// @lc code=start
#include <iostream>
#include <vector>
#include <climits>

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

// 思路：利用BST tree的性质来实现
// 
class Solution {
public:
    bool isValidBST(TreeNode* root) {
        if (root == nullptr)
            return true;
        return _valid(root, NULL, NULL);
    }

    bool _valid(TreeNode* node, TreeNode* minNode, TreeNode* maxNode) {
        // terminator
        if (node == nullptr)
            return true;
        
        // process the logic of this level
        if ((minNode && node->val <= minNode->val) || 
            (maxNode && node->val >= maxNode->val))
            return false;
        else
        {
            return _valid(node->left, minNode, node) && _valid(node->right, node, maxNode);
        }
    }
};
// @lc code=end

