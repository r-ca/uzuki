#!/usr/bin/env python3
"""
シーケンス管理システムのテスト
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uzuki.app import main

if __name__ == '__main__':
    main() 