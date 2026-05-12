#!/usr/bin/env python3
"""
CodeSnippet Pro - Database Module
Handles all database operations for snippet management.
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any
from contextlib import contextmanager
import os


class SnippetDatabase:
    """SQLite database manager for code snippets."""
    
    def __init__(self, db_path: str):
        """Initialize database connection."""
        self.db_path = db_path
        self._init_db()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_db(self) -> None:
        """Initialize database schema."""
        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS snippets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    code TEXT NOT NULL,
                    language TEXT,
                    description TEXT,
                    tags TEXT,
                    hash TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 0
                );
                
                CREATE INDEX IF NOT EXISTS idx_snippets_language ON snippets(language);
                CREATE INDEX IF NOT EXISTS idx_snippets_created ON snippets(created_at);
                CREATE INDEX IF NOT EXISTS idx_snippets_title ON snippets(title);
                
                CREATE VIRTUAL TABLE IF NOT EXISTS snippets_fts USING fts5(
                    title, code, description, tags,
                    content='snippets',
                    content_rowid='id'
                );
                
                CREATE TRIGGER IF NOT EXISTS snippets_ai AFTER INSERT ON snippets BEGIN
                    INSERT INTO snippets_fts(rowid, title, code, description, tags)
                    VALUES (new.id, new.title, new.code, new.description, new.tags);
                END;
                
                CREATE TRIGGER IF NOT EXISTS snippets_ad AFTER DELETE ON snippets BEGIN
                    INSERT INTO snippets_fts(snippets_fts, rowid, title, code, description, tags)
                    VALUES ('delete', old.id, old.title, old.code, old.description, old.tags);
                END;
                
                CREATE TRIGGER IF NOT EXISTS snippets_au AFTER UPDATE ON snippets BEGIN
                    INSERT INTO snippets_fts(snippets_fts, rowid, title, code, description, tags)
                    VALUES ('delete', old.id, old.title, old.code, old.description, old.tags);
                    INSERT INTO snippets_fts(rowid, title, code, description, tags)
                    VALUES (new.id, new.title, new.code, new.description, new.tags);
                END;
            """)
    
    def _generate_hash(self, code: str) -> str:
        """Generate hash for code content."""
        return hashlib.sha256(code.encode()).hexdigest()[:16]
    
    def add_snippet(self, title: str, code: str, language: Optional[str] = None,
                   description: Optional[str] = None, tags: Optional[List[str]] = None) -> int:
        """Add a new snippet to the database."""
        code_hash = self._generate_hash(code)
        tags_str = ",".join(tags) if tags else ""
        
        with self._get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO snippets (title, code, language, description, tags, hash)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (title, code, language or "", description or "", tags_str, code_hash)
            )
            return cursor.lastrowid
    
    def get_snippet(self, snippet_id: int) -> Optional[Dict[str, Any]]:
        """Get a single snippet by ID."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM snippets WHERE id = ?",
                (snippet_id,)
            ).fetchone()
            
            if row:
                return self._row_to_dict(row)
            return None
    
    def update_snippet(self, snippet_id: int, **kwargs) -> bool:
        """Update a snippet."""
        allowed_fields = ["title", "code", "language", "description", "tags"]
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return False
        
        if "code" in updates:
            updates["hash"] = self._generate_hash(updates["code"])
        
        updates["updated_at"] = datetime.now().isoformat()
        
        set_clause = ", ".join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [snippet_id]
        
        with self._get_connection() as conn:
            cursor = conn.execute(
                f"UPDATE snippets SET {set_clause} WHERE id = ?",
                values
            )
            return cursor.rowcount > 0
    
    def delete_snippet(self, snippet_id: int) -> bool:
        """Delete a snippet."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM snippets WHERE id = ?",
                (snippet_id,)
            )
            return cursor.rowcount > 0
    
    def increment_usage(self, snippet_id: int) -> None:
        """Increment usage count for a snippet."""
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE snippets SET usage_count = usage_count + 1 WHERE id = ?",
                (snippet_id,)
            )
    
    def search_snippets(self, query: str, language: Optional[str] = None,
                       tag: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Search snippets using full-text search."""
        with self._get_connection() as conn:
            if query:
                # Use FTS for text search
                sql = """
                    SELECT s.* FROM snippets s
                    JOIN snippets_fts fts ON s.id = fts.rowid
                    WHERE snippets_fts MATCH ?
                """
                params = [query]
            else:
                sql = "SELECT * FROM snippets WHERE 1=1"
                params = []
            
            if language:
                sql += " AND language = ?"
                params.append(language)
            
            if tag:
                sql += " AND (',' || tags || ',') LIKE ?"
                params.append(f"%,{tag},%")
            
            if query:
                sql += " ORDER BY rank"
            else:
                sql += " ORDER BY created_at DESC"
            
            sql += " LIMIT ?"
            params.append(limit)
            
            rows = conn.execute(sql, params).fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def list_snippets(self, language: Optional[str] = None, tag: Optional[str] = None,
                     limit: int = 50, sort_by: str = "date") -> List[Dict[str, Any]]:
        """List snippets with optional filtering."""
        with self._get_connection() as conn:
            sql = "SELECT * FROM snippets WHERE 1=1"
            params = []
            
            if language:
                sql += " AND language = ?"
                params.append(language)
            
            if tag:
                sql += " AND (',' || tags || ',') LIKE ?"
                params.append(f"%,{tag},%")
            
            sort_map = {
                "date": "created_at DESC",
                "title": "title ASC",
                "language": "language ASC, title ASC"
            }
            sql += f" ORDER BY {sort_map.get(sort_by, 'created_at DESC')}"
            
            sql += " LIMIT ?"
            params.append(limit)
            
            rows = conn.execute(sql, params).fetchall()
            return [self._row_to_dict(row) for row in rows]
    
    def get_languages(self) -> List[Tuple[str, int]]:
        """Get list of languages with snippet counts."""
        with self._get_connection() as conn:
            rows = conn.execute(
                """SELECT language, COUNT(*) as count 
                   FROM snippets 
                   WHERE language != '' 
                   GROUP BY language 
                   ORDER BY count DESC"""
            ).fetchall()
            return [(row["language"], row["count"]) for row in rows]
    
    def get_tags(self) -> List[Tuple[str, int]]:
        """Get list of all tags with counts."""
        with self._get_connection() as conn:
            rows = conn.execute("SELECT tags FROM snippets WHERE tags != ''").fetchall()
            
            tag_counts = {}
            for row in rows:
                for tag in row["tags"].split(","):
                    tag = tag.strip()
                    if tag:
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            return sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        with self._get_connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM snippets").fetchone()[0]
            
            languages = conn.execute(
                "SELECT COUNT(DISTINCT language) FROM snippets WHERE language != ''"
            ).fetchone()[0]
            
            total_usage = conn.execute(
                "SELECT COALESCE(SUM(usage_count), 0) FROM snippets"
            ).fetchone()[0]
            
            most_used = conn.execute(
                """SELECT id, title, usage_count FROM snippets 
                   ORDER BY usage_count DESC LIMIT 5"""
            ).fetchall()
            
            recent = conn.execute(
                """SELECT id, title, created_at FROM snippets 
                   ORDER BY created_at DESC LIMIT 5"""
            ).fetchall()
            
            return {
                "total_snippets": total,
                "languages": languages,
                "total_usage": total_usage,
                "most_used": [dict(row) for row in most_used],
                "recent": [dict(row) for row in recent]
            }
    
    def export_snippets(self, format_type: str = "json") -> str:
        """Export all snippets to string."""
        snippets = self.list_snippets(limit=10000)
        
        if format_type == "json":
            return json.dumps(snippets, indent=2, default=str)
        elif format_type == "csv":
            import csv
            import io
            
            if not snippets:
                return ""
            
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=snippets[0].keys())
            writer.writeheader()
            writer.writerows(snippets)
            return output.getvalue()
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def import_snippets(self, data: str, format_type: str = "json") -> int:
        """Import snippets from string."""
        count = 0
        
        if format_type == "json":
            snippets = json.loads(data)
            for snippet in snippets:
                try:
                    tags = snippet.get("tags", "")
                    if isinstance(tags, str):
                        tags = [t.strip() for t in tags.split(",") if t.strip()]
                    
                    self.add_snippet(
                        title=snippet["title"],
                        code=snippet["code"],
                        language=snippet.get("language", ""),
                        description=snippet.get("description", ""),
                        tags=tags
                    )
                    count += 1
                except Exception:
                    continue
        elif format_type == "csv":
            import csv
            import io
            
            reader = csv.DictReader(io.StringIO(data))
            for row in reader:
                try:
                    tags = row.get("tags", "")
                    if isinstance(tags, str):
                        tags = [t.strip() for t in tags.split(",") if t.strip()]
                    
                    self.add_snippet(
                        title=row["title"],
                        code=row["code"],
                        language=row.get("language", ""),
                        description=row.get("description", ""),
                        tags=tags
                    )
                    count += 1
                except Exception:
                    continue
        
        return count
    
    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert database row to dictionary."""
        result = dict(row)
        if result.get("tags"):
            result["tags_list"] = [t.strip() for t in result["tags"].split(",") if t.strip()]
        else:
            result["tags_list"] = []
        return result
