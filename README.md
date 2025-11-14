# XSS Payload Generator

CLI XSS payload generator. Retrieve XSS payloads by tags and events. Can add encoding on top.

Use PortSwigger's 10k+ XSS payloads as a default source (a custom payload list can be provided).

## Quick Start

```bash
git clone https://github.com/fineko/xss-payload-generator.git
cd xss-payload-generator
```

## Installation

### Option 1: Run directly (no installation)

```bash
./xssgen.py -t svg -e onload
```

### Option 2: Install globally

```bash
./install.sh
```

Then use from anywhere:

```bash
xssgen -t svg -e onload
```

### Uninstall

```bash
sudo rm /usr/local/bin/xssgen
sudo rm -r /usr/share/xssgen
```

## Usage

```bash
# Generate by tag
xssgen -t svg

# Generate by tag AND event
xssgen -t svg -e onload

# Multiple tags together
xssgen -t button -t xmp -l 10

# Encode output
xssgen -t img -e onerror --encode url

# Raw output (for piping)
xssgen -t svg --raw

# Show statistics
xssgen --stats

# Save to file
xssgen -t iframe -o payloads.txt
```

## Note

**Custom tags:** In PortSwigger's payload list, custom HTML tags are named `xss`. To find payloads with custom tags, use:

```bash
xssgen -t xss
```

## Examples

### Find SVG tag with onload event

```bash
xssgen -t svg -e onload
```

### URL-encode payloads

```bash
xssgen -t img -e onerror --encode url -l 5
```

### Combine and exclude elements

```bash
xssgen -t button -t div --exclude-event onclick
```

### Pipe to other tools

```bash
xssgen -t svg --raw | ffuf -w - -u https://target.com/?q=FUZZ
```

## Features

- Generate by tags & events (AND logic)
- Syntax highlighting
- Multiple encodings (URL, base64, hex, HTML)
- Payload statistics
- Single file, no dependencies

## Requirements

- Python 3.8+
- No external dependencies

## Reference

Complete lists of HTML tags and events are available in the `lists/` directory:
- `lists/html_tags.txt` - All HTML tags
- `lists/html_events.txt` - All HTML event handlers

## Credits

Payloads from [PortSwigger XSS Cheat Sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)
