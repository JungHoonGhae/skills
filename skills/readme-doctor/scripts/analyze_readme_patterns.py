#!/usr/bin/env python3
"""
README Pattern Analyzer

Analyzes multiple README files to extract common patterns in structure and style.

Usage:
    python3 analyze_readme_patterns.py readme1.md readme2.md readme3.md

Output:
    JSON with detected patterns including sections, styles, and recommended order.
"""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


# Standard section name normalizations
SECTION_ALIASES = {
    'install': 'Installation',
    'installation': 'Installation',
    'getting started': 'Installation',
    'quick start': 'Installation',
    'setup': 'Installation',
    'usage': 'Usage',
    'how to use': 'Usage',
    'example': 'Examples',
    'examples': 'Examples',
    'demo': 'Examples',
    'quickstart': 'Installation',
    'intro': 'Introduction',
    'introduction': 'Introduction',
    'overview': 'Introduction',
    'about': 'Introduction',
    'features': 'Features',
    'feature': 'Features',
    'what it does': 'Features',
    'api': 'API',
    'api reference': 'API',
    'documentation': 'API',
    'docs': 'API',
    'config': 'Configuration',
    'configuration': 'Configuration',
    'settings': 'Configuration',
    'options': 'Configuration',
    'contributing': 'Contributing',
    'contribute': 'Contributing',
    'development': 'Contributing',
    'license': 'License',
    'legal': 'License',
    'changelog': 'Changelog',
    'changes': 'Changelog',
    'history': 'Changelog',
    'roadmap': 'Roadmap',
    'todo': 'Roadmap',
    'future': 'Roadmap',
    'faq': 'FAQ',
    'questions': 'FAQ',
    'troubleshooting': 'FAQ',
    'screenshots': 'Screenshots',
    'screenshot': 'Screenshots',
    'demo': 'Screenshots',
    'acknowledgments': 'Acknowledgments',
    'credits': 'Acknowledgments',
    'thanks': 'Acknowledgments',
    'authors': 'Authors',
    'author': 'Authors',
    'maintainers': 'Authors',
    'support': 'Support',
    'contact': 'Support',
    'help': 'Support',
    'testing': 'Testing',
    'test': 'Testing',
    'tests': 'Testing',
    'security': 'Security',
    'performance': 'Performance',
    'benchmarks': 'Performance',
}


