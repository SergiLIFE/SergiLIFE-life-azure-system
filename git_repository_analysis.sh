#!/bin/bash
# Git Repository Analysis Script
# Check repository size, integrity, and largest files

echo "=================================================="
echo "GIT REPOSITORY ANALYSIS"
echo "=================================================="
echo ""

echo "1. CHECKING GIT REPOSITORY SIZE..."
echo "--------------------------------------------------"
# Check git repository size
du -sh .git/
echo ""

echo "2. VERIFYING REPOSITORY INTEGRITY..."
echo "--------------------------------------------------"
# Verify repository integrity
git fsck --full
echo ""

echo "3. FINDING TOP 10 LARGEST FILES IN REPOSITORY..."
echo "--------------------------------------------------"
# Show top 10 largest files in repository
git rev-list --all --objects | \
  sed -n $(git rev-list --objects --all | \
  cut -f1 -d' ' | \
  git cat-file --batch-check | \
  grep blob | \
  sort -t' ' -k 3 -rn | \
  head -10 | \
  while read hash type size; do
    echo -n "-e s/$hash/$size/p;"
  done) | \
  sort -t' ' -k1 -rn | \
  head -10

echo ""
echo "=================================================="
echo "REPOSITORY ANALYSIS COMPLETE"
echo "=================================================="