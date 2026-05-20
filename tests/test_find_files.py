from pycounter.model import find_files


class TestFindFiles:
    def test_find_files_no_ext(self, tmp_path):
        # Create some test files
        (tmp_path / "file1.py").write_text("print('Hello')")
        (tmp_path / "file2.md").write_text("# Markdown")
        (tmp_path / "file3.txt").write_text("Just text")

        files = find_files(tmp_path, None)
        assert len(files) == 3

    def test_find_files_with_ext(self, tmp_path):
        # Create some test files
        (tmp_path / "file1.py").write_text("print('Hello')")
        (tmp_path / "file2.md").write_text("# Markdown")
        (tmp_path / "file3.txt").write_text("Just text")

        py_files = find_files(tmp_path, ".py")
        assert len(py_files) == 1
        assert py_files[0].name == "file1.py"

    def test_find_files_ignore_hidden(self, tmp_path):
        # Create some test files
        (tmp_path / "file1.py").write_text("print('Hello')")
        (tmp_path / ".hidden_file.py").write_text("print('Hidden')")
        (tmp_path / ".hidden_folder").mkdir()
        (tmp_path / ".hidden_folder" / "file2.py").write_text("print('Hidden folder')")

        files = find_files(tmp_path, ".py")
        assert len(files) == 1
        assert files[0].name == "file1.py"
