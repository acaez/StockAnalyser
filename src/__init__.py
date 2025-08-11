"""
StockAnalyser Package to initialize the stock analysis tool
"""

__version__ = "1.0.0"
__author__ = "caze"

import sys
from pathlib import Path

src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
