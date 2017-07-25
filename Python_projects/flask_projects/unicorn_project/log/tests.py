"""
tests for module log
"""
import os
import service
from mock import patch, Mock, mock_open, MagicMock
from django.test import TestCase
from django.core.files.base import File

__author__ = 'yuxiubj@inspur.com'


class LogTest(TestCase):

    # test readList
    @patch('log.service.get_log_list')
    def test_readloglist(self, mock_service):
        mock_service.return_value = {"path": "/var/log/",
                                     "fts": [{"f_time": "2015-06-16 08:48:26",
                                              "is_dir": False,
                                              "f_size": "2.2 MB",
                                              "name": "djang-rest-framework.zip"}]}
        response = self.client.get("/logs/?path=../test/")
        self.assertFalse(mock_service.called)
        self.assertEqual(response.status_code, 500)

        response = self.client.get("/logs/")
        self.assertTrue(mock_service.called)
        self.assertEqual(response.status_code, 200)

    # test file upload
    @patch("os.path.exists")
    @patch('log.service.check_file_size')
    @patch('log.service.upload_file')
    def test_uploadfile(self, mock_upload, mock_check, mock_path):
        with open("abce", 'w') as f0:
            f0.write("write file!!!")
        with open("abce") as f1:
            response = self.client.post("/logs/?path=../test/", data={"fileName": "temp_upload.log", "file": f1})
            self.assertFalse(mock_upload.called)
            self.assertEqual(response.status_code, 500)

            mock_check.return_value = False
            response = self.client.post("/logs/", data={"fileName": "temp_upload.log", "file": f1})
            self.assertFalse(mock_upload.called)
            self.assertEqual(response.status_code, 500)

            mock_check.return_value = True
            mock_path.return_value = True
            response = self.client.post("/logs/", data={"fileName": "temp_upload.log", "file": f1})
            self.assertFalse(mock_upload.called)
            self.assertEqual(response.status_code, 500)

            mock_path.return_value = False
            mock_upload.return_value = "upload success"
            response = self.client.post("/logs/", data={"fileName": "temp_upload.log", "file": f1})
            self.assertTrue(mock_upload.called)
            self.assertEqual(response.status_code, 200)

    # test download File
    @patch('log.service.view_log_detail')
    @patch("os.path.isdir")
    def test_downloadfile(self, mock_path, mock_service):
        response = self.client.get("/logs/anyFile.log/?path=../test/")
        self.assertEqual(response.status_code, 500)

        mock_path.return_value = True
        mock_service.return_value = "abcd"
        response = self.client.get("/logs/anyFile.log/")
        self.assertFalse(mock_service.called)
        self.assertEqual(response.status_code, 500)

        mock_path.return_value = False
        mock_service.return_value = "abcd"
        response = self.client.get("/logs/anyFile.log/")
        self.assertTrue(mock_service.called)
        self.assertEqual(response.status_code, 200)


class TestService(TestCase):

    # test upload
    @patch('__builtin__.open')
    def test_upload(self, open_mock):
        data = "abcdefghijklmnopqrstuvwxyz"
        f = Mock(chunks=lambda: data)
        open_mock.return_value = open("abce", 'w')
        service.upload_file(f, 'abce')
        self.assertTrue(open_mock.return_value.write.called)
        self.assertTrue(open_mock.return_value.close.called)

    # test checkSize
    def test_size(self):
        f_file = Mock(size=500000)
        c = service.check_file_size(f_file)
        self.assertEqual(c, True)
        f_file = Mock(size=500000001)
        c = service.check_file_size(f_file)
        self.assertEqual(c, False)

    # test delete
    @patch.object(os, 'remove')
    @patch('os.path')
    def test_delete(self, mock_path, mock_remove):
        mock_path.exists.return_value = False
        service.delete_file("any path")
        self.assertFalse(mock_remove.called)

        mock_path.exists.return_value = True
        service.delete_file("any path")
        self.assertTrue(mock_remove.called)

    @patch('log.service')
    def test_readLogList(self, mock_service):
        cmdurl = "/logs/"
        mock_service.get_log_list.return_value = "ttt"
        response = self.client.get(cmdurl)
        self.assertEqual(response.status_code, 200)

    def test_create_file(self):
        with patch('__builtin__.open', mock_open(), create=True) as m:
            service.create_temp("anyfile")
        m.assert_called_with("anyfile", 'w')
        wm = m()
        wm.write.assert_called_with("write file!!!")

    def test_upload_file(self):
        file_mock = MagicMock(spec=File)
        file_mock.chunks.return_value = "write"
        with patch('__builtin__.open', mock_open(), create=True) as m:
            service.upload_file(file_mock, 'anyfile')
        m.assert_called_with("anyfile", 'w')
        wm = m()
        self.assertTrue(file_mock.chunks.called)
        self.assertTrue(wm.write.called)
        self.assertTrue(wm.close.called)

'''
    def test_readLogList(self):
        cmdurl = "/logs/"
        response = self.client.get(cmdurl)
        self.assertEqual(response.status_code, 200)

    def test_deleteLog(self):
        cmdurl = "/logs/temp_del.log/"
        service.create_temp("/var/log/temp_del.log")
        response = self.client.delete(cmdurl)
        self.assertEqual(response.status_code, 200)

    def test_readLog(self):
        cmdurl = "/logs/temp_read.log/"
        service.create_temp("/var/log/temp_read.log")
        response = self.client.get(cmdurl)
        self.assertEqual(response.status_code, 200)

    def test_uploadLog(self):
        service.create_temp("/home/filetrans/temp_up.log")
        service.delete_file("/var/log//temp_up.log")
        f = open("/home/filetrans/temp_up.log")
        dict4post = {"fileName":  "temp_up.log", "file": f}

        cmdurl = "/logs/"
        response = self.client.post(cmdurl, data=dict4post)
        f.close()
        self.assertEqual(response.status_code, 200)
'''
