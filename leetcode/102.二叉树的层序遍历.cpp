/*
 * @lc app=leetcode.cn id=102 lang=cpp
 *
 * [102] 二叉树的层序遍历
 */

// @lc code=start
#include <iostream>
#include <vector>
#include <deque>

using std::vector;
using std::deque;

//Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

// 迭代的思路
class Solution {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> result;
        if (root == nullptr)
            return result;

        deque<TreeNode*> queue;
        queue.push_back(root);
        while (!queue.empty()) {
            int n = queue.size();
            vector<int> tempResult;
            for (int i = 0; i < n; ++i) {
                TreeNode* temp = queue.front();
                tempResult.push_back(temp->val);
                queue.pop_front();
                if (temp->left)
                    queue.push_back(temp->left);
                if (temp->right)
                    queue.push_back(temp->right);
            }
            result.push_back(tempResult);
        }
        return result;
    }
};

// 递归的思路
class Solution2 {
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> result;
        if (root == nullptr)
            return result;
        // 从根节点，level0层开始执行
        _levelorder(0, root, result);
        return result;
    }

    void _levelorder(int level, TreeNode* node, vector<vector<int>>& result) {
        // 终止条件
        if (node == nullptr)
            return;

        // 每层处理逻辑
        if (level == result.size()) {
            result.resize(level + 1);
            // 思路2
            //result.push_back(vector<int>());
        }
        result[level].push_back(node->val);

        // 左右子树处理
        _levelorder(level+1, node->left, result);
        _levelorder(level+1, node->right, result);
    }
};
// @lc code=end

