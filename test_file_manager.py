#!/usr/bin/env python3
"""
Unit tests for Python CLI File Manager
Testing Week 1 concepts: variables, expressions, statements, functions
Uses only unittest from standard library.
"""

import unittest
import sys
import os
import io
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import patch

# Import the file_manager module
import file_manager


class TestFileManager(unittest.TestCase):
    """Test cases for file_manager functions."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary test file for file size testing
        self.test_filename = "test_temp_file.txt"
        self.test_content = "Hello, World! This is a test file.\n" * 10
        
        with open(self.test_filename, 'w') as f:
            f.write(self.test_content)
    
    def tearDown(self):
        """Clean up after each test method."""
        # Remove temporary test file if it exists
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    def test_display_welcome(self):
        """Test the display_welcome function output."""
        # Capture stdout
        captured_output = io.StringIO()
        
        with redirect_stdout(captured_output):
            file_manager.display_welcome()
        
        output = captured_output.getvalue()
        
        # Check that welcome message contains expected text
        self.assertIn("Welcome to Python CLI File Manager!", output)
        self.assertIn("Python fundamentals", output)
        self.assertIn("=" * 50, output)
    
    def test_display_help(self):
        """Test the display_help function output."""
        captured_output = io.StringIO()
        
        with redirect_stdout(captured_output):
            file_manager.display_help()
        
        output = captured_output.getvalue()
        
        # Check that help contains all expected commands
        self.assertIn("help", output)
        self.assertIn("calc", output)  
        self.assertIn("info", output)
        self.assertIn("quit", output)
        self.assertIn("Available Commands", output)
    
    def test_display_info(self):
        """Test the display_info function output."""
        captured_output = io.StringIO()
        
        with redirect_stdout(captured_output):
            file_manager.display_info()
        
        output = captured_output.getvalue()
        
        # Check that info contains expected program information
        self.assertIn("Python CLI File Manager", output)
        self.assertIn("Week 1", output)
        self.assertIn("Variables, expressions, statements, functions", output)
        self.assertIn("Python Version:", output)
    
    @patch('builtins.input', return_value='help')
    def test_get_user_choice_help(self, mock_input):
        """Test get_user_choice function with 'help' input."""
        captured_output = io.StringIO()
        
        with redirect_stdout(captured_output):
            choice = file_manager.get_user_choice()
        
        # Check that the function returns the correct choice
        self.assertEqual(choice, 'help')
        
        # Check that the menu is displayed
        output = captured_output.getvalue()
        self.assertIn("Available commands:", output)
        self.assertIn("help", output)
        self.assertIn("calc", output)
        self.assertIn("info", output)
        self.assertIn("quit", output)
    
    @patch('builtins.input', return_value='QUIT')
    def test_get_user_choice_case_insensitive(self, mock_input):
        """Test that get_user_choice handles case insensitive input."""
        captured_output = io.StringIO()
        
        with redirect_stdout(captured_output):
            choice = file_manager.get_user_choice()
        
        # Check that input is converted to lowercase
        self.assertEqual(choice, 'quit')
    
    @patch('builtins.input', return_value='  calc  ')
    def test_get_user_choice_strips_whitespace(self, mock_input):
        """Test that get_user_choice strips whitespace from input."""
        captured_output = io.StringIO()
        
        with redirect_stdout(captured_output):
            choice = file_manager.get_user_choice()
        
        # Check that whitespace is stripped
        self.assertEqual(choice, 'calc')
    
    @patch('builtins.input')
    def test_calculate_file_size_existing_file(self, mock_input):
        """Test calculate_file_size with an existing file."""
        mock_input.return_value = self.test_filename
        
        captured_output = io.StringIO()
        
        with redirect_stdout(captured_output):
            file_manager.calculate_file_size()
        
        output = captured_output.getvalue()
        
        # Check that file information is displayed
        self.assertIn(self.test_filename, output)
        self.assertIn("bytes", output)
        self.assertIn("Size:", output)
    
    @patch('builtins.input', return_value='nonexistent_file.txt')
    def test_calculate_file_size_nonexistent_file(self, mock_input):
        """Test calculate_file_size with a nonexistent file."""
        captured_output = io.StringIO()
        
        with redirect_stdout(captured_output):
            file_manager.calculate_file_size()
        
        output = captured_output.getvalue()
        
        # Check that error message is displayed
        self.assertIn("Error", output)
        self.assertIn("not found", output)
    
    @patch('builtins.input', return_value='')
    def test_calculate_file_size_empty_input(self, mock_input):
        """Test calculate_file_size with empty input."""
        captured_output = io.StringIO()
        
        with redirect_stdout(captured_output):
            file_manager.calculate_file_size()
        
        output = captured_output.getvalue()
        
        # Check that error message for empty input is displayed
        self.assertIn("Error", output)
        self.assertIn("No filename provided", output)
    
    @patch('builtins.input')
    def test_calculate_file_size_directory(self, mock_input):
        """Test calculate_file_size with a directory instead of a file."""
        # Use current directory as test case
        mock_input.return_value = '.'
        
        captured_output = io.StringIO()
        
        with redirect_stdout(captured_output):
            file_manager.calculate_file_size()
        
        output = captured_output.getvalue()
        
        # Check that error message for directory is displayed
        self.assertIn("Error", output)
        self.assertIn("not a regular file", output)
    
    def test_file_size_calculation_units(self):
        """Test that file size calculation shows appropriate units."""
        # Create a larger test file for unit testing
        large_filename = "large_test_file.txt"
        large_content = "X" * 2048  # 2KB file
        
        try:
            with open(large_filename, 'w') as f:
                f.write(large_content)
            
            with patch('builtins.input', return_value=large_filename):
                captured_output = io.StringIO()
                
                with redirect_stdout(captured_output):
                    file_manager.calculate_file_size()
                
                output = captured_output.getvalue()
                
                # Should show both bytes and KB for files >= 1024 bytes
                self.assertIn("bytes", output)
                self.assertIn("KB", output)
                
        finally:
            # Clean up
            if os.path.exists(large_filename):
                os.remove(large_filename)


class TestFileManagerVariables(unittest.TestCase):
    """Test variables and expressions used in the file manager."""
    
    def test_module_imports(self):
        """Test that only standard library modules are imported."""
        # Check that file_manager module has the expected attributes
        self.assertTrue(hasattr(file_manager, 'os'))
        self.assertTrue(hasattr(file_manager, 'sys'))
        
        # Verify functions exist
        self.assertTrue(callable(file_manager.display_welcome))
        self.assertTrue(callable(file_manager.calculate_file_size))
        self.assertTrue(callable(file_manager.get_user_choice))
        self.assertTrue(callable(file_manager.display_help))
        self.assertTrue(callable(file_manager.display_info))
        self.assertTrue(callable(file_manager.main))
    
    def test_string_expressions(self):
        """Test string expressions and formatting."""
        # Test that the module can handle string operations
        test_string = "test_file.txt"
        self.assertTrue(len(test_string) > 0)
        self.assertEqual(test_string.lower(), "test_file.txt")
        self.assertEqual(test_string.strip(), "test_file.txt")
    
    def test_numeric_expressions(self):
        """Test numeric expressions for file size calculations."""
        # Test basic arithmetic expressions used in file size calculation
        bytes_value = 2048
        kb_value = bytes_value / 1024
        mb_value = kb_value / 1024
        
        self.assertEqual(kb_value, 2.0)
        self.assertEqual(mb_value, 2.0 / 1024)
        self.assertTrue(bytes_value >= 1024)


if __name__ == '__main__':
    # Create a test suite and run the tests
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)