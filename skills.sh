#!/bin/bash

SKILLS_DIR="$(cd "$(dirname "$0")" && pwd)/skills"

register_skills() {
    local target="${1:-$HOME/.claude/skills}"
    mkdir -p "$target"
    for skill in "$SKILLS_DIR"/*/; do
        name=$(basename "$skill")
        [ -L "$target/$name" ] && rm "$target/$name"
        [ -d "$target/$name" ] && rm -rf "$target/$name"
        ln -s "$skill" "$target/$name"
        echo "  + $name"
    done
    echo "Done: $target"
}

unregister_skills() {
    local target="${1:-$HOME/.claude/skills}"
    for skill in "$SKILLS_DIR"/*/; do
        name=$(basename "$skill")
        [ -L "$target/$name" ] && rm "$target/$name" && echo "  - $name"
    done
}

list_skills() {
    echo "Available skills:"
    for skill in "$SKILLS_DIR"/*/; do
        name=$(basename "$skill")
        desc=$(grep -m1 "^description:" "$skill/SKILL.md" 2>/dev/null | cut -d: -f2- | xargs | cut -c1-50)
        echo "  $name - $desc..."
    done
}

case "${1:-}" in
    register) register_skills "$2" ;;
    unregister) unregister_skills "$2" ;;
    list) list_skills ;;
    *) echo "Usage: source skills.sh && {register|unregister|list} [target_dir]" ;;
esac
