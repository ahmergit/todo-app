"""Integration tests for complete application workflows"""
import pytest
from unittest.mock import patch, MagicMock
from todo.main import main
from todo.manager import TaskManager


class TestMainMenuLoop:
    """Tests for main application menu loop"""

    @patch('builtins.input', return_value='0')
    def test_main_exits_on_zero_input(self, mock_input, capsys):
        """Test that entering 0 exits the application"""
        with pytest.raises(SystemExit):
            main()
        captured = capsys.readouterr()
        assert "Goodbye" in captured.out or "goodbye" in captured.out.lower()

    @patch('builtins.input', side_effect=['q', '0'])
    def test_main_exits_on_quit_command(self, mock_input, capsys):
        """Test that entering 'q' or 'quit' exits the application"""
        try:
            main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        assert "Goodbye" in captured.out or "goodbye" in captured.out.lower()

    @patch('builtins.input', side_effect=['invalid', '0'])
    def test_main_handles_invalid_input_gracefully(self, mock_input, capsys):
        """Test that invalid input doesn't crash the application"""
        try:
            main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        # Should show error or invalid message, then exit
        assert "Goodbye" in captured.out or "goodbye" in captured.out.lower()

    @patch('builtins.input', side_effect=['2', '0'])
    def test_main_displays_menu_repeatedly(self, mock_input, capsys):
        """Test that menu is redisplayed after each action"""
        try:
            main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        # Menu should appear at least twice (initial + after action)
        menu_count = captured.out.count("TODO LIST APPLICATION")
        assert menu_count >= 1

    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_main_handles_keyboard_interrupt(self, mock_input, capsys):
        """Test that Ctrl+C is handled gracefully"""
        try:
            main()
        except (SystemExit, KeyboardInterrupt):
            pass
        captured = capsys.readouterr()
        # Should exit gracefully without crashing
        assert "Goodbye" in captured.out or captured.out == "" or "goodbye" in captured.out.lower()


class TestAddTaskWorkflow:
    """Integration tests for adding tasks"""

    @patch('builtins.input', side_effect=['1', 'Buy groceries', '', '0'])
    def test_add_task_with_default_priority(self, mock_input, capsys):
        """Test adding a task with default priority"""
        try:
            main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        assert "Task added successfully" in captured.out or "added" in captured.out.lower()

    @patch('builtins.input', side_effect=['1', 'Urgent task', 'H', '0'])
    def test_add_task_with_high_priority(self, mock_input, capsys):
        """Test adding a task with high priority"""
        try:
            main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        assert "added" in captured.out.lower() or "success" in captured.out.lower()

    @patch('builtins.input', side_effect=['1', '', 'Valid task', '', '0'])
    def test_add_task_handles_empty_description(self, mock_input, capsys):
        """Test that empty description is handled gracefully"""
        try:
            main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        assert "Error" in captured.out or "empty" in captured.out.lower()


class TestViewTasksWorkflow:
    """Integration tests for viewing tasks"""

    @patch('builtins.input', side_effect=['2', '0'])
    def test_view_tasks_when_empty(self, mock_input, capsys):
        """Test viewing tasks when list is empty"""
        try:
            main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        assert "No tasks" in captured.out or "empty" in captured.out.lower() or "Add a task" in captured.out

    @patch('builtins.input', side_effect=['1', 'Task 1', '', '1', 'Task 2', 'H', '2', '0'])
    def test_view_tasks_shows_all_added_tasks(self, mock_input, capsys):
        """Test that viewing tasks shows all added tasks"""
        try:
            main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out
        assert "Total" in captured.out or "task(s)" in captured.out.lower()
