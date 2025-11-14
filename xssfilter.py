#!/usr/bin/env python3
"""
XSSfilter - Quick XSS payload filter
Author: fineko
"""

import sys
import re
import argparse
import urllib.parse
import base64
from pathlib import Path
from collections import Counter

# ANSI colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'

def get_data_file():
    """Get xss_payloads.txt path"""
    script_dir = Path(__file__).parent
    return script_dir / 'xss_payloads.txt'

def parse_payload(payload):
    """Extract tags and events from payload"""
    tags = set(re.findall(r'<(\w+)[\s/>]', payload, re.I))
    events = set(re.findall(r'\b(on\w+)\s*=', payload, re.I))
    return tags, events

def load_payloads(file_path):
    """Load all payloads from file"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def filter_payloads(payloads, tags=None, events=None, exclude_tags=None, exclude_events=None):
    """Filter payloads by tags and events"""
    results = []
    
    for payload in payloads:
        p_tags, p_events = parse_payload(payload)
        
        # Check tags (AND logic)
        if tags:
            if not all(any(t.lower() == pt.lower() for pt in p_tags) for t in tags):
                continue
        
        # Check events (AND logic)
        if events:
            if not all(any(e.lower() == pe.lower() for pe in p_events) for e in events):
                continue
        
        # Exclude tags
        if exclude_tags:
            if any(any(t.lower() == pt.lower() for pt in p_tags) for t in exclude_tags):
                continue
        
        # Exclude events
        if exclude_events:
            if any(any(e.lower() == pe.lower() for pe in p_events) for e in exclude_events):
                continue
        
        results.append((payload, p_tags, p_events))
    
    return results

def highlight_payload(payload, search_tags=None, search_events=None):
    """Add color highlighting to payload"""
    # Convert search terms to lowercase sets for comparison
    search_tags_lower = set(t.lower() for t in search_tags) if search_tags else set()
    search_events_lower = set(e.lower() for e in search_events) if search_events else set()
    
    # Parse to find all tags and events in this payload
    all_tags = re.findall(r'<(\w+)', payload, re.I)
    all_events = re.findall(r'\b(on\w+)\s*=', payload, re.I)
    
    text = payload
    
    # First pass: highlight searched items in BOLD
    if search_tags_lower:
        for tag_match in re.finditer(r'<(\w+)', text, re.I):
            tag = tag_match.group(1)
            if tag.lower() in search_tags_lower:
                # Opening tag
                old = tag_match.group(0)
                new = f'{BOLD}{CYAN}{old}{RESET}'
                text = text.replace(old, new, 1)
        
        # Closing tags
        for tag in search_tags_lower:
            text = re.sub(f'(</{tag}>)', f'{BOLD}{CYAN}\\1{RESET}', text, flags=re.I)
    
    if search_events_lower:
        for event_match in re.finditer(r'\b(on\w+)\s*=', text, re.I):
            event = event_match.group(1)
            if event.lower() in search_events_lower:
                old = event
                new = f'{BOLD}{GREEN}{old}{RESET}'
                text = text[:event_match.start(1)] + new + text[event_match.end(1):]
    
    # Second pass: highlight all other tags/events in normal color
    # Tags (not already bolded)
    text = re.sub(r'<(\w+)', lambda m: f'{CYAN}<{m.group(1)}{RESET}' if BOLD not in text[max(0,m.start()-10):m.start()] else m.group(0), text)
    text = re.sub(r'</(\w+)>', lambda m: f'{CYAN}</{m.group(1)}>{RESET}' if BOLD not in text[max(0,m.start()-10):m.start()] else m.group(0), text)
    
    # Events (not already bolded)
    text = re.sub(r'\b(on\w+)=', lambda m: f'{GREEN}{m.group(1)}{RESET}=' if BOLD not in text[max(0,m.start()-10):m.start()] else m.group(0), text, flags=re.I)
    
    # Tag closing >
    text = re.sub(r'>', f'{CYAN}>{RESET}', text)
    
    return text

def encode_payload(payload, encoding):
    """Encode payload"""
    if encoding == 'url':
        return urllib.parse.quote(payload, safe='')
    elif encoding == 'url2':
        return urllib.parse.quote(urllib.parse.quote(payload, safe=''), safe='')
    elif encoding == 'base64':
        return base64.b64encode(payload.encode()).decode()
    elif encoding == 'hex':
        return ''.join(f'\\x{ord(c):02x}' for c in payload)
    elif encoding == 'html':
        return ''.join(f'&#{ord(c)};' for c in payload)
    return payload

def show_stats(payloads):
    """Show payload statistics"""
    all_tags = []
    all_events = []
    
    for payload in payloads:
        tags, events = parse_payload(payload)
        all_tags.extend(tags)
        all_events.extend(events)
    
    tag_counts = Counter(all_tags)
    event_counts = Counter(all_events)
    
    print(f"\n{BOLD}{CYAN}XSS Payload Statistics{RESET}\n")
    print(f"{BOLD}Total payloads:{RESET} {YELLOW}{len(payloads)}{RESET}")
    print(f"{BOLD}Unique tags:{RESET} {YELLOW}{len(tag_counts)}{RESET}")
    print(f"{BOLD}Unique events:{RESET} {YELLOW}{len(event_counts)}{RESET}\n")
    
    print(f"{BOLD}Top 5 Tags:{RESET}")
    for tag, count in tag_counts.most_common(5):
        tag_display = tag[:20]
        print(f"  {CYAN}{tag_display:<20}{RESET} {count:>5}")
    
    print(f"\n{BOLD}Top 5 Events:{RESET}")
    for event, count in event_counts.most_common(5):
        event_display = event[:30]
        print(f"  {GREEN}{event_display:<30}{RESET} {count:>5}")
    print()

def main():
    parser = argparse.ArgumentParser(
        prog='xssfilter',
        description='XSSfilter - XSS payload filter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  xssfilter -t svg -e onload
  xssfilter -t img -e onerror --encode url
  xssfilter -t button -t xmp -l 10
  xssfilter --stats
  xssfilter -t svg --raw
        """,
        add_help=False
    )
    
    # Main options
    main_group = parser.add_argument_group('Main options')
    main_group.add_argument('-h', '--help', action='help', help='show this help')
    main_group.add_argument('-t', '--tag', action='append', metavar='TAG', help='filter by tag)')
    main_group.add_argument('-e', '--event', action='append', metavar='EVENT', help='filter by event')
    main_group.add_argument('-l', '--limit', type=int, metavar='N', help='limit results')
    main_group.add_argument('-o', '--output', metavar='FILE', help='output file')
    
    # Advanced options
    adv_group = parser.add_argument_group('Advanced options')
    adv_group.add_argument('-xt', '--exclude-tag', action='append', metavar='TAG', help='exclude tag')
    adv_group.add_argument('-xe', '--exclude-event', action='append', metavar='EVENT', help='exclude event')
    adv_group.add_argument('-ec', '--encode', choices=['url', 'url2', 'base64', 'hex', 'html'], help='encode output')
    adv_group.add_argument('-r', '--raw', action='store_true', help='raw output (no colors)')
    adv_group.add_argument('-s', '--stats', action='store_true', help='show statistics')
    adv_group.add_argument('-f', '--file', metavar='FILE', help='custom payload file')
    
    args = parser.parse_args()
    
    # Get payload file
    payload_file = Path(args.file) if args.file else get_data_file()
    
    if not payload_file.exists():
        print(f"Error: Payload file not found: {payload_file}", file=sys.stderr)
        sys.exit(1)
    
    # Load payloads
    payloads = load_payloads(payload_file)
    
    # Show stats if no filters or --stats flag
    if args.stats or not any([args.tag, args.event, args.exclude_tag, args.exclude_event]):
        show_stats(payloads)
        return
    
    # Filter payloads
    results = filter_payloads(
        payloads,
        tags=args.tag,
        events=args.event,
        exclude_tags=args.exclude_tag,
        exclude_events=args.exclude_event
    )
    
    # Limit results
    if args.limit:
        results = results[:args.limit]
    
    if not results:
        if not args.raw:
            print(f"{YELLOW}No payloads found{RESET}", file=sys.stderr)
        sys.exit(0)
    
    # Output
    output_lines = []
    for payload, tags, events in results:
        # Encode if requested
        if args.encode:
            output_text = encode_payload(payload, args.encode)
        else:
            output_text = payload
        
        # Add highlighting if not raw
        if not args.raw and not args.encode:
            output_text = highlight_payload(output_text, args.tag, args.event)
        
        output_lines.append(output_text)
    
    # Write output
    output_text = '\n'.join(output_lines)
    
    if args.output:
        Path(args.output).write_text(output_text + '\n', encoding='utf-8')
        if not args.raw:
            print(f"{GREEN}✓{RESET} Saved {len(results)} payloads to {args.output}")
    else:
        print(output_text)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Interrupted{RESET}", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"{BOLD}Error:{RESET} {e}", file=sys.stderr)
        sys.exit(1)
