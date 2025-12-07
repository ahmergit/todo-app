"""Unit tests for UI layer functions"""
import pytest
from io import StringIO
from unittest.mock import patch
from todo.ui import display_menu, get_menu_choice, validate_description, validate_priority_input, format_task_display
from todo.models import Task, Priority
from todo.manager import TaskManager


class TestDisplayMenu:
    """Tests for menu display function"""

    def test_display_menu_outputs_header(self, capsys):
        """Test that menu displays header"""
        display_menu()
        captured = capsys.readouterr()
        assert "TODO LIST APPLICATION" in captured.out

    def test_display_menu_outputs_all_options(self, capsys):
        """Test that menu displays all action options"""
        display_menu()
        captured = capsys.readouterr()
        assert "1. Add Task" in captured.out
        assert "2. View Tasks" in captured.out
        assert "3. Update Task" in captured.out
        assert "4. Delete Task" in captured.out
        assert "5. Complete Task" in captured.out
        assert "6. Set Priority" in captured.out
        assert "0. Exit" in captured.out

    def test_display_menu_outputs_menu_structure(self, capsys):
        """Test that menu displays proper structure"""
        display_menu()
        captured = capsys.readouterr()
        assert "Main Menu" in captured.out or "menu" in captured.out.lower()


class TestGetMenuChoice:
    """Tests for menu choice validation"""

    @patch('builtins.input', return_value='1')
    def test_get_menu_choice_returns_valid_choice(self, mock_input):
        """Test that valid menu choice is returned"""
        choice = get_menu_choice()
        assert choice == '1'

    @patch('builtins.input', return_value='0')
    def test_get_menu_choice_accepts_exit_option(self, mock_input):
        """Test that exit option (0) is accepted"""
        choice = get_menu_choice()
        assert choice == '0'

    @patch('builtins.input', return_value='6')
    def test_get_menu_choice_accepts_all_valid_options(self, mock_input):
        """Test that all valid options (0-6) are accepted"""
        choice = get_menu_choice()
        assert choice in ['0', '1', '2', '3', '4', '5', '6']

    @patch('builtins.input', side_effect=['invalid', '1'])
    def test_get_menu_choice_handles_invalid_input(self, mock_input):
        """Test that invalid input is handled gracefully"""
        choice = get_menu_choice()
        assert choice == '1'

    @patch('builtins.input', side_effect=['99', '1'])
    def test_get_menu_choice_rejects_out_of_range(self, mock_input):
        """Test that out-of-range numbers are rejected"""
        choice = get_menu_choice()
        assert choice == '1'

    @patch('builtins.input', return_value='q')
    def test_get_menu_choice_accepts_quit_command(self, mock_input):
        """Test that 'q' or 'quit' commands are accepted"""
        choice = get_menu_choice()
        assert choice.lower() in ['q', 'quit', '0']


class TestValidateDescription:
    """Tests for description validation"""

    def test_validate_description_accepts_valid_input(self):
        """Test that valid description passes validation"""
        is_valid, error = validate_description("Buy groceries")
        assert is_valid is True
        assert error == ""

    def test_validate_description_rejects_empty_string(self):
        """Test that empty string fails validation"""
        is_valid, error = validate_description("")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_validate_description_rejects_whitespace_only(self):
        """Test that whitespace-only string fails validation"""
        is_valid, error = validate_description("   ")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_validate_description_accepts_max_length(self):
        """Test that 500-character description passes"""
        description = "a" * 500
        is_valid, error = validate_description(description)
        assert is_valid is True
        assert error == ""

    def test_validate_description_rejects_over_max_length(self):
        """Test that 501-character description fails"""
        description = "a" * 501
        is_valid, error = validate_description(description)
        assert is_valid is False
        assert "500" in error


class TestValidatePriorityInput:
    """Tests for priority input validation"""

    def test_validate_priority_accepts_high(self):
        """Test that 'H' returns HIGH priority"""
        priority, error = validate_priority_input("H")
        assert priority == Priority.HIGH
        assert error == ""

    def test_validate_priority_accepts_medium(self):
        """Test that 'M' returns MEDIUM priority"""
        priority, error = validate_priority_input("M")
        assert priority == Priority.MEDIUM
        assert error == ""

    def test_validate_priority_accepts_low(self):
        """Test that 'L' returns LOW priority"""
        priority, error = validate_priority_input("L")
        assert priority == Priority.LOW
        assert error == ""

    def test_validate_priority_accepts_lowercase(self):
        """Test that lowercase input works"""
        priority, error = validate_priority_input("h")
        assert priority == Priority.HIGH
        assert error == ""

    def test_validate_priority_defaults_to_medium_on_empty(self):
        """Test that empty input defaults to MEDIUM"""
        priority, error = validate_priority_input("")
        assert priority == Priority.MEDIUM
        assert error == ""

    def test_validate_priority_rejects_invalid_input(self):
        """Test that invalid input returns None and error"""
        priority, error = validate_priority_input("X")
        assert priority is None
        assert "H" in error and "M" in error and "L" in error


class TestFormatTaskDisplay:
    """Tests for task display formatting"""

    def test_format_task_display_shows_task_id(self):
        """Test that formatted output includes task ID"""
        task = Task(id=1, description="Test task")
        output = format_task_display(task)
        assert "[1]" in output

    def test_format_task_display_shows_description(self):
        """Test that formatted output includes description"""
        task = Task(id=1, description="Buy groceries")
        output = format_task_display(task)
        assert "Buy groceries" in output

    def test_format_task_display_shows_priority(self):
        """Test that formatted output includes priority"""
        task = Task(id=1, description="Test", priority=Priority.HIGH)
        output = format_task_display(task)
        assert "High" in output

    def test_format_task_display_shows_incomplete_status(self):
        """Test that incomplete tasks show as incomplete"""
        task = Task(id=1, description="Test", completed=False)
        output = format_task_display(task)
        assert "Incomplete" in output or "○" in output

    def test_format_task_display_shows_complete_status(self):
        """Test that completed tasks show as complete"""
        task = Task(id=1, description="Test", completed=True)
        output = format_task_display(task)
        assert "COMPLETE" in output or "✓" in output
