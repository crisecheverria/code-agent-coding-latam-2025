import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock
import importlib.util
from pathlib import Path

# Import the module with numeric prefix
spec = importlib.util.spec_from_file_location("edit_tool", "06_edit_text_tool.py")
edit_tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edit_tool)

handle_text_editor_tool = edit_tool.handle_text_editor_tool
handle_view = edit_tool.handle_view
handle_str_replace = edit_tool.handle_str_replace
handle_create = edit_tool.handle_create
handle_insert = edit_tool.handle_insert


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_file(temp_dir):
    """Create a sample file for testing."""
    file_path = temp_dir / "test.py"
    content = """def hello():
    print("Hello, World!")
    return True

def goodbye():
    print("Goodbye!")
"""
    file_path.write_text(content, encoding='utf-8')
    return file_path


class TestHandleView:
    def test_view_file_complete(self, sample_file):
        """Test viewing complete file contents."""
        result = handle_view(str(sample_file))
        
        assert "1: def hello():" in result
        assert "2:     print(\"Hello, World!\")" in result
        assert "6:     print(\"Goodbye!\")" in result
    
    def test_view_file_with_range(self, sample_file):
        """Test viewing file with specific line range."""
        result = handle_view(str(sample_file), (2, 4))
        
        assert "2:     print(\"Hello, World!\")" in result
        assert "3:     return True" in result
        assert "4:" in result
        assert "1: def hello():" not in result
    
    def test_view_directory(self, temp_dir, sample_file):
        """Test viewing directory contents."""
        result = handle_view(str(temp_dir))
        
        assert "Directory contents of" in result
        assert "test.py" in result
    
    def test_view_nonexistent_file(self, temp_dir):
        """Test viewing non-existent file."""
        result = handle_view(str(temp_dir / "nonexistent.py"))
        assert "Error: File not found" in result


class TestHandleStrReplace:
    def test_str_replace_success(self, sample_file):
        """Test successful string replacement."""
        old_str = 'print("Hello, World!")'
        new_str = 'print("Hello, Universe!")'
        
        result = handle_str_replace(str(sample_file), old_str, new_str)
        
        assert "Successfully replaced text at exactly one location" in result
        
        # Verify the change was made
        content = sample_file.read_text(encoding='utf-8')
        assert 'print("Hello, Universe!")' in content
        assert 'print("Hello, World!")' not in content
    
    def test_str_replace_no_match(self, sample_file):
        """Test string replacement with no matches."""
        result = handle_str_replace(str(sample_file), "nonexistent text", "replacement")
        assert "Error: No match found for replacement text" in result
    
    def test_str_replace_multiple_matches(self, temp_dir):
        """Test string replacement with multiple matches."""
        file_path = temp_dir / "multiple.py"
        content = """print("test")
print("test")
print("test")"""
        file_path.write_text(content, encoding='utf-8')
        
        result = handle_str_replace(str(file_path), 'print("test")', 'print("new")')
        assert "Error: Found 3 matches for replacement text" in result
    
    def test_str_replace_nonexistent_file(self, temp_dir):
        """Test string replacement on non-existent file."""
        result = handle_str_replace(str(temp_dir / "missing.py"), "old", "new")
        assert "Error: File not found" in result


class TestHandleCreate:
    def test_create_new_file(self, temp_dir):
        """Test creating a new file."""
        file_path = temp_dir / "new_file.py"
        content = "print('New file created!')"
        
        result = handle_create(str(file_path), content)
        
        assert f"Successfully created file {file_path}" in result
        assert file_path.exists()
        assert file_path.read_text(encoding='utf-8') == content
    
    def test_create_file_with_directories(self, temp_dir):
        """Test creating a file with nested directories."""
        file_path = temp_dir / "subdir" / "nested" / "file.py"
        content = "# Nested file"
        
        result = handle_create(str(file_path), content)
        
        assert f"Successfully created file {file_path}" in result
        assert file_path.exists()
        assert file_path.read_text(encoding='utf-8') == content
    
    def test_create_existing_file(self, sample_file):
        """Test creating a file that already exists."""
        result = handle_create(str(sample_file), "new content")
        assert f"Error: File {sample_file} already exists" in result


