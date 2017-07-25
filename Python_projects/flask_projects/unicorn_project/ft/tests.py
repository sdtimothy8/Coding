"""
tests for module ft
"""
import mock
import service
from django.test import TestCase
import os
from django.core.files.base import File

__author__ = 'yuxiubj@inspur.com'


class TestViews(TestCase):

    # test readList
    @mock.patch('ft.service.get_ft_list')
    def test_readFtsList(self, mock_service):
        mock_service.return_value = {"path": "/home/filetrans/",
                                     "fts": [{"f_time": "2015-06-16 08:48:26",
                                              "is_dir": False,
                                              "f_size": "2.2 MB",
                                              "name": "djang-rest-framework.zip"}]}

        response = self.client.get("/fts/?path=../test/")
        self.assertFalse(mock_service.called)
        self.assertEqual(response.status_code, 500)

        response = self.client.get("/fts/")
        self.assertTrue(mock_service.called)
        self.assertEqual(response.status_code, 200)

    # test file upload
    @mock.patch("os.path.exists")
    @mock.patch('ft.service.make_path')
    @mock.patch('ft.service.check_filesize')
    @mock.patch('ft.service.upload_file')
    def test_uploadfile(self, mock_upload, mock_check, mock_make, mock_path):
        with open("abce", 'w') as f0:
            f0.write("write file!!!")
        with open("abce") as f1:
            response = self.client.post("/fts/?path=../test/", data={"fileName": "temp_upload.log", "file": f1})
            self.assertFalse(mock_upload.called)
            self.assertEqual(response.status_code, 500)

            mock_check.return_value = False
            response = self.client.post("/fts/", data={"fileName": "temp_upload.log", "file": f1})
            self.assertFalse(mock_upload.called)
            self.assertEqual(response.status_code, 500)

            mock_check.return_value = True
            mock_make.return_value = True
            mock_path.return_value = True
            response = self.client.post("/fts/", data={"fileName": "temp_upload.log", "file": f1})
            self.assertFalse(mock_upload.called)
            self.assertEqual(response.status_code, 500)

            mock_path.return_value = False
            mock_upload.return_value = "upload success"
            response = self.client.post("/fts/", data={"fileName": "temp_upload.log", "file": f1})
            self.assertTrue(mock_upload.called)
            self.assertEqual(response.status_code, 200)

    # test download File
    @mock.patch("os.path.exists")
    @mock.patch('ft.service.make_path')
    @mock.patch('ft.service.download_file')
    def test_downloadfile(self, mock_download, mock_make, mock_path):
        response = self.client.get("/fts/anyFile.log/?path=../test/")
        self.assertFalse(mock_download.called)
        self.assertEqual(response.status_code, 500)

        mock_make.return_value = True
        mock_path.return_value = False
        response = self.client.get("/fts/anyFile.log/")
        self.assertFalse(mock_download.called)
        self.assertEqual(response.status_code, 500)

        mock_make.return_value = True
        mock_path.return_value = True
        mock_download.return_value = "abc"
        response = self.client.get("/fts/anyFile.log/")
        self.assertTrue(mock_download.called)
        self.assertEqual(response.status_code, 200)


class TestService(TestCase):

    # test upload
    @mock.patch('__builtin__.open')
    def test_upload(self, open_mock):
        data = "abcdefghijklmnopqrstuvwxyz"
        f = mock.Mock(chunks=lambda: data)
        open_mock.return_value = open("abce", 'w')
        service.upload_file(f, 'abce')
        self.assertTrue(open_mock.return_value.write.called)
        self.assertTrue(open_mock.return_value.close.called)

    # test checkSize
    def test_size(self):
        f_file = mock.Mock(size=500000)
        c = service.check_filesize(f_file)
        self.assertEqual(c, True)
        f_file = mock.Mock(size=500000001)
        c = service.check_filesize(f_file)
        self.assertEqual(c, False)

    # test make path
    @mock.patch("os.path.isdir")
    @mock.patch.object(os, "makedirs")
    def test_makePath(self, mock_make, mock_dir):
        mock_dir.return_value = 1
        service.make_path("any path")
        self.assertFalse(mock_make.called)

        mock_dir.return_value = 0
        service.make_path("any path")
        self.assertTrue(mock_make.called)

    # test delete
    @mock.patch.object(os, 'remove')
    @mock.patch('os.path')
    def test_delete(self, mock_path, mock_remove):
        mock_path.exists.return_value = False
        service.delete_file("any path")
        self.assertFalse(mock_remove.called)

        mock_path.exists.return_value = True
        service.delete_file("any path")
        self.assertTrue(mock_remove.called)

    @mock.patch('ft.service')
    def test_readFtsList(self, mock_service):
        cmdurl = "/fts/"
        mock_service.get_ft_list.return_value = "ttt"
        response = self.client.get(cmdurl)

        self.assertEqual(response.status_code, 200)

    def test_create_file(self):
        with mock.patch('__builtin__.open', mock.mock_open(), create=True) as m:
            service.creat_file("anyfile")
        m.assert_called_with("anyfile", 'w')
        wm = m()
        wm.write.assert_called_with("write file!!!")

    def test_upload_file(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.chunks.return_value = "write"
        with mock.patch('__builtin__.open', mock.mock_open(), create=True) as m:
            service.upload_file(file_mock, 'anyfile')
        m.assert_called_with("anyfile", 'w')
        wm = m()
        self.assertTrue(file_mock.chunks.called)
        self.assertTrue(wm.write.called)
        self.assertTrue(wm.close.called)

    def test_file_name(self):
        print service.rule_filename("C:\kapath\\temp1.py")
        print service.rule_filename("temp1.py")
        print service.rule_filename(" ")
