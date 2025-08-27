import unittest
import json
import os
import tempfile
from app import app
from services.progress_manager import ProgressManager

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)

    def test_get_progress_api(self):
        """進捗データ取得APIのテスト"""
        response = self.app.get('/api/progress')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIn('completed_sessions', data['data'])
        self.assertIn('focus_minutes', data['data'])
        self.assertIn('date', data['data'])

    def test_post_progress_api(self):
        """進捗データ保存APIのテスト"""
        payload = {'focus_minutes': 25}
        response = self.app.post('/api/progress', 
                                json=payload, 
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)

class ProgressManagerTestCase(unittest.TestCase):
    def setUp(self):
        # テスト用の一時ファイルを作成
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test_progress.json')
        self.progress_manager = ProgressManager(self.test_file)

    def tearDown(self):
        # テスト後にファイルを削除
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    def test_get_today_progress_initial(self):
        """初期状態の今日の進捗取得テスト"""
        progress = self.progress_manager.get_today_progress()
        self.assertEqual(progress['completed_sessions'], 0)
        self.assertEqual(progress['focus_minutes'], 0)
        self.assertIn('date', progress)

    def test_add_completed_session(self):
        """セッション完了追加のテスト"""
        # 最初のセッション追加
        progress = self.progress_manager.add_completed_session(25)
        self.assertEqual(progress['completed_sessions'], 1)
        self.assertEqual(progress['focus_minutes'], 25)
        
        # 2回目のセッション追加
        progress = self.progress_manager.add_completed_session(30)
        self.assertEqual(progress['completed_sessions'], 2)
        self.assertEqual(progress['focus_minutes'], 55)

if __name__ == '__main__':
    unittest.main()
