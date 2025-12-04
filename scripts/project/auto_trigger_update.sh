#!/bin/bash
# Auto-trigger project status update after /implement completes
# Called automatically by build agent after implementation

PROJECT_DIR=".opencode/project"

# Check if project initialized
if [ ! -d "$PROJECT_DIR" ]; then
    echo "No .opencode/project/ found - skipping auto-update"
    exit 0
fi

echo "📊 Auto-updating project status..."

# Run update script
python "$(dirname "$0")/update_project_status.py" . 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Project status updated"
else
    echo "⚠️ Failed to update project status (non-blocking)"
fi

exit 0
