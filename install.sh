#!/bin/bash

# XSSfilter Installer (Linux)

set -e

echo "Installing XSSfilter..."

# Check if already installed
if command -v xssfilter &>/dev/null; then
  echo "xssfilter is already installed!"
  echo "To reinstall, run:"
  echo "  sudo rm /usr/local/bin/xssfilter"
  echo "Then run this script again."
  exit 0
fi

# Check Python 3
if ! command -v python3 &>/dev/null; then
  echo "Python 3 is required. Please install Python 3 first."
  exit 1
fi

# Create directories
echo "Creating directories..."
sudo mkdir -p /usr/share/xssfilter
sudo mkdir -p /usr/local/bin

# Copy data files
echo "Installing data files..."
sudo cp xss_payloads.txt /usr/share/xssfilter/
sudo chmod 644 /usr/share/xssfilter/xss_payloads.txt

# Copy and rename executable (xssfilter.py -> xssfilter)
echo "Installing executable..."
sudo cp xssfilter.py /usr/local/bin/xssfilter
sudo chmod +x /usr/local/bin/xssfilter

# Update the script to use system path
sudo sed -i 's|script_dir = Path(__file__).parent|script_dir = Path("/usr/share/xssfilter")|' /usr/local/bin/xssfilter

echo "Installation complete!"

# Test installation
if command -v xssfilter &>/dev/null; then
  echo ""
  echo "Testing installation..."
  if xssfilter --stats &>/dev/null; then
    echo "XSSfilter is ready to use."
  else
    echo "Installation may have issues. Check permissions."
  fi
else
  echo "xssfilter not found in PATH. Try: source ~/.bashrc or ~/.zshrc"
fi

echo ""
echo "To uninstall:"
echo "  sudo rm /usr/local/bin/xssfilter"
echo "  sudo rm -r /usr/share/xssfilter"
