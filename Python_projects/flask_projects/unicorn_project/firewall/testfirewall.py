from mock import patch, MagicMock
import os
from django.test import TestCase
from rest_framework import status
import firewall.views
import firewall.move


# Create your tests here.
class TestFireWallMove(TestCase):

    @patch.object(firewall.views, 'process_move_rule')
    def test_post(self, process_move_rule_method):
        # case1
        process_move_rule_method.return_value = 0
        request = MagicMock(DATA={'chain': 'fewa', 'table': 'llife', 'newserial': [1, 4, 2, 3]})

        response = firewall.views.FirewallMove().post(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {"status": "success", "message": "move succeed"})
        self.assertTrue(process_move_rule_method.called)

        # case2
        process_move_rule_method.return_value = -1
        process_move_rule_method.called = False
        response = firewall.views.FirewallMove().post(request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {"status": "error",
                                             "message": "move wrong"})
        self.assertTrue(process_move_rule_method.called)

        # case3
        process_move_rule_method.return_value = 3
        process_move_rule_method.called = False
        response = firewall.views.FirewallMove().post(request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {"status": "fail", "message": "move fail"})
        self.assertTrue(process_move_rule_method.called)


class TestStaticFunc(TestCase):

    @patch.object(firewall.move, 'table_restore')
    @patch.object(firewall.move, 'combine_table_rules')
    @patch.object(firewall.move, 'adjust_order')
    @patch.object(firewall.move, 'find_chain_rules')
    @patch.object(firewall.move, 'get_table_rules')
    def test_process_rule_method(self, get_table_rules_method,
                                 find_chain_rules_method,
                                 adjust_order_method,
                                 combine_table_rules_method,
                                 table_restore_method):

        # case1
        params = ['abc', 'bcd', [2, 3, 1]]

        adjust_order_method.return_value = 'abc', None, -1
        retcode = firewall.views.process_move_rule(params[0], params[1], params[2])
        self.assertEquals(retcode, -1)
        self.assertTrue(get_table_rules_method.called)
        self.assertTrue(find_chain_rules_method.called)
        self.assertTrue(adjust_order_method.called)
        self.assertFalse(combine_table_rules_method.called)
        self.assertFalse(table_restore_method.called)

        # case2
        adjust_order_method.return_value = 'abc', None, 0
        table_restore_method.return_value = True
        retcode = firewall.views.process_move_rule(params[0], params[1], params[2])
        self.assertEquals(retcode, 0)
        self.assertTrue(combine_table_rules_method.called)
        self.assertTrue(table_restore_method.called)

        # case3
        table_restore_method.return_value = False
        retcode = firewall.views.process_move_rule(params[0], params[1], params[2])
        self.assertEquals(retcode, 1)

    @patch.object(os, 'popen')
    def test_get_table_rules(self, os_popen_method):

        tfile = open('tmpfirewall3254f.feni', 'w')
        tfile.write('table abc\nchain abc\n1. ABCDEFG\n2. abcdefg\n3. 1234567\n')
        tfile.close()
        os_popen_method.return_value = open('tmpfirewall3254f.feni', 'r')
        retcode = firewall.move.get_table_rules('fewaf')
        self.assertListEqual(retcode, ['table abc\n', 'chain abc\n',
                                       '1. ABCDEFG\n', '2. abcdefg\n', '3. 1234567\n'])

    def test_find_chain_rules(self):
        rules = ['table abc\n',
                 'chain abc\n',
                 '1. -A INPUT ABCDEFG\n',
                 '2. -A INPUT abcdefg\n',
                 '3. -A OUTPUT 1234567\n',
                 '4. -A OUTPUT UVWXYZX']
        chainname = 'INPUT'
        expected_value = [{'index': 1, 'rule': '1. -A INPUT ABCDEFG\n'},
                          {'index': 2, 'rule': '2. -A INPUT abcdefg\n'}]
        retcode = firewall.move.find_chain_rules(rules=rules, chainname=chainname)

        self.assertEquals(retcode, expected_value)

        chainname = 'INPUT_OUTPUT'

        expected_value = []

        retcode = firewall.move.find_chain_rules(rules=rules, chainname=chainname)
        self.assertEquals(retcode, expected_value)

    def test_adjust_order(self):

        # case1
        rules = [{'index': 1, 'rule': '-A INPUT ABCDEFG\n'},
                 {'index': 2, 'rule': '-A INPUT abcdefg\n'},
                 {'index': 3, 'rule': '-A INPUT 1234567\n'},
                 {'index': 4, 'rule': '-A INPUT UVWXYZX\n'}]
        order = [2, 1, 4, 3]
        expect_value = ['-A INPUT abcdefg\n', '-A INPUT ABCDEFG\n', '-A INPUT UVWXYZX\n', '-A INPUT 1234567\n']
        retvalue, message, retcode = firewall.move.adjust_order(rules=rules, order=order)
        self.assertListEqual(retvalue, expect_value)
        self.assertEquals(message, 'success')
        self.assertEquals(retcode, 0)

        # case2
        order = [2, 1, 3, 4, 5]
        retvalue, message, retcode = firewall.move.adjust_order(rules=rules, order=order)
        self.assertIsNone(retvalue)
        self.assertEquals(message, 'error input for adjust, please refresh web site')
        self.assertEquals(retcode, -1)

        # case3
        order = [2, 1, 5, 3]
        retvalue, message, retcode = firewall.move.adjust_order(rules=rules, order=order)
        self.assertIsNone(retvalue)
        self.assertEquals(message, 'error order')
        self.assertEquals(retcode, -1)

    def test_find_rule_by_index(self):

        rules = [{'index': 1, 'rule': '-A INPUT ABCDEFG\n'},
                 {'index': 2, 'rule': '-A INPUT abcdefg\n'},
                 {'index': 3, 'rule': '-A INPUT 1234567\n'},
                 {'index': 4, 'rule': '-A INPUT UVWXYZX\n'}]
        index = [3, 5, -1]
        expect_value = [rules[2]['rule'], None, None]
        for item in range(len(index)):
            retvalue = firewall.move.find_rule_by_index(rules=rules, index=index[item])
            self.assertEquals(retvalue, expect_value[item])

    def test_combine_table_rules(self):

        tables_all_line = ['table filter\n',
                           'chain INPUT\n',
                           '-A OUTPUT feawgnife\n',
                           '-A INPUT ABCDEFG\n',
                           '-A INPUT abcdefg\n',
                           '-A INPUT 1234567\n',
                           '-A INPUT UVWXYZX\n']
        # adjust order [2, 1, 4, 3]
        adjusted_line = ['-A INPUT abcdefg\n',
                         '-A INPUT ABCDEFG\n',
                         '-A INPUT UVWXYZX\n',
                         '-A INPUT 1234567\n']
        chainname = 'INPUT'
        expected_value = ['table filter\n',
                          'chain INPUT\n',
                          '-A OUTPUT feawgnife\n',
                          '-A INPUT abcdefg\n',
                          '-A INPUT ABCDEFG\n',
                          '-A INPUT UVWXYZX\n',
                          '-A INPUT 1234567\n']
        retcode = firewall.move.combine_table_rules(table_all_rules=tables_all_line,
                                                    adjusted_rules=adjusted_line,
                                                    chainname=chainname)
        self.assertEquals(retcode, expected_value)

        # case2
        testcase = [['1', '2', '3'], [4, 5, 6], 'few']
        retcode = firewall.move.combine_table_rules(table_all_rules=testcase[0],
                                                    adjusted_rules=testcase[1],
                                                    chainname=testcase[2])
        expected_value = ['1', '2', '3']
        self.assertEquals(retcode, expected_value)

    @patch.object(os, 'system')
    def test_table_restore(self, os_system_method):
        # case1
        os_system_method.return_value = 0
        self.assertTrue(firewall.move.table_restore(['1', '2', '3']))

        # case2
        os_system_method.return_value = 1
        self.assertFalse(firewall.move.table_restore(['1', '2', '3']))
