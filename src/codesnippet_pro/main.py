#!/usr/bin/env python3
"""
CodeSnippet Pro - Main Entry Point
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codesnippet_pro.cli import main

if __name__ == "__main__":
    sys.exit(main())