class TestHandleInsert:
    def test_insert_at_beginning(self, sample_file):
        """Test inserting text at the beginning of file."""
        new_text = "# New header comment"
        
        result = handle_insert(str(sample_file), 0, new_text)
        
        assert "Successfully inserted text at line 0" in result
        
        lines = sample_file.read_text(encoding='utf-8').splitlines()
        assert lines[0] == "# New header comment"
        assert lines[1] == "def hello():"
    
    def test_insert_at_middle(self, sample_file):
        """Test inserting text in the middle of file."""
        new_text = "    # Comment before return"
        
        result = handle_insert(str(sample_file), 2, new_text)
        
        assert "Successfully inserted text at line 2" in result
        
        lines = sample_file.read_text(encoding='utf-8').splitlines()
        assert lines[2] == "    # Comment before return"
    
    def test_insert_nonexistent_file(self, temp_dir):
        """Test inserting into non-existent file."""
        result = handle_insert(str(temp_dir / "missing.py"), 0, "text")
        assert "Error: File not found" in result


class TestHandleTextEditorTool:
    def test_security_directory_traversal(self):
        """Test security check for directory traversal."""
        tool_call = Mock()
        tool_call.input = {
            'command': 'view',
            'path': '../../../etc/passwd'
        }
        
        result = handle_text_editor_tool(tool_call)
        assert "Error: Invalid file path for security reasons" in result
    
    def test_security_absolute_path(self):
        """Test security check for absolute paths."""
        tool_call = Mock()
        tool_call.input = {
            'command': 'view',
            'path': '/etc/passwd'
        }
        
        result = handle_text_editor_tool(tool_call)
        assert "Error: Invalid file path for security reasons" in result
    
    def test_security_home_directory(self):
        """Test security check for home directory paths."""
        tool_call = Mock()
        tool_call.input = {
            'command': 'view',
            'path': '~/sensitive_file.txt'
        }
        
        result = handle_text_editor_tool(tool_call)
        assert "Error: Invalid file path for security reasons" in result
    
    def test_security_file_extension(self):
        """Test security check for disallowed file extensions."""
        tool_call = Mock()
        tool_call.input = {
            'command': 'view',
            'path': 'malicious.exe'
        }
        
        result = handle_text_editor_tool(tool_call)
        assert "Error: File extension '.exe' not allowed for security reasons" in result
    
    def test_allowed_file_extensions(self, temp_dir):
        """Test that allowed file extensions work."""
        allowed_extensions = ['.py', '.txt', '.md', '.json', '.yaml', '.yml', '.js', '.ts', '.html', '.css', '.sh']
        
        for ext in allowed_extensions:
            file_path = temp_dir / f"test{ext}"
            file_path.write_text("test content", encoding='utf-8')
            
            tool_call = Mock()
            tool_call.input = {
                'command': 'view',
                'path': str(file_path.name)  # Just use the filename
            }
            
            result = handle_text_editor_tool(tool_call)
            assert "Error:" not in result or "File not found" in result  # File not found is OK
    
    def test_unknown_command(self):
        """Test handling of unknown commands."""
        tool_call = Mock()
        tool_call.input = {
            'command': 'unknown_command',
            'path': 'test.py'
        }
        
        result = handle_text_editor_tool(tool_call)
        assert "Error: Unknown command 'unknown_command'" in result


class TestEdgeCases:
    def test_unicode_content(self, temp_dir):
        """Test handling of Unicode content."""
        file_path = temp_dir / "unicode_test.py"
        unicode_content = """# Español, Français, 中文
def greet():
    print("Hola! 你好! Bonjour! 🌍")
"""
        file_path.write_text(unicode_content, encoding='utf-8')
        
        # Test view
        result = handle_view(str(file_path))
        assert "你好" in result
        assert "🌍" in result
        
        # Test replacement
        result = handle_str_replace(str(file_path), "你好", "Hello")
        assert "Successfully replaced" in result
    
    def test_empty_file_operations(self, temp_dir):
        """Test operations on empty files."""
        empty_file = temp_dir / "empty.py"
        empty_file.write_text("", encoding='utf-8')
        
        # Test view empty file
        result = handle_view(str(empty_file))
        assert result == ""
        
        # Test replace in empty file
        result = handle_str_replace(str(empty_file), "something", "else")
        assert "Error: No match found" in result
        
        # Test insert in empty file
        result = handle_insert(str(empty_file), 0, "First line")
        assert "Successfully inserted" in result
    
    def test_large_file_handling(self, temp_dir):
        """Test handling of larger files."""
        large_file = temp_dir / "large.py"
        lines = [f"# Line {i}" for i in range(1000)]
        content = "\n".join(lines)
        large_file.write_text(content, encoding='utf-8')
        
        # Test view with range
        result = handle_view(str(large_file), (500, 505))
        assert "500: # Line 499" in result  # 0-indexed in array, 1-indexed in display
        assert "505: # Line 504" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
