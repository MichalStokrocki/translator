
import unittest
from unittest.mock import mock_open, patch
from PyQt5.QtWidgets import QApplication
from Translator import Translator



class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.window = Translator()

    def tearDown(self):
        self.window.close()

    @patch('Translator.QFileDialog.getOpenFileName')
    @patch('Translator.open', new_callable=mock_open,
           read_data='Panno święta, co Jasnej bronisz Częstochowy\nI w Ostrej świecisz Bramie! Ty, co gród zamkowy')
    def test_choose_file(self, mock_open, mock_getOpenFileName):
        mock_getOpenFileName.return_value = ('/path/to/testfile.txt', 'Text files (*.txt)')
        self.window.choose_file()
        self.assertEqual(self.window.file_name, 'testfile-en')
        self.assertEqual(self.window.input_file_path, '/path/to/testfile.txt')
        expected_preview = ('Panno święta, co Jasnej bronisz Częstochowy\nI w Ostrej świecisz Bramie! Ty, co gród '
                            'zamkowy')[
                           :50]
        self.assertIn(expected_preview, self.window.text_display.toPlainText())

    @patch('Translator.QFileDialog.getExistingDirectory')
    def test_choose_save_location(self, mock_get_existing_directory):
        mock_get_existing_directory.return_value = '/test/directory'
        self.window.choose_save_location()
        self.assertEqual(self.window.save_path_entry.text(), '/test/directory')


    @patch('Translator.QMessageBox.information')
    @patch('Translator.open', new_callable=mock_open, read_data='Panno święta, co Jasnej bronisz Częstochowy')
    def test_translate_and_save(self, mock_open, mock_information):

        self.window.input_file_path = '/path/to/testfile.txt', 'Text files (*.txt)'
        self.window.save_path_entry.setText('/test/directory')
        self.window.file_name_entry.setText('testfile-en')

        self.window.translate_and_save()

        self.assertEqual(self.window.translated_text, 'Miss Christmas, what are you defending?')
        mock_information.assert_called_with(self.window, "Sukces", "Plik przetłumaczony i zapisany w /test/directory\\testfile-en.txt")

    @patch('Translator.QMessageBox.critical')
    def test_translate_and_save_no_file(self, mock_critical):
        self.window.translate_and_save()
        mock_critical.assert_called_with(self.window, "Błąd", "Wybierz plik do przetłumaczenia.")

    @patch('Translator.QMessageBox.critical')
    def test_translate_and_save_no_save_location(self, mock_critical):
        self.window.input_file_path = 'test_file.txt'
        self.window.translate_and_save()
        mock_critical.assert_called_with(self.window, "Błąd", "Wybierz miejsce zapisu pliku.")

    @patch('Translator.QMessageBox.critical')
    def test_translate_and_save_no_file_name(self, mock_critical):
        self.window.input_file_path = 'test_file.txt'
        self.window.save_path_entry.setText('/test/directory')
        self.window.translate_and_save()
        mock_critical.assert_called_with(self.window, "Błąd", "Wybierz nazwe pliku.")


if __name__ == '__main__':
    unittest.main()
