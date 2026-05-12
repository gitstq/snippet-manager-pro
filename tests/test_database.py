#!/usr/bin/env python3
"""Tests for database module."""

import os
import tempfile
import unittest
from codesnippet_pro.database import SnippetDatabase


class TestSnippetDatabase(unittest.TestCase):
    """Test cases for SnippetDatabase."""
    
    def setUp(self):
        """Set up test database."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        self.db = SnippetDatabase(self.db_path)
    
    def tearDown(self):
        """Clean up test database."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)
    
    def test_add_snippet(self):
        """Test adding a snippet."""
        snippet_id = self.db.add_snippet(
            title="Test Snippet",
            code="print('hello')",
            language="python",
            description="A test snippet",
            tags=["test", "python"]
        )
        
        self.assertIsInstance(snippet_id, int)
        self.assertGreater(snippet_id, 0)
    
    def test_get_snippet(self):
        """Test retrieving a snippet."""
        snippet_id = self.db.add_snippet(
            title="Test Snippet",
            code="print('hello')",
            language="python"
        )
        
        snippet = self.db.get_snippet(snippet_id)
        
        self.assertIsNotNone(snippet)
        self.assertEqual(snippet["title"], "Test Snippet")
        self.assertEqual(snippet["code"], "print('hello')")
        self.assertEqual(snippet["language"], "python")
    
    def test_get_nonexistent_snippet(self):
        """Test retrieving a non-existent snippet."""
        snippet = self.db.get_snippet(99999)
        self.assertIsNone(snippet)
    
    def test_update_snippet(self):
        """Test updating a snippet."""
        snippet_id = self.db.add_snippet(
            title="Original Title",
            code="original code"
        )
        
        result = self.db.update_snippet(
            snippet_id,
            title="Updated Title",
            code="updated code"
        )
        
        self.assertTrue(result)
        
        snippet = self.db.get_snippet(snippet_id)
        self.assertEqual(snippet["title"], "Updated Title")
        self.assertEqual(snippet["code"], "updated code")
    
    def test_delete_snippet(self):
        """Test deleting a snippet."""
        snippet_id = self.db.add_snippet(
            title="To Delete",
            code="delete me"
        )
        
        result = self.db.delete_snippet(snippet_id)
        self.assertTrue(result)
        
        snippet = self.db.get_snippet(snippet_id)
        self.assertIsNone(snippet)
    
    def test_search_snippets(self):
        """Test searching snippets."""
        self.db.add_snippet(
            title="Python Hello",
            code="print('hello')",
            language="python",
            tags=["beginner"]
        )
        
        self.db.add_snippet(
            title="JavaScript Alert",
            code="alert('hello')",
            language="javascript",
            tags=["web"]
        )
        
        # Search by query
        results = self.db.search_snippets("hello")
        self.assertEqual(len(results), 2)
        
        # Search by language
        results = self.db.search_snippets("", language="python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["language"], "python")
        
        # Search by tag
        results = self.db.search_snippets("", tag="web")
        self.assertEqual(len(results), 1)
    
    def test_list_snippets(self):
        """Test listing snippets."""
        self.db.add_snippet(title="Snippet 1", code="code1", language="python")
        self.db.add_snippet(title="Snippet 2", code="code2", language="javascript")
        self.db.add_snippet(title="Snippet 3", code="code3", language="python")
        
        # List all
        results = self.db.list_snippets()
        self.assertEqual(len(results), 3)
        
        # List by language
        results = self.db.list_snippets(language="python")
        self.assertEqual(len(results), 2)
    
    def test_get_languages(self):
        """Test getting language statistics."""
        self.db.add_snippet(title="S1", code="c1", language="python")
        self.db.add_snippet(title="S2", code="c2", language="python")
        self.db.add_snippet(title="S3", code="c3", language="javascript")
        
        languages = self.db.get_languages()
        
        self.assertEqual(len(languages), 2)
        # Should be sorted by count
        self.assertEqual(languages[0], ("python", 2))
        self.assertEqual(languages[1], ("javascript", 1))
    
    def test_get_tags(self):
        """Test getting tag statistics."""
        self.db.add_snippet(title="S1", code="c1", tags=["web", "python"])
        self.db.add_snippet(title="S2", code="c2", tags=["web", "javascript"])
        
        tags = self.db.get_tags()
        
        self.assertEqual(len(tags), 3)
        # web should have count 2
        web_tag = next((t for t in tags if t[0] == "web"), None)
        self.assertIsNotNone(web_tag)
        self.assertEqual(web_tag[1], 2)
    
    def test_increment_usage(self):
        """Test incrementing usage count."""
        snippet_id = self.db.add_snippet(title="Test", code="code")
        
        self.db.increment_usage(snippet_id)
        self.db.increment_usage(snippet_id)
        
        snippet = self.db.get_snippet(snippet_id)
        self.assertEqual(snippet["usage_count"], 2)
    
    def test_export_import_json(self):
        """Test JSON export and import."""
        self.db.add_snippet(
            title="Test Snippet",
            code="print('test')",
            language="python",
            description="A test",
            tags=["test"]
        )
        
        # Export
        json_data = self.db.export_snippets("json")
        self.assertIn("Test Snippet", json_data)
        
        # Create new database and import
        db2_path = os.path.join(self.temp_dir, "test2.db")
        db2 = SnippetDatabase(db2_path)
        
        count = db2.import_snippets(json_data, "json")
        self.assertEqual(count, 1)
        
        # Verify import
        snippets = db2.list_snippets()
        self.assertEqual(len(snippets), 1)
        self.assertEqual(snippets[0]["title"], "Test Snippet")
        
        os.remove(db2_path)
    
    def test_get_stats(self):
        """Test getting statistics."""
        self.db.add_snippet(title="S1", code="c1", language="python")
        self.db.add_snippet(title="S2", code="c2", language="javascript")
        
        self.db.increment_usage(1)
        self.db.increment_usage(1)
        self.db.increment_usage(2)
        
        stats = self.db.get_stats()
        
        self.assertEqual(stats["total_snippets"], 2)
        self.assertEqual(stats["languages"], 2)
        self.assertEqual(stats["total_usage"], 3)


if __name__ == "__main__":
    unittest.main()
