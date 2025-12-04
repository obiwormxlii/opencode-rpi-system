#!/bin/bash
# RPI System - Sync configuration with GitHub repository
# This script helps maintain the base configuration in sync with a remote repo

set -e

CONFIG_DIR="$HOME/.config/opencode"
REPO_URL="${RPI_REPO_URL:-https://github.com/obiwormxlii/opencode-rpi-system.git}"  # Default repo URL

usage() {
    echo "Usage: sync-config.sh [command]"
    echo ""
    echo "Commands:"
    echo "  push      - Push local config to remote repository"
    echo "  pull      - Pull remote config to local"
    echo "  status    - Show git status of config directory"
    echo "  setup     - Initialize git repository in config directory"
    echo ""
    echo "Set RPI_REPO_URL environment variable to specify remote repository"
    exit 1
}

check_git() {
    if [ ! -d "$CONFIG_DIR/.git" ]; then
        echo "Error: Config directory is not a git repository"
        echo "Run: sync-config.sh setup"
        exit 1
    fi
}

setup_repo() {
    cd "$CONFIG_DIR"
    
    if [ -d ".git" ]; then
        echo "Git repository already initialized"
        return
    fi
    
    echo "Initializing git repository in $CONFIG_DIR"
    git init
    
    # Create .gitignore for config directory
    cat > .gitignore << 'EOF'
# Ignore OpenCode user-specific files
token.json
credentials.json
.DS_Store
*.log

# Keep the core configuration
!agent/
!command/
!prompt/
!rules/
!scripts/
!opencode.json
EOF
    
    git add .
    git commit -m "Initial commit: RPI system base configuration"
    
    if [ -n "$REPO_URL" ]; then
        echo "Adding remote repository: $REPO_URL"
        git remote add origin "$REPO_URL"
    else
        echo "No REPO_URL set. Add remote manually with:"
        echo "  git remote add origin <your-repo-url>"
    fi
    
    echo "Setup complete!"
}

push_config() {
    check_git
    cd "$CONFIG_DIR"
    
    echo "Pushing configuration to remote repository..."
    git add agent/ command/ prompt/ rules/ scripts/ opencode.json
    
    if git diff --cached --quiet; then
        echo "No changes to commit"
    else
        git commit -m "Update RPI configuration - $(date '+%Y-%m-%d %H:%M:%S')"
        git push origin main
        echo "Configuration pushed successfully"
    fi
}

pull_config() {
    check_git
    cd "$CONFIG_DIR"
    
    echo "Pulling configuration from remote repository..."
    git pull origin main
    echo "Configuration updated successfully"
}

show_status() {
    check_git
    cd "$CONFIG_DIR"
    
    echo "Configuration status:"
    git status
}

# Main command handling
case "${1:-}" in
    push)
        push_config
        ;;
    pull)
        pull_config
        ;;
    status)
        show_status
        ;;
    setup)
        setup_repo
        ;;
    *)
        usage
        ;;
esac
