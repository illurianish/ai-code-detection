#!/bin/bash

# 🚀 Deploy AI Code Detection Bot to GitHub Pages
# This script prepares and deploys the frontend for GitHub Pages demo

echo "🚀 Preparing AI Code Detection Bot for GitHub Pages deployment..."

# Create gh-pages directory
mkdir -p gh-pages

# Copy frontend files
cp -r frontend/* gh-pages/

# Update script.js for demo mode
sed -i.bak 's/DEMO_MODE: false/DEMO_MODE: true/g' gh-pages/script.js
sed -i.bak 's|API_BASE_URL: .*|API_BASE_URL: "https://your-app-name.onrender.com", // Update this with your backend URL|g' gh-pages/script.js

# Clean up backup files
rm gh-pages/*.bak 2>/dev/null || true

echo "✅ Files prepared in gh-pages/ directory"
echo ""
echo "📋 Next steps:"
echo "1. Update gh-pages/script.js with your backend URL (if you have one)"
echo "2. Push gh-pages directory to GitHub"
echo "3. Enable GitHub Pages in repository settings"
echo ""
echo "Commands to deploy:"
echo "  git add gh-pages/"
echo "  git commit -m 'Deploy to GitHub Pages'"
echo "  git subtree push --prefix gh-pages origin gh-pages"
echo ""
echo "🌐 Your demo will be available at:"
echo "  https://yourusername.github.io/ai-code-detection/"

# Make the script executable
chmod +x scripts/deploy-github-pages.sh 