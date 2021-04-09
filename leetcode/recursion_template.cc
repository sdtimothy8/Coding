
void recursion(int level, int param1, int param2) {
    // 终止条件
    if (level > MAX_LEVEL) {
        process_result();
        return;
    }

    // process the  of current level
    process_data(param1, param2);

    // drill down
    recursion(level + 1, param1, param2);

    //reverse state
}