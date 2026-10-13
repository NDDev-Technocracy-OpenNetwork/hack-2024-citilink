import os
import unittest
from unittest.mock import Mock, patch

from clever_search import get_search_results
from neuro_mentor import get_ya_gpt


class ClientsTest(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_credentials_do_not_send_network_requests(self):
        with patch('requests.post') as post, patch('requests.get') as get:
            with self.assertRaises(RuntimeError):
                get_ya_gpt('question')
            with self.assertRaises(RuntimeError):
                get_search_results('product')
            post.assert_not_called()
            get.assert_not_called()

    @patch.dict(os.environ, {'YANDEX_FOLDER_ID': 'test-folder', 'YANDEX_API_KEY': 'test-key'}, clear=True)
    def test_completion_schema_and_message_text(self):
        response = Mock()
        response.json.return_value = {'result': {'alternatives': [{'message': {'text': 'answer'}}]}}
        with patch('requests.post', return_value=response) as post:
            self.assertEqual(get_ya_gpt('question'), 'answer')
        args = post.call_args.kwargs
        self.assertEqual(args['json']['completionOptions']['temperature'], 0.3)
        self.assertEqual(args['headers']['Authorization'], 'Api-Key test-key')
        self.assertEqual(args['timeout'], (10, 60))

    @patch.dict(os.environ, {'YANDEX_FOLDER_ID': 'test-folder', 'YANDEX_SEARCH_API_KEY': 'test-key'}, clear=True)
    def test_xml_single_group_and_document(self):
        response = Mock(text='<yandexsearch><response><results><grouping><group><doc><url>https://example.com</url></doc></group></grouping></results></response></yandexsearch>')
        with patch('requests.get', return_value=response):
            self.assertEqual(get_search_results('product'), ['https://example.com'])


if __name__ == '__main__':
    unittest.main()
