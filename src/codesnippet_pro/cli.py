#!/usr/bin/env python3
"""
CodeSnippet Pro - Command Line Interface
"""

import argparse
import sys
import os
from typing import Optional, List

from codesnippet_pro.database import SnippetDatabase
from codesnippet_pro.ui import SnippetUI
from codesnippet_pro.utils import get_data_dir, ensure_dir
from codesnippet_pro import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog="csp",
        description="🚀 CodeSnippet Pro - Intelligent Code Snippet Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  csp add                    # Add a new snippet interactively
  csp search python          # Search snippets containing 'python'
  csp list --lang python     # List all Python snippets
  csp show 1                 # Display snippet with ID 1
  csp edit 1                 # Edit snippet with ID 1
  csp delete 1               # Delete snippet with ID 1
  csp export backup.json     # Export snippets to JSON
  csp import backup.json     # Import snippets from JSON
  csp stats                  # Show usage statistics
        """
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"CodeSnippet Pro v{__version__}"
    )
    
    parser.add_argument(
        "-d", "--data-dir",
        help="Custom data directory (default: ~/.codesnippet-pro)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new snippet")
    add_parser.add_argument("-t", "--title", help="Snippet title")
    add_parser.add_argument("-c", "--code", help="Code content")
    add_parser.add_argument("-l", "--language", help="Programming language")
    add_parser.add_argument("-g", "--tags", help="Tags (comma-separated)")
    add_parser.add_argument("-d", "--description", help="Description")
    add_parser.add_argument("--from-clipboard", action="store_true", help="Read code from clipboard")
    add_parser.add_argument("--from-file", help="Read code from file")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search snippets")
    search_parser.add_argument("query", nargs="?", help="Search query")
    search_parser.add_argument("-l", "--language", help="Filter by language")
    search_parser.add_argument("-g", "--tag", help="Filter by tag")
    search_parser.add_argument("--fuzzy", action="store_true", help="Enable fuzzy search")
    
    # List command
    list_parser = subparsers.add_parser("list", aliases=["ls"], help="List all snippets")
    list_parser.add_argument("-l", "--language", help="Filter by language")
    list_parser.add_argument("-g", "--tag", help="Filter by tag")
    list_parser.add_argument("--limit", type=int, default=50, help="Limit results")
    list_parser.add_argument("--sort", choices=["date", "title", "language"], default="date",
                            help="Sort by field")
    
    # Show command
    show_parser = subparsers.add_parser("show", aliases=["view", "cat"], help="Show snippet details")
    show_parser.add_argument("id", type=int, help="Snippet ID")
    show_parser.add_argument("-c", "--copy", action="store_true", help="Copy to clipboard")
    
    # Edit command
    edit_parser = subparsers.add_parser("edit", help="Edit a snippet")
    edit_parser.add_argument("id", type=int, help="Snippet ID")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", aliases=["rm", "remove"], help="Delete a snippet")
    delete_parser.add_argument("id", type=int, help="Snippet ID")
    delete_parser.add_argument("-f", "--force", action="store_true", help="Force delete without confirmation")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export snippets")
    export_parser.add_argument("file", help="Output file path")
    export_parser.add_argument("-f", "--format", choices=["json", "csv", "md"], default="json",
                              help="Export format")
    export_parser.add_argument("-l", "--language", help="Filter by language")
    
    # Import command
    import_parser = subparsers.add_parser("import", help="Import snippets")
    import_parser.add_argument("file", help="Input file path")
    import_parser.add_argument("-f", "--format", choices=["json", "csv"], default="json",
                              help="Import format")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    
    # Languages command
    subparsers.add_parser("languages", aliases=["langs"], help="List all languages")
    
    # Tags command
    subparsers.add_parser("tags", help="List all tags")
    
    # Interactive command
    subparsers.add_parser("interactive", aliases=["i", "tui"], help="Launch interactive TUI mode")
    
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    # Determine data directory
    data_dir = parsed_args.data_dir or get_data_dir()
    ensure_dir(data_dir)
    
    db_path = os.path.join(data_dir, "snippets.db")
    
    # Initialize database
    db = SnippetDatabase(db_path)
    
    # Initialize UI
    ui = SnippetUI(db)
    
    # Handle commands
    try:
        if parsed_args.command == "add":
            return ui.cmd_add(parsed_args)
        elif parsed_args.command in ("search", None):
            if parsed_args.command is None:
                parser.print_help()
                return 0
            return ui.cmd_search(parsed_args)
        elif parsed_args.command in ("list", "ls"):
            return ui.cmd_list(parsed_args)
        elif parsed_args.command in ("show", "view", "cat"):
            return ui.cmd_show(parsed_args)
        elif parsed_args.command == "edit":
            return ui.cmd_edit(parsed_args)
        elif parsed_args.command in ("delete", "rm", "remove"):
            return ui.cmd_delete(parsed_args)
        elif parsed_args.command == "export":
            return ui.cmd_export(parsed_args)
        elif parsed_args.command == "import":
            return ui.cmd_import(parsed_args)
        elif parsed_args.command == "stats":
            return ui.cmd_stats(parsed_args)
        elif parsed_args.command in ("languages", "langs"):
            return ui.cmd_languages(parsed_args)
        elif parsed_args.command == "tags":
            return ui.cmd_tags(parsed_args)
        elif parsed_args.command in ("interactive", "i", "tui"):
            return ui.run_interactive()
        else:
            parser.print_help()
            return 0
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