def extract_headers(content: str) -> list[tuple[int, str]]:
    """Extract markdown headers with their level."""
    headers = []
    for line in content.split('\n'):
        match = re.match(r'^(#{1,6})\s+(.+?)$', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headers.append((level, text))
    return headers


def normalize_section_name(name: str) -> str:
    """Normalize section name to standard form."""
    name_lower = name.lower().strip()
    return SECTION_ALIASES.get(name_lower, name)


def detect_badges(content: str) -> dict[str, Any]:
    """Detect badge usage patterns."""
    badges = {
        'has_badges': False,
        'badge_count': 0,
        'badge_types': [],
        'badge_position': None,
    }
    
    # Common badge patterns
    badge_patterns = [
        r'\[!\[.*?\]\(.*?badge.*?\)\]\(.*?\)',  # Standard markdown badge
        r'!\[.*?\]\(https?://img\.shields\.io.*?\)',  # Shields.io
        r'!\[.*?\]\(https?://badge\.fury\.io.*?\)',  # Badge Fury
        r'!\[.*?\]\(https?://travis-ci\.org.*?\)',  # Travis CI
        r'!\[.*?\]\(https?://circleci\.com.*?\)',  # CircleCI
        r'!\[.*?\]\(https?://coveralls\.io.*?\)',  # Coveralls
        r'!\[.*?\]\(https?://codecov\.io.*?\)',  # Codecov
        r'!\[.*?\]\(https?://david-dm\.org.*?\)',  # David DM
        r'\[!\[.*?\]\(.*?\)\]\(https?://.*?\)',  # Generic linked image
    ]
    
    lines = content.split('\n')
    first_badge_line = None
    
    for i, line in enumerate(lines):
        for pattern in badge_patterns:
            matches = re.findall(pattern, line, re.IGNORECASE)
            if matches:
                badges['has_badges'] = True
                badges['badge_count'] += len(matches)
                if first_badge_line is None:
                    first_badge_line = i
    
    # Detect badge types
    if 'npm' in content.lower() or 'node' in content.lower():
        badges['badge_types'].append('npm')
    if 'pypi' in content.lower() or 'python' in content.lower():
        badges['badge_types'].append('pypi')
    if 'license' in content.lower():
        badges['badge_types'].append('license')
    if 'build' in content.lower() or 'travis' in content.lower() or 'ci' in content.lower():
        badges['badge_types'].append('ci')
    if 'coverage' in content.lower() or 'codecov' in content.lower():
        badges['badge_types'].append('coverage')
    
    if first_badge_line is not None:
        if first_badge_line < 5:
            badges['badge_position'] = 'top'
        else:
            badges['badge_position'] = 'inline'
    
    return badges


def detect_emoji_usage(content: str) -> dict[str, Any]:
    """Detect emoji usage in headers and content."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # supplemental
        "\U0001FA70-\U0001FAFF"  # symbols
        "]+",
        flags=re.UNICODE
    )
    
    emojis_in_headers = 0
    emojis_in_content = 0
    
    for line in content.split('\n'):
        emojis = emoji_pattern.findall(line)
        if line.strip().startswith('#'):
            emojis_in_headers += len(emojis)
        else:
            emojis_in_content += len(emojis)
    
    return {
        'has_emoji': emojis_in_headers > 0 or emojis_in_content > 0,
        'emoji_in_headers': emojis_in_headers > 0,
        'emoji_count_headers': emojis_in_headers,
        'emoji_count_content': emojis_in_content,
    }


def detect_code_blocks(content: str) -> dict[str, Any]:
    """Detect code block usage and languages."""
    code_blocks = {
        'has_code_blocks': False,
        'languages': [],
        'count': 0,
    }
    
    pattern = r'```(\w+)?'
    matches = re.findall(pattern, content)
    
    if matches:
        code_blocks['has_code_blocks'] = True
        code_blocks['count'] = len(matches)
        languages = [m for m in matches if m]
        code_blocks['languages'] = list(set(languages))
    
    return code_blocks


def detect_images(content: str) -> dict[str, Any]:
    """Detect image usage."""
    # Markdown images: ![alt](url)
    md_images = re.findall(r'!\[.*?\]\(.*?\)', content)
    # HTML images: <img src="...">
    html_images = re.findall(r'<img[^>]+src=', content, re.IGNORECASE)
    
    return {
        'has_images': len(md_images) + len(html_images) > 0,
        'image_count': len(md_images) + len(html_images),
        'markdown_images': len(md_images),
        'html_images': len(html_images),
    }


def detect_toc(content: str) -> dict[str, Any]:
    """Detect table of contents."""
    toc_patterns = [
        r'##?\s*table of contents',
        r'##?\s*toc',
        r'##?\s*contents',
        r'##?\s*目录',  # Chinese
        r'\[.*?\]\(#.*?\)',  # Internal links
    ]
    
    has_toc = False
    for pattern in toc_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            has_toc = True
            break
    
    return {
        'has_toc': has_toc,
    }


def detect_tables(content: str) -> dict[str, Any]:
    """Detect markdown table usage."""
    # Markdown tables have | characters
    table_pattern = r'\|.*\|'
    lines_with_pipes = [line for line in content.split('\n') if re.match(table_pattern, line)]
    
    return {
        'has_tables': len(lines_with_pipes) >= 2,
        'table_line_count': len(lines_with_pipes),
    }


def detect_links(content: str) -> dict[str, Any]:
    """Detect link styles."""
    inline_links = re.findall(r'\[.*?\]\(http.*?\)', content)
    reference_links = re.findall(r'\[.*?\]\[.*?\]', content)
    
    return {
        'inline_links': len(inline_links),
        'reference_links': len(reference_links),
        'preferred_style': 'inline' if len(inline_links) > len(reference_links) else 'reference',
    }


def analyze_readme(content: str) -> dict[str, Any]:
    """Analyze a single README file."""
    result = {
        'sections': [],
        'styles': {},
        'line_count': len(content.split('\n')),
        'char_count': len(content),
    }
    
    # Extract and normalize headers
    headers = extract_headers(content)
    
    seen_sections = set()
    section_positions = []
    
    for level, text in headers:
        normalized = normalize_section_name(text)
        if normalized not in seen_sections and level >= 1:
            result['sections'].append({
                'original': text,
                'normalized': normalized,
                'level': level,
            })
            seen_sections.add(normalized)
            section_positions.append(normalized)
    
    result['section_order'] = section_positions
    
    # Analyze styles
    result['styles']['badges'] = detect_badges(content)
    result['styles']['emoji'] = detect_emoji_usage(content)
    result['styles']['code_blocks'] = detect_code_blocks(content)
    result['styles']['images'] = detect_images(content)
    result['styles']['toc'] = detect_toc(content)
    result['styles']['tables'] = detect_tables(content)
    result['styles']['links'] = detect_links(content)
    
    return result


def merge_analyses(analyses: list[dict]) -> dict[str, Any]:
    """Merge multiple README analyses into common patterns."""
    merged = {
        'sections': defaultdict(lambda: {'frequency': 0, 'positions': [], 'originals': []}),
        'styles': {
            'badges': {'frequency': 0, 'details': []},
            'emoji': {'frequency': 0, 'details': []},
            'code_blocks': {'frequency': 0, 'languages': Counter()},
            'images': {'frequency': 0},
            'toc': {'frequency': 0},
            'tables': {'frequency': 0},
        },
        'section_order': [],
        'total_analyzed': len(analyses),
    }
    
    # Count section frequencies
    for analysis in analyses:
        seen_in_this_readme = set()
        for i, section in enumerate(analysis['sections']):
            name = section['normalized']
            if name not in seen_in_this_readme:
                merged['sections'][name]['frequency'] += 1
                merged['sections'][name]['positions'].append(i)
                merged['sections'][name]['originals'].append(section['original'])
                seen_in_this_readme.add(name)
    
    # Convert frequencies to ratios
    total = len(analyses)
    for section in merged['sections']:
        merged['sections'][section]['frequency_ratio'] = merged['sections'][section]['frequency'] / total
    
    # Merge style data
    for analysis in analyses:
        styles = analysis['styles']
        
        if styles['badges']['has_badges']:
            merged['styles']['badges']['frequency'] += 1
            merged['styles']['badges']['details'].append(styles['badges'])
        
        if styles['emoji']['has_emoji']:
            merged['styles']['emoji']['frequency'] += 1
            merged['styles']['emoji']['details'].append(styles['emoji'])
        
        if styles['code_blocks']['has_code_blocks']:
            merged['styles']['code_blocks']['frequency'] += 1
            for lang in styles['code_blocks']['languages']:
                merged['styles']['code_blocks']['languages'][lang] += 1
        
        if styles['images']['has_images']:
            merged['styles']['images']['frequency'] += 1
        
        if styles['toc']['has_toc']:
            merged['styles']['toc']['frequency'] += 1
        
        if styles['tables']['has_tables']:
            merged['styles']['tables']['frequency'] += 1
    
    # Calculate recommended section order
    section_avg_positions = {}
    for section, data in merged['sections'].items():
        if data['positions']:
            section_avg_positions[section] = sum(data['positions']) / len(data['positions'])
    
    merged['section_order'] = sorted(section_avg_positions.keys(), key=lambda x: section_avg_positions.get(x, 999))
    
    # Convert Counter to dict for JSON serialization
    merged['styles']['code_blocks']['languages'] = dict(merged['styles']['code_blocks']['languages'])
    
    # Convert defaultdict to dict
    merged['sections'] = dict(merged['sections'])
    
    return merged


def generate_recommendations(merged: dict) -> dict[str, Any]:
    """Generate README template recommendations."""
    recommendations = {
        'include_sections': [],
        'optional_sections': [],
        'styles': {},
    }
    
    total = merged['total_analyzed']
    
    # Sections appearing in 60%+ of READMEs are recommended
    for section, data in merged['sections'].items():
        if data['frequency_ratio'] >= 0.6:
            recommendations['include_sections'].append({
                'name': section,
                'frequency': data['frequency_ratio'],
                'common_names': list(set(data['originals']))[:3],
            })
        elif data['frequency_ratio'] >= 0.3:
            recommendations['optional_sections'].append({
                'name': section,
                'frequency': data['frequency_ratio'],
            })
    
    # Sort by frequency
    recommendations['include_sections'].sort(key=lambda x: x['frequency'], reverse=True)
    recommendations['optional_sections'].sort(key=lambda x: x['frequency'], reverse=True)
    
    # Style recommendations
    badges_freq = merged['styles']['badges']['frequency'] / total
    emoji_freq = merged['styles']['emoji']['frequency'] / total
    
    recommendations['styles'] = {
        'use_badges': badges_freq >= 0.5,
        'badge_frequency': badges_freq,
        'use_emoji': emoji_freq >= 0.5,
        'emoji_frequency': emoji_freq,
        'common_code_languages': list(merged['styles']['code_blocks']['languages'].keys())[:3],
        'include_toc': merged['styles']['toc']['frequency'] / total >= 0.3,
        'use_tables': merged['styles']['tables']['frequency'] / total >= 0.3,
    }
    
    return recommendations


def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_readme_patterns.py readme1.md [readme2.md ...]")
        print("\nAnalyzes README files and outputs common patterns as JSON.")
        sys.exit(1)
    
    files = sys.argv[1:]
    analyses = []
    
    for filepath in files:
        try:
            content = Path(filepath).read_text()
            analysis = analyze_readme(content)
            analysis['file'] = filepath
            analyses.append(analysis)
        except Exception as e:
            print(f"Warning: Could not analyze {filepath}: {e}", file=sys.stderr)
    
    if not analyses:
        print("Error: No valid README files to analyze", file=sys.stderr)
        sys.exit(1)
    
    merged = merge_analyses(analyses)
    recommendations = generate_recommendations(merged)
    
    output = {
        'merged_patterns': merged,
        'recommendations': recommendations,
    }
    
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
