"""
config.py
Configuration module for the Universal Encoder & Decoder Toolkit.
Holds constants, directory paths, and search configurations.
"""

import os
from pathlib import Path
from typing import Dict, List, Any

# Root directory of the application
APP_DIR = Path(__file__).resolve().parent

# Output directories
OUTPUT_DIR = APP_DIR / "output"
EXPORTS_DIR = OUTPUT_DIR / "exports"
LOGS_DIR = OUTPUT_DIR / "logs"

# Create output directories if they do not exist
for directory in [EXPORTS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Application Metadata
APP_NAME = "Universal Encoder & Decoder Toolkit"
VERSION = "1.0.0"
AUTHOR = "Antigravity Pair"
GITHUB_LINK = "https://github.com/universal-encoder-decoder"

# Logo and Icon paths
LOGO_PATH = str(APP_DIR / "assets" / "logo.png")
ICON_PATH = str(APP_DIR / "assets" / "icon.png")

# Page configurations
PAGE_CONFIG = {
    "page_title": "Universal Encoder & Decoder Toolkit",
    "page_icon": "🔒",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Categorized Tools registry for search and dynamic routing
TOOL_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "General": {
        "icon": "🏠",
        "tools": {
            "Home": "pages.home",
            "About": "pages.about",
            "Compare Outputs": "pages.compare",
        }
    },
    "Encoders / Decoders": {
        "icon": "🔄",
        "tools": {
            "String Encoder": "pages.encoder",
            "String Decoder": "pages.decoder",
            "Auto Detect Format": "pages.auto_detect",
        }
    },
    "Specialized Formats": {
        "icon": "⚙️",
        "tools": {
            "Binary Tools": "pages.binary_tools",
            "Text & Unicode Converter": "pages.text_converter",
            "Unicode Tools": "pages.unicode_tools",
            "URL Tools": "pages.url_tools",
        }
    },
    "Cryptography & Hashes": {
        "icon": "🔑",
        "tools": {
            "Crypto Tools": "pages.crypto_tools",
            "Hash Tools": "pages.hash_tools",
            "JWT Tools": "pages.jwt_tools",
        }
    },
    "Utilities": {
        "icon": "🛠️",
        "tools": {
            "File Encoder/Decoder": "pages.file_encoder",
            "QR Tools": "pages.qr_tools",
            "Password Generator": "pages.password_generator",
        }
    }
}
