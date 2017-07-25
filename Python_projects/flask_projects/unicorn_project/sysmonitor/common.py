# -*- coding: utf-8 -*-
"""common func."""

import os
__author__ = 'yuxiubj@inspur.com'
COMMON_NONE = 'comand is None!'
COMMON_EXCEPT = "except in command_exec, command= "


class Common():

    """
    some common function
    """

    @classmethod
    def command_exec(cls, command, dict_flag=0, start=0, end=-1, changeKeys=None):
        """
        exec command then return; if dict_flag=0 return string list,if dict_flag=1 return dict list.
        when dict_flag=1, change string list from start to end.
        you can change the dict_key through diction changeKeys like {o:"time",2:"dev"}
        :param command:
        :param dict_flag:
        :param start:
        :param end:
        :param changeKeys:
        :return:
        """
        if command.strip() is None:
            return False, COMMON_NONE
        try:
            command_result = cls.list_result_command(command)
            if 0 == dict_flag:
                return True, command_result
            command_dict_list = cls.trans_list_to_dict(command_result, start, end, changeKeys)
        except:
            return False, COMMON_EXCEPT + command
        return True, command_dict_list

    @classmethod
    def list_result_command(cls, command):
        """
         get list of commond , removed empty line
        """
        result_list = []
        list_com = os.popen(command).readlines()
        for line in list_com:
            if line.strip():
                result_list.append(line.strip())
        return result_list

    @classmethod
    def trans_list_to_dict(cls, r_list, start=0, end=-1, changeKeys=None):
        """
        transform r_list to a list contain some dictionary
        trans from start to end
        satrt line is keys line
        trans all for end=-1
        change first key to changeFistKey except changeFistKey is None
        :param r_list:
        :param start:
        :param end:
        :param changeKeys:
        :return:
        """
        if end == -1:
            list_length = len(r_list)
        else:
            list_length = end

        list_keys = r_list[start].strip().split()
        if changeKeys is not None:
            for k, v in changeKeys.items():
                list_keys[k] = v

        key_length = len(list_keys)
        list_dict = []
        if key_length == 0:
            return list_dict
        for i in range(start+1, list_length):
            if len(r_list[i].strip()) == 0:
                continue
            line_i = r_list[i].strip().split()
            line_i_con = {}
            for j in range(0, key_length):
                line_i_con[list_keys[j]] = line_i[j]
            list_dict.append(line_i_con)
        return list_dict

    @classmethod
    def get_dict_by_name(cls, dict_key, dict_name, dict_map):
        """
        get dict form dict_map when dict.dict_key = dict_name
        :param dict_key:
        :param dict_name:
        :param dict_map:
        :return:
        """
        for map in dict_map:
            if map[dict_key] == dict_name:
                return map
        return None

    @classmethod
    def get_index_by_name(cls, dict_key, dict_name, dict_map):
        """
        get index form dict_map when dict.dict_key = dict_name
        :param dict_key:
        :param dict_name:
        :param dict_map:
        :return:
        """
        for i in range(0, len(dict_map)):
            if dict_map[i][dict_key] == dict_name:
                return i
        return -1
