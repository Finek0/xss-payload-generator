# XSSfilter

Quick XSS payload filter. Filter PortSwigger's 10k+ XSS payloads (or any XSS payload list) by tags and events.

## Quick Start

```bash
git clone https://github.com/fineko/xss-filter.git
cd xss-filter
```

## Installation

### Option 1: Run directly (no installation)

```bash
./xssfilter.py -t svg -e onload
```

### Option 2: Install globally

```bash
./install.sh
```

Then use from anywhere:

```bash
xssfilter -t svg -e onload
```

### Uninstall

```bash
sudo rm /usr/local/bin/xssfilter
sudo rm -r /usr/share/xssfilter
```

## Usage

```bash
# Filter by tag
xssfilter -t svg

# Filter by tag AND event
xssfilter -t svg -e onload

# Multiple tags together
xssfilter -t button -t xmp -l 10

# Encode output
xssfilter -t img -e onerror --encode url

# Raw output (for piping)
xssfilter -t svg --raw

# Show statistics
xssfilter --stats

# Save to file
xssfilter -t iframe -o payloads.txt
```

## Note

**Custom tags:** In PortSwigger's payload list, custom HTML tags are named `xss`. To find payloads with custom tags, use:

```bash
xssfilter -t xss
```

## Examples

### Find SVG tag with onload event

```bash
xssfilter -t svg -e onload
```

### URL-encode payloads

```bash
xssfilter -t img -e onerror --encode url -l 5
```

### Combine and exclude tags

```bash
xssfilter -t button -t div --exclude-event onclick
```

### Pipe to other tools

```bash
xssfilter -t svg --raw | ffuf -w - -u https://target.com/?q=FUZZ
```

## Features

- Filter by tags & events (AND logic)
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
