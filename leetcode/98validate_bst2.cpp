/*
 * @lc app=leetcode.cn id=98 lang=cpp
 *
 * [98] 验证二叉搜索树
 */

// @lc code=start
#include <iostream>
#include <vector>
#include <stack>

using std::vector;
using std::stack;

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
        if (root == nullptr)
            return true;
        vector<int> result;
        stack<TreeNode*> stk;
        bool isValid = true;
        TreeNode* current = root;
        stk.push(root);
        while (!stk.empty()) {
            if (current != nullptr) {
                stk.push(current);
                current = current->left;
            }
            else
            {
                TreeNode* temp = stk.top();
                if (!result.empty() && (temp->val < result.back())) {
                    isValid = false;
                    break;
                }
                result.push_back(temp->val);
                stk.pop();
                current = temp->right;
            }
        }
        return isValid;
    }
};
// @lc code=end

