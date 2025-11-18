#!/bin/bash

# Check git status
echo "Checking status..."
git status

# Ask for commit message
echo
read -p "Enter commit message: " msg

# Add all changes
echo "Adding changes..."
git add .

# Commit
echo "Committing..."
git commit -m "$msg"

# Push
echo "Pushing to remote..."
git push

echo "Done!"
