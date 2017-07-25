import os


def process_move_rule(tablename, chainname, new_order):
    """
    main function for moving rules
    :param tablename: string
    :param chainname: string
    :param new_order: list of number
    :return: -1--"error" 0--"success" 1--"fail"
    """
    table_all_rules = get_table_rules(tablename)
    chain_rules = find_chain_rules(table_all_rules, chainname)
    adjusted_rules, message, retcode = adjust_order(chain_rules, new_order)
    if retcode != 0:
        return -1
    final_table_rules = combine_table_rules(
                            table_all_rules,
                            adjusted_rules, chainname)
    if not table_restore(final_table_rules):
        return 1
    else:
        return 0


def get_table_rules(tablename):
    """
    get_table_rules
    :param tablename: string
    :return: list of all rules in one table
    """
    retcode = os.popen("iptables-save -t " + tablename)
    rules = []
    for line in retcode:
        rules.append(line)
    return rules


def find_chain_rules(rules, chainname):
    """
    find_chain_rules
    :param rules: string -- all rules in on table
    :param chainname: string
    :return: list of all rules in the table and in the chainname
    """
    index = 0
    rrule = []    # real rules
    findword = "-A " + chainname + " "
    for rule in rules:
        if findword in rule:
            index += 1
            rrule.append({"rule": rule, "index": index})
    return rrule


def adjust_order(rules, order):
    """
    adjust chain rules order
    :param rules: chain rules preadjusted.
    :param order:list like [1,2,3,5,7,4,6]
    :return: new_rules new chain rules adjusted
             message message about adjusting conducted message
             0/-1 about whether adjusting conducted successfully
    """

    if len(rules) != len(order):
        message = "error input for adjust, please refresh web site"
        return (None, message, -1)
    old_order = range(1, len(order)+1)

    new_rules = []
    for index in range(len(order)):
        if order[index] != old_order[index]:
            ret = find_rule_by_index(rules, order[index])
            if ret:
                new_rules.append(ret)
            else:
                message = "error order"
                return (None, message, -1)
        else:
            new_rules.append(rules[index]['rule'])
    message = "success"
    return (new_rules, message, 0)


def find_rule_by_index(rules, index):
    """
    util for adjust_order
    :param rules: chain rules preadjusted
    :param index: the order num to find
    :return: the rule found or None
    """
    for rule in rules:
        if rule["index"] == index:
            return rule['rule']
    return None


def combine_table_rules(table_all_rules, adjusted_rules, chainname):
    """
    combines chain rules into table.
    :param table_all_rules: table rules preadjusted
    :param adjusted_rules: chain rules postadjusted
    :param chainname: iptable chain name
    :return: final_table_rules list of final table rules
    """
    final_table_rules = []
    index = 0
    findword = "-A " + chainname + " "
    for line in table_all_rules:
        if findword in line:
            final_table_rules.append(adjusted_rules[index])
            index += 1
        else:
            final_table_rules.append(line)

    return final_table_rules


def table_restore(final_table_rules):
    """
    final_table_rules is list of all table lines;
    :param final_table_rules: iptables table name,like "filter"
    :return: boolean value for success or not
    """
    final_rules = ''.join(final_table_rules)
    ret = os.system("echo \"" + final_rules + "\"  | iptables-restore")
    return ret == 0
