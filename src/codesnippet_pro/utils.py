#!/usr/bin/env python3
"""
CodeSnippet Pro - Utility Functions
"""

import os
import sys
from pathlib import Path
from typing import Optional


def get_data_dir() -> str:
    """Get the data directory for CodeSnippet Pro."""
    # Check environment variable first
    if "CODESNIPPET_PRO_DATA" in os.environ:
        return os.environ["CODESNIPPET_PRO_DATA"]
    
    # Use platform-specific directories
    if sys.platform == "win32":
        # Windows: %APPDATA%\\CodeSnippet Pro
        base_dir = os.environ.get("APPDATA", Path.home())
        return os.path.join(base_dir, "CodeSnippet Pro")
    elif sys.platform == "darwin":
        # macOS: ~/Library/Application Support/CodeSnippet Pro
        return os.path.join(Path.home(), "Library", "Application Support", "CodeSnippet Pro")
    else:
        # Linux/Unix: ~/.local/share/codesnippet-pro or ~/.codesnippet-pro
        xdg_data = os.environ.get("XDG_DATA_HOME")
        if xdg_data:
            return os.path.join(xdg_data, "codesnippet-pro")
        return os.path.join(Path.home(), ".codesnippet-pro")


def ensure_dir(directory: str) -> None:
    """Ensure directory exists, create if not."""
    Path(directory).mkdir(parents=True, exist_ok=True)


def get_editor() -> Optional[str]:
    """Get the system's default editor."""
    for env_var in ["EDITOR", "VISUAL"]:
        editor = os.environ.get(env_var)
        if editor:
            return editor
    
    # Try common editors
    for editor in ["vim", "nano", "emacs", "code", "notepad"]:
        if os.system(f"which {editor} > /dev/null 2>&1") == 0:
            return editor
    
    return None


def truncate_string(s: str, max_length: int, suffix: str = "...") -> str:
    """Truncate string to max_length."""
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def detect_language_from_extension(filename: str) -> Optional[str]:
    """Detect programming language from file extension."""
    ext_map = {
        ".py": "python",
        ".pyw": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".java": "java",
        ".go": "go",
        ".rs": "rust",
        ".c": "c",
        ".h": "c",
        ".cpp": "cpp",
        ".hpp": "cpp",
        ".cs": "csharp",
        ".rb": "ruby",
        ".php": "php",
        ".swift": "swift",
        ".kt": "kotlin",
        ".scala": "scala",
        ".r": "r",
        ".sh": "bash",
        ".bash": "bash",
        ".zsh": "bash",
        ".sql": "sql",
        ".html": "html",
        ".htm": "html",
        ".css": "css",
        ".scss": "css",
        ".sass": "css",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".xml": "xml",
        ".md": "markdown",
        ".dockerfile": "dockerfile",
        ".tf": "terraform",
    }
    
    ext = Path(filename).suffix.lower()
    return ext_map.get(ext)


def detect_language_from_shebang(code: str) -> Optional[str]:
    """Detect programming language from shebang line."""
    if not code.startswith("#!/"):
        return None
    
    shebang = code.split("\n")[0]
    
    shebang_map = {
        "python": "python",
        "python3": "python",
        "node": "javascript",
        "bash": "bash",
        "sh": "shell",
        "zsh": "bash",
        "ruby": "ruby",
        "perl": "perl",
        "php": "php",
    }
    
    for key, lang in shebang_map.items():
        if key in shebang:
            return lang
    
    return None
