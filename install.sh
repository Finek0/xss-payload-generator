#!/bin/bash

# XSS Payload Generator Installer (Linux)

set -e

echo "Installing xssgen ..."

# Check if already installed
if command -v xssgen &>/dev/null; then
  echo "xssgen is already installed!"
  echo "To reinstall, run:"
  echo "  sudo rm /usr/local/bin/xssgen"
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
sudo mkdir -p /usr/share/xssgen
sudo mkdir -p /usr/local/bin

# Copy data files
echo "Installing data files..."
sudo cp xss_payloads.txt /usr/share/xssgen/
sudo chmod 644 /usr/share/xssgen/xss_payloads.txt

# Copy and rename executable (xssgen.py -> xssgen)
echo "Installing executable..."
sudo cp xssgen.py /usr/local/bin/xssgen
sudo chmod +x /usr/local/bin/xssgen

# Update the script to use system path
sudo sed -i 's|script_dir = Path(__file__).parent|script_dir = Path("/usr/share/xssgen")|' /usr/local/bin/xssgen

echo "Installation complete!"

# Test installation
if command -v xssgen &>/dev/null; then
  echo ""
  echo "Testing installation..."
  if xssgen --stats &>/dev/null; then
    echo "xssgen is ready to use."
  else
    echo "Installation may have issues. Check permissions."
  fi
else
  echo "xssgen not found in PATH. Try: source ~/.bashrc or ~/.zshrc"
fi

echo ""
echo "To uninstall:"
echo "  sudo rm /usr/local/bin/xssgen"
echo "  sudo rm -r /usr/share/xssgen"
