#!/usr/bin/env python3
"""
Project Info Detector

Auto-detects project metadata from current directory.

Usage:
    python3 detect_project_info.py

Output:
    JSON with project name, type, language, framework, and other metadata.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional


def detect_node_project() -> Optional[dict[str, Any]]:
    """Detect Node.js project from package.json."""
    pkg_path = Path("package.json")
    if not pkg_path.exists():
        return None
    
    try:
        import json
        with open(pkg_path) as f:
            pkg = json.load(f)
        
        deps = pkg.get("dependencies", {})
        dev_deps = pkg.get("devDependencies", {})
        all_deps = {**deps, **dev_deps}
        
        frameworks = []
        if "react" in all_deps:
            frameworks.append("react")
        if "next" in all_deps:
            frameworks.append("nextjs")
        if "vue" in all_deps:
            frameworks.append("vue")
        if "angular" in all_deps or "@angular/core" in all_deps:
            frameworks.append("angular")
        if "express" in all_deps:
            frameworks.append("express")
        if "fastify" in all_deps:
            frameworks.append("fastify")
        if "nestjs" in all_deps or "@nestjs/core" in all_deps:
            frameworks.append("nestjs")
        if "svelte" in all_deps:
            frameworks.append("svelte")
        if "remix" in all_deps:
            frameworks.append("remix")
        if "astro" in all_deps:
            frameworks.append("astro")
        
        return {
            "name": pkg.get("name"),
            "version": pkg.get("version"),
            "description": pkg.get("description"),
            "author": pkg.get("author"),
            "license": pkg.get("license"),
            "repository": pkg.get("repository", {}).get("url") if isinstance(pkg.get("repository"), dict) else pkg.get("repository"),
            "keywords": pkg.get("keywords", []),
            "type": "node",
            "frameworks": frameworks,
            "main": pkg.get("main"),
            "bin": pkg.get("bin"),
        }
    except Exception:
        return None


def detect_python_project() -> Optional[dict[str, Any]]:
    """Detect Python project from pyproject.toml or setup.py."""
    result = {
        "type": "python",
        "frameworks": [],
    }
    
    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        try:
            content = pyproject_path.read_text()
            
            name_match = re.search(r'^name\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
            version_match = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
            desc_match = re.search(r'^description\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
            
            if name_match:
                result["name"] = name_match.group(1)
            if version_match:
                result["version"] = version_match.group(1)
            if desc_match:
                result["description"] = desc_match.group(1)
            
            deps = re.search(r'dependencies\s*=\s*\[(.*?)\]', content, re.DOTALL)
            if deps:
                deps_content = deps.group(1)
                if "django" in deps_content.lower():
                    result["frameworks"].append("django")
                if "flask" in deps_content.lower():
                    result["frameworks"].append("flask")
                if "fastapi" in deps_content.lower():
                    result["frameworks"].append("fastapi")
                if "torch" in deps_content.lower() or "pytorch" in deps_content.lower():
                    result["frameworks"].append("pytorch")
            
            return result
        except Exception:
            pass
    
    setup_path = Path("setup.py")
    if setup_path.exists():
        try:
            content = setup_path.read_text()
            
            name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', content)
            version_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
            desc_match = re.search(r'description\s*=\s*["\']([^"\']+)["\']', content)
            author_match = re.search(r'author\s*=\s*["\']([^"\']+)["\']', content)
            
            if name_match:
                result["name"] = name_match.group(1)
            if version_match:
                result["version"] = version_match.group(1)
            if desc_match:
                result["description"] = desc_match.group(1)
            if author_match:
                result["author"] = author_match.group(1)
            
            return result
        except Exception:
            pass
    
    return None


def detect_rust_project() -> Optional[dict[str, Any]]:
    """Detect Rust project from Cargo.toml."""
    cargo_path = Path("Cargo.toml")
    if not cargo_path.exists():
        return None
    
    try:
        content = cargo_path.read_text()
        
        result = {"type": "rust", "frameworks": []}
        
        name_match = re.search(r'^name\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        version_match = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        desc_match = re.search(r'^description\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        license_match = re.search(r'^license\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        
        if name_match:
            result["name"] = name_match.group(1)
        if version_match:
            result["version"] = version_match.group(1)
        if desc_match:
            result["description"] = desc_match.group(1)
        if license_match:
            result["license"] = license_match.group(1)
        
        return result
    except Exception:
        return None


def detect_go_project() -> Optional[dict[str, Any]]:
    """Detect Go project from go.mod."""
    go_mod_path = Path("go.mod")
    if not go_mod_path.exists():
        return None
    
    try:
        content = go_mod_path.read_text()
        
        result = {"type": "go", "frameworks": []}
        
        module_match = re.search(r'^module\s+(.+)$', content, re.MULTILINE)
        go_version_match = re.search(r'^go\s+(\d+(?:\.\d+)?)', content, re.MULTILINE)
        
        if module_match:
            module_name = module_match.group(1).strip()
            result["name"] = module_name.split("/")[-1]
            result["module"] = module_name
        if go_version_match:
            result["go_version"] = go_version_match.group(1)
        
        return result
    except Exception:
        return None


def detect_java_project() -> Optional[dict[str, Any]]:
    """Detect Java project from pom.xml or build.gradle."""
    result = {"type": "java", "frameworks": []}
    
    pom_path = Path("pom.xml")
    if pom_path.exists():
        try:
            content = pom_path.read_text()
            
            name_match = re.search(r'<name>([^<]+)</name>', content)
            version_match = re.search(r'<version>([^<]+)</version>', content)
            desc_match = re.search(r'<description>([^<]+)</description>', content)
            
            if name_match:
                result["name"] = name_match.group(1)
            if version_match:
                result["version"] = version_match.group(1)
            if desc_match:
                result["description"] = desc_match.group(1)
            
            if "spring" in content.lower():
                result["frameworks"].append("spring")
            
            return result
        except Exception:
            pass
    
    gradle_path = Path("build.gradle")
    if gradle_path.exists():
        try:
            content = gradle_path.read_text()
            
            return result
        except Exception:
            pass
    
    return None


def detect_ruby_project() -> Optional[dict[str, Any]]:
    """Detect Ruby project from Gemfile or .gemspec."""
    result = {"type": "ruby", "frameworks": []}
    
    gemspecs = list(Path(".").glob("*.gemspec"))
    if gemspecs:
        try:
            content = gemspecs[0].read_text()
            
            name_match = re.search(r'\.name\s*=\s*["\']([^"\']+)["\']', content)
            version_match = re.search(r'\.version\s*=\s*["\']([^"\']+)["\']', content)
            desc_match = re.search(r'\.summary\s*=\s*["\']([^"\']+)["\']', content)
            
            if name_match:
                result["name"] = name_match.group(1)
            if version_match:
                result["version"] = version_match.group(1)
            if desc_match:
                result["description"] = desc_match.group(1)
            
            return result
        except Exception:
            pass
    
    return None


def get_git_info() -> dict[str, Any]:
    """Get git repository information."""
    result = {}
    
    try:
        remote_url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
        )
        if remote_url.returncode == 0:
            url = remote_url.stdout.strip()
            result["git_remote"] = url
            
            if "github.com" in url:
                match = re.search(r"github\.com[/:]([^/]+)/([^/.]+)", url)
                if match:
                    result["github_owner"] = match.group(1)
                    result["github_repo"] = match.group(2)
    except Exception:
        pass
    
    try:
        author = subprocess.run(
            ["git", "log", "-1", "--format=%an"],
            capture_output=True,
            text=True,
        )
        if author.returncode == 0:
            result["last_author"] = author.stdout.strip()
    except Exception:
        pass
    
    return result


def detect_all() -> dict[str, Any]:
    """Detect all project info."""
    result = {
        "detected": False,
        "cwd": os.getcwd(),
    }
    
    detectors = [
        ("node", detect_node_project),
        ("python", detect_python_project),
        ("rust", detect_rust_project),
        ("go", detect_go_project),
        ("java", detect_java_project),
        ("ruby", detect_ruby_project),
    ]
    
    for name, detector in detectors:
        info = detector()
        if info and info.get("name"):
            result.update(info)
            result["detected"] = True
            result["language"] = info.get("type")
            break
    
    git_info = get_git_info()
    result.update(git_info)
    
    if not result.get("name"):
        result["name"] = Path.cwd().name
    
    return result


def main():
    info = detect_all()
    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
