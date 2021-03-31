/*
 * @lc app=leetcode.cn id=144 lang=cpp
 *
 * [144] 二叉树的前序遍历
 */

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
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> result;
        if (root == nullptr) 
            return result;
        // 
        TreeNode* current = root;
        stack<TreeNode*> stk;
        while (!stk.empty() || current != nullptr) {
            if (current != nullptr) {
                result.push_back(current->val);
                stk.push(current);
                current = current->left;
            }
            else 
            {
                TreeNode* temp = stk.top();
                stk.pop();
                if (temp->right)
                    current = temp->right;
            }
        }
        return result;
    }
};

//
class Solution2 {
public:
    vector<int> preorderTraversal(TreeNode* root) {
        vector<int> result;
        if (root == nullptr) 
            return result;
        // 
        stack<TreeNode*> stk;
        stk.push(root);
        while (!stk.empty()) {
            TreeNode* top = stk.top();
            result.push_back(top->val);
            stk.pop();
            if (top->right)
                stk.push(top->right); //右子树先入栈
            if (top->left)
                stk.push(top->left);
        }
        return result;
    }
};
// @lc code=end

