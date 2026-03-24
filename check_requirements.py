#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CareerCatalyst - Dependency Verification Script
Copyright (c) 2025-present Martin Mei
"""

import sys
import subprocess
import importlib.metadata
from typing import Dict, List, Tuple
import platform

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Disable colors if not in terminal
if not sys.stdout.isatty():
    for attr in dir(Colors):
        if not attr.startswith('__'):
            setattr(Colors, attr, '')

# Required packages with minimum versions
REQUIRED_PACKAGES = {
    # Core AI/ML Framework
    'langchain': '0.1.0',
    'langchain-community': '0.0.10',
    'langchain-chroma': '0.1.0',
    'langchain-ollama': '0.1.0',
    'langchain-text-splitters': '0.1.0',
    
    # Web Interface
    'streamlit': '1.29.0',
    
    # API Gateway
    'fastapi': '0.104.1',
    'uvicorn': '0.24.0',
    'pydantic': '2.5.0',
    
    # Document Processing
    'pypdf2': '3.0.1',
    'pdfplumber': '0.10.3',
    'python-docx': '1.1.0',
    'pandas': '2.1.3',
    'openpyxl': '3.1.2',
    'python-pptx': '0.6.22',
    
    # Telegram Bot
    'python-telegram-bot': '20.6',
    
    # Vector Database
    'chromadb': '0.4.22',
    'sentence-transformers': '2.2.2',
    
    # Utilities
    'requests': '2.31.0',
    'python-dotenv': '1.0.0',
    'tqdm': '4.66.1',
}

def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}  {text}{Colors.ENDC}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}    {text}{Colors.ENDC}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}  {text}{Colors.ENDC}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}   {text}{Colors.ENDC}")

def check_python_version() -> bool:
    """Check if Python version is 3.9 or higher"""
    print_header("Checking Python Version")
    
    current_version = sys.version_info
    required_version = (3, 9)
    
    print(f"Current Python version: {sys.version}")
    
    if current_version.major == required_version[0] and current_version.minor >= required_version[1]:
        print_success(f"Python {current_version.major}.{current_version.minor}.{current_version.micro} is compatible")
        return True
    elif current_version.major > required_version[0]:
        print_success(f"Python {current_version.major}.{current_version.minor}.{current_version.micro} is compatible")
        return True
    else:
        print_error(f"Python {required_version[0]}.{required_version[1]}+ is required")
        return False

def check_package_installed(package_name: str, min_version: str = None) -> Tuple[bool, str]:
    """Check if a package is installed and meets minimum version"""
    try:
        # Handle package name mapping for import
        import_name = package_name.replace('-', '_')
        
        # Special cases for package names
        special_cases = {
            'pypdf2': 'PyPDF2',
            'python-docx': 'docx',
            'python-pptx': 'pptx',
            'python-telegram-bot': 'telegram',
            'python-dotenv': 'dotenv',
        }
        
        if package_name in special_cases:
            import_name = special_cases[package_name]
        
        # Try to get version using importlib.metadata
        try:
            version = importlib.metadata.version(package_name)
        except importlib.metadata.PackageNotFoundError:
            # Fallback to importing the module
            module = __import__(import_name)
            version = getattr(module, '__version__', 'unknown')
        
        if min_version:
            from packaging import version as version_parser
            if version_parser.parse(version) >= version_parser.parse(min_version):
                return True, version
            else:
                return False, version
        else:
            return True, version
            
    except (ImportError, importlib.metadata.PackageNotFoundError) as e:
        return False, None
    except Exception as e:
        return False, str(e)

def check_required_packages() -> Dict[str, bool]:
    """Check all required packages"""
    print_header("Checking Required Packages")
    
    results = {}
    all_passed = True
    
    for package, min_version in REQUIRED_PACKAGES.items():
        installed, version = check_package_installed(package, min_version)
        
        if installed:
            print_success(f"{package:<30} version {version} (required >= {min_version})")
            results[package] = True
        else:
            if version:
                print_error(f"{package:<30} version {version} (required >= {min_version})")
            else:
                print_error(f"{package:<30} NOT INSTALLED (required >= {min_version})")
            results[package] = False
            all_passed = False
    
    return results

def check_optional_packages():
    """Check optional packages"""
    print_header("Checking Optional Packages")
    
    for package, description in OPTIONAL_PACKAGES.items():
        installed, version = check_package_installed(package)
        
        if installed:
            print_success(f"{package:<30} version {version} - {description}")
        else:
            print_info(f"{package:<30} not installed - {description}")

def check_ollama() -> bool:
    """Check if Ollama is running"""
    print_header("Checking Ollama")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                print_success(f"Ollama is running with {len(models)} model(s):")
                for model in models:
                    print(f"   - {model.get('name')}")
            else:
                print_warning("Ollama is running but no models found")
                print_info("Run 'ollama pull llama3' to download a model")
            return True
        else:
            print_error(f"Ollama returned unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to Ollama. Is it running?")
        print_info("Start Ollama with: ollama serve")
        return False
    except Exception as e:
        print_error(f"Error checking Ollama: {e}")
        return False

def check_chromadb() -> bool:
    """Check if ChromaDB is accessible"""
    print_header("Checking ChromaDB")
    
    try:
        import chromadb
        print_success(f"ChromaDB version {chromadb.__version__} is installed")
        
        # Try to create a test client
        client = chromadb.Client()
        print_success("ChromaDB client initialized successfully")
        return True
        
    except ImportError:
        print_error("ChromaDB not installed")
        return False
    except Exception as e:
        print_warning(f"ChromaDB client test failed: {e}")
        return True  # Still return True as it's installed

def check_directories():
    """Check required directories"""
    print_header("Checking Directories")
    
    import os
    
    required_dirs = ['company_data', 'chroma_db_company']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            if os.path.isdir(dir_name):
                # Check if directory is empty
                if os.listdir(dir_name):
                    print_success(f"Directory '{dir_name}' exists and contains files")
                else:
                    print_warning(f"Directory '{dir_name}' exists but is empty")
            else:
                print_error(f"'{dir_name}' exists but is not a directory")
        else:
            if dir_name == 'company_data':
                print_warning(f"Directory '{dir_name}' does not exist")
                print_info("Create it with: mkdir company_data")
            else:
                print_info(f"Directory '{dir_name}' will be created when running rag_setup.py")

def check_system_info():
    """Display system information"""
    print_header("System Information")
    
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Executable: {sys.executable}")

def print_summary(package_results: Dict[str, bool]):
    """Print installation summary"""
    print_header("Summary")
    
    total_packages = len(package_results)
    passed_packages = sum(1 for v in package_results.values() if v)
    
    print(f"Packages checked: {total_packages}")
    print(f"Passed: {passed_packages}")
    print(f"Failed: {total_packages - passed_packages}")
    
    if passed_packages == total_packages:
        print(f"\n{Colors.BOLD}{Colors.GREEN}  All requirements satisfied!{Colors.ENDC}")
        print(f"\n{Colors.BOLD}Next steps:{Colors.ENDC}")
        print("1. Ensure Ollama is running: ollama serve")
        print("2. Place company documents in ./company_data/")
        print("3. Run: python rag_setup.py")
        print("4. Start the services:")
        print("   - API Gateway: python -m uvicorn api_gateway:app --reload --port 8000")
        print("   - Web Interface: streamlit run web_app.py")
        print("   - Telegram Bot: python telegram_bot.py")
    else:
        print(f"\n{Colors.BOLD}{Colors.RED}  Some requirements are missing.{Colors.ENDC}")
        print(f"\n{Colors.BOLD}To install missing packages:{Colors.ENDC}")
        print("pip install -r requirements.txt")
        
        # Show missing packages
        missing = [pkg for pkg, installed in package_results.items() if not installed]
        if missing:
            print(f"\nMissing packages: {', '.join(missing)}")

def main():
    """Main function"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}  CareerCatalyst - Dependency Verification{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}This script will check if your system is ready to run CareerCatalyst{Colors.ENDC}\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Display system info
    check_system_info()
    
    # Check required packages
    package_results = check_required_packages()
    
    # Check optional packages
    check_optional_packages()
    
    # Check directories
    check_directories()
    
    # Check Ollama
    ollama_ok = check_ollama()
    
    # Check ChromaDB
    chromadb_ok = check_chromadb()
    
    # Print summary
    print_summary(package_results)
    
    # Exit with appropriate code
    all_packages_ok = all(package_results.values())
    if not all_packages_ok:
        sys.exit(1)
    if not ollama_ok:
        print_warning("\nOllama is not running, but packages are installed.")
        print_info("You can still proceed, but Ollama needs to be running for the application to work.")
        sys.exit(0)
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}  System is ready to run CareerCatalyst!{Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}   Check interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)