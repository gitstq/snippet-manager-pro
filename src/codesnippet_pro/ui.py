#!/usr/bin/env python3
"""
CodeSnippet Pro - User Interface Module
Handles all user interactions and display formatting.
"""

import os
import sys
import subprocess
from typing import Optional, List
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.tree import Tree
from rich import box

from codesnippet_pro.database import SnippetDatabase


console = Console()


class SnippetUI:
    """User interface for CodeSnippet Pro."""
    
    # Language to color mapping
    LANGUAGE_COLORS = {
        "python": "#3776ab",
        "javascript": "#f7df1e",
        "typescript": "#3178c6",
        "java": "#b07219",
        "go": "#00add8",
        "rust": "#dea584",
        "c": "#555555",
        "cpp": "#f34b7d",
        "csharp": "#178600",
        "ruby": "#701516",
        "php": "#4F5D95",
        "swift": "#ffac45",
        "kotlin": "#A97BFF",
        "scala": "#c22d40",
        "r": "#198CE7",
        "shell": "#89e051",
        "bash": "#89e051",
        "sql": "#e38c00",
        "html": "#e34c26",
        "css": "#563d7c",
        "json": "#292929",
        "yaml": "#cb171e",
        "markdown": "#083fa1",
        "dockerfile": "#384d54",
    }
    
    def __init__(self, db: SnippetDatabase):
        """Initialize UI with database instance."""
        self.db = db
    
    def _get_language_color(self, language: str) -> str:
        """Get color for a programming language."""
        return self.LANGUAGE_COLORS.get(language.lower(), "#808080")
    
    def _format_datetime(self, dt_str: str) -> str:
        """Format datetime string for display."""
        try:
            dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M")
        except:
            return dt_str
    
    def cmd_add(self, args) -> int:
        """Handle add command."""
        console.print(Panel("📝 Add New Snippet", style="bold blue"))
        
        # Get title
        title = args.title or Prompt.ask("Title")
        if not title:
            console.print("❌ Title is required!")
            return 1
        
        # Get code
        if args.from_clipboard:
            try:
                import pyperclip
                code = pyperclip.paste()
                console.print("📋 Code loaded from clipboard")
            except ImportError:
                console.print("⚠️ pyperclip not installed. Install with: pip install pyperclip")
                code = None
        elif args.from_file:
            try:
                with open(args.from_file, "r") as f:
                    code = f.read()
                console.print(f"📄 Code loaded from {args.from_file}")
            except Exception as e:
                console.print(f"❌ Error reading file: {e}")
                return 1
        else:
            code = args.code
        
        if not code:
            console.print("Enter code (Ctrl+D or empty line to finish):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            code = "\n".join(lines)
        
        if not code.strip():
            console.print("❌ Code content is required!")
            return 1
        
        # Get language
        language = args.language or Prompt.ask("Language (optional)", default="")
        
        # Get description
        description = args.description or Prompt.ask("Description (optional)", default="")
        
        # Get tags
        tags_str = args.tags or Prompt.ask("Tags (comma-separated, optional)", default="")
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        
        # Add to database
        snippet_id = self.db.add_snippet(
            title=title,
            code=code,
            language=language,
            description=description,
            tags=tags
        )
        
        console.print(f"\n✅ Snippet added successfully! ID: {snippet_id}")
        return 0
    
    def cmd_search(self, args) -> int:
        """Handle search command."""
        query = args.query or ""
        
        if not query and not args.language and not args.tag:
            query = Prompt.ask("🔍 Search query")
        
        snippets = self.db.search_snippets(
            query=query,
            language=args.language,
            tag=args.tag,
            limit=50
        )
        
        if not snippets:
            console.print("🔍 No snippets found matching your criteria.")
            return 0
        
        self._display_snippet_list(snippets, f"🔍 Search Results ({len(snippets)} found)")
        return 0
    
    def cmd_list(self, args) -> int:
        """Handle list command."""
        snippets = self.db.list_snippets(
            language=args.language,
            tag=args.tag,
            limit=args.limit,
            sort_by=args.sort
        )
        
        if not snippets:
            console.print("📭 No snippets found.")
            return 0
        
        title = "📚 All Snippets"
        if args.language:
            title += f" (Language: {args.language})"
        if args.tag:
            title += f" (Tag: {args.tag})"
        
        self._display_snippet_list(snippets, title)
        return 0
    
    def _display_snippet_list(self, snippets: List[dict], title: str) -> None:
        """Display snippets in a formatted table."""
        table = Table(
            title=title,
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )
        
        table.add_column("ID", style="dim", width=6)
        table.add_column("Title", min_width=20)
        table.add_column("Language", width=12)
        table.add_column("Tags", min_width=15)
        table.add_column("Created", width=16)
        table.add_column("Used", width=6, justify="right")
        
        for snippet in snippets:
            lang = snippet.get("language", "") or "text"
            lang_display = f"[{self._get_language_color(lang)}]{lang}[/]"
            
            tags = ", ".join(snippet.get("tags_list", []))
            if len(tags) > 30:
                tags = tags[:27] + "..."
            
            created = self._format_datetime(snippet["created_at"])
            
            table.add_row(
                str(snippet["id"]),
                snippet["title"],
                lang_display,
                tags,
                created,
                str(snippet.get("usage_count", 0))
            )
        
        console.print(table)
    
    def cmd_show(self, args) -> int:
        """Handle show command."""
        snippet = self.db.get_snippet(args.id)
        
        if not snippet:
            console.print(f"❌ Snippet with ID {args.id} not found!")
            return 1
        
        # Increment usage count
        self.db.increment_usage(args.id)
        
        # Display snippet
        lang = snippet.get("language", "") or "text"
        
        # Header panel
        header_text = f"[bold]{snippet['title']}[/bold]\n"
        if snippet.get("description"):
            header_text += f"{snippet['description']}\n"
        header_text += f"\n[yellow]Language:[/yellow] {lang}"
        if snippet.get("tags_list"):
            header_text += f"  [yellow]Tags:[/yellow] {', '.join(snippet['tags_list'])}"
        header_text += f"\n[yellow]Created:[/yellow] {self._format_datetime(snippet['created_at'])}"
        header_text += f"  [yellow]Used:[/yellow] {snippet.get('usage_count', 0)} times"
        
        console.print(Panel(header_text, border_style="blue"))
        
        # Code panel
        syntax = Syntax(
            snippet["code"],
            lang or "text",
            theme="monokai",
            line_numbers=True,
            word_wrap=True
        )
        console.print(Panel(syntax, border_style="green"))
        
        # Copy to clipboard if requested
        if args.copy:
            try:
                import pyperclip
                pyperclip.copy(snippet["code"])
                console.print("📋 Code copied to clipboard!")
            except ImportError:
                console.print("⚠️ pyperclip not installed. Install with: pip install pyperclip")
        
        return 0
    
    def cmd_edit(self, args) -> int:
        """Handle edit command."""
        snippet = self.db.get_snippet(args.id)
        
        if not snippet:
            console.print(f"❌ Snippet with ID {args.id} not found!")
            return 1
        
        console.print(Panel(f"✏️ Editing Snippet #{args.id}", style="bold yellow"))
        
        # Edit fields
        title = Prompt.ask("Title", default=snippet["title"])
        
        # Edit code in external editor if available
        code = snippet["code"]
        if os.environ.get("EDITOR"):
            if Confirm.ask("Edit code in external editor?"):
                import tempfile
                with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
                    f.write(code)
                    temp_path = f.name
                
                subprocess.call([os.environ["EDITOR"], temp_path])
                
                with open(temp_path, "r") as f:
                    code = f.read()
                os.unlink(temp_path)
        else:
            console.print("Current code:")
            console.print(Syntax(code, snippet.get("language", "text") or "text", theme="monokai"))
            if Confirm.ask("Replace code?"):
                console.print("Enter new code (Ctrl+D to finish):")
                lines = []
                try:
                    while True:
                        lines.append(input())
                except EOFError:
                    pass
                code = "\n".join(lines)
        
        language = Prompt.ask("Language", default=snippet.get("language", ""))
        description = Prompt.ask("Description", default=snippet.get("description", ""))
        tags_str = Prompt.ask("Tags (comma-separated)", default=snippet.get("tags", ""))
        
        # Update snippet
        updates = {
            "title": title,
            "code": code,
            "language": language,
            "description": description,
            "tags": tags_str
        }
        
        if self.db.update_snippet(args.id, **updates):
            console.print(f"\n✅ Snippet #{args.id} updated successfully!")
        else:
            console.print(f"\n❌ Failed to update snippet #{args.id}")
        
        return 0
    
    def cmd_delete(self, args) -> int:
        """Handle delete command."""
        snippet = self.db.get_snippet(args.id)
        
        if not snippet:
            console.print(f"❌ Snippet with ID {args.id} not found!")
            return 1
        
        console.print(Panel(
            f"[bold red]⚠️ Delete Snippet #{args.id}?[/bold red]\n\n"
            f"Title: {snippet['title']}\n"
            f"This action cannot be undone!",
            border_style="red"
        ))
        
        if args.force or Confirm.ask("Are you sure?"):
            if self.db.delete_snippet(args.id):
                console.print(f"✅ Snippet #{args.id} deleted successfully!")
            else:
                console.print(f"❌ Failed to delete snippet #{args.id}")
        else:
            console.print("❎ Deletion cancelled.")
        
        return 0
    
    def cmd_export(self, args) -> int:
        """Handle export command."""
        try:
            data = self.db.export_snippets(args.format)
            
            with open(args.file, "w") as f:
                f.write(data)
            
            console.print(f"✅ Exported to {args.file} ({args.format} format)")
            return 0
        except Exception as e:
            console.print(f"❌ Export failed: {e}")
            return 1
    
    def cmd_import(self, args) -> int:
        """Handle import command."""
        try:
            with open(args.file, "r") as f:
                data = f.read()
            
            count = self.db.import_snippets(data, args.format)
            console.print(f"✅ Imported {count} snippets from {args.file}")
            return 0
        except Exception as e:
            console.print(f"❌ Import failed: {e}")
            return 1
    
    def cmd_stats(self, args) -> int:
        """Handle stats command."""
        stats = self.db.get_stats()
        
        # Main stats panel
        stats_text = (
            f"[bold cyan]Total Snippets:[/bold cyan] {stats['total_snippets']}\n"
            f"[bold cyan]Languages:[/bold cyan] {stats['languages']}\n"
            f"[bold cyan]Total Usage:[/bold cyan] {stats['total_usage']}"
        )
        console.print(Panel(stats_text, title="📊 Statistics", border_style="blue"))
        
        # Most used snippets
        if stats["most_used"]:
            table = Table(title="🔥 Most Used Snippets", box=box.ROUNDED)
            table.add_column("ID", style="dim")
            table.add_column("Title")
            table.add_column("Usage", justify="right")
            
            for item in stats["most_used"]:
                table.add_row(str(item["id"]), item["title"], str(item["usage_count"]))
            
            console.print(table)
        
        # Recent snippets
        if stats["recent"]:
            table = Table(title="🕐 Recently Added", box=box.ROUNDED)
            table.add_column("ID", style="dim")
            table.add_column("Title")
            table.add_column("Created")
            
            for item in stats["recent"]:
                created = self._format_datetime(item["created_at"])
                table.add_row(str(item["id"]), item["title"], created)
            
            console.print(table)
        
        return 0
    
    def cmd_languages(self, args) -> int:
        """Handle languages command."""
        languages = self.db.get_languages()
        
        if not languages:
            console.print("📭 No languages found.")
            return 0
        
        table = Table(title="📚 Languages", box=box.ROUNDED)
        table.add_column("Language", style="bold")
        table.add_column("Count", justify="right")
        
        for lang, count in languages:
            color = self._get_language_color(lang)
            table.add_row(f"[{color}]{lang}[/{color}]", str(count))
        
        console.print(table)
        return 0
    
    def cmd_tags(self, args) -> int:
        """Handle tags command."""
        tags = self.db.get_tags()
        
        if not tags:
            console.print("📭 No tags found.")
            return 0
        
        table = Table(title="🏷️ Tags", box=box.ROUNDED)
        table.add_column("Tag", style="bold cyan")
        table.add_column("Count", justify="right")
        
        for tag, count in tags:
            table.add_row(tag, str(count))
        
        console.print(table)
        return 0
    
    def run_interactive(self) -> int:
        """Run interactive TUI mode."""
        console.print(Panel(
            "🚀 CodeSnippet Pro - Interactive Mode\n"
            "Type 'help' for commands, 'quit' to exit",
            border_style="blue"
        ))
        
        while True:
            try:
                command = Prompt.ask("\n[csp]").strip()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                args = parts[1:]
                
                if cmd in ("quit", "exit", "q"):
                    console.print("👋 Goodbye!")
                    break
                elif cmd == "help":
                    self._show_interactive_help()
                elif cmd == "add":
                    self.cmd_add(type("Args", (), {
                        "title": None, "code": None, "language": None,
                        "tags": None, "description": None,
                        "from_clipboard": False, "from_file": None
                    })())
                elif cmd == "list":
                    self.cmd_list(type("Args", (), {
                        "language": None, "tag": None, "limit": 50, "sort": "date"
                    })())
                elif cmd == "search":
                    self.cmd_search(type("Args", (), {
                        "query": " ".join(args) if args else "",
                        "language": None, "tag": None, "fuzzy": False
                    })())
                elif cmd == "show" and args:
                    try:
                        self.cmd_show(type("Args", (), {"id": int(args[0]), "copy": False})())
                    except ValueError:
                        console.print("❌ Invalid ID")
                elif cmd == "stats":
                    self.cmd_stats(type("Args", ())())
                else:
                    console.print(f"❓ Unknown command: {cmd}")
                    
            except KeyboardInterrupt:
                console.print("\n👋 Goodbye!")
                break
            except Exception as e:
                console.print(f"❌ Error: {e}")
        
        return 0
    
    def _show_interactive_help(self) -> None:
        """Show help for interactive mode."""
        help_text = """
[bold cyan]Available Commands:[/bold cyan]

  [green]add[/green]           Add a new snippet
  [green]list[/green]          List all snippets
  [green]search <query>[/green]  Search snippets
  [green]show <id>[/green]     Show snippet details
  [green]stats[/green]         Show statistics
  [green]help[/green]          Show this help
  [green]quit[/green]          Exit interactive mode
        """
        console.print(help_text)
