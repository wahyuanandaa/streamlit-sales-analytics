#!/bin/bash

echo "🚀 Starting deployment process for Sales Analytics Dashboard..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Deploy: Sales Analytics Dashboard $(date '+%Y-%m-%d %H:%M:%S')"

# Check if remote origin exists
if ! git remote get-url origin &> /dev/null; then
    echo "⚠️  No remote origin found."
    echo "Please add your GitHub repository URL:"
    echo "git remote add origin https://github.com/username/streamlit-sales-analytics.git"
    echo ""
    echo "Then run: git push -u origin main"
else
    echo "🚀 Pushing to GitHub..."
    git push origin main
fi

echo ""
echo "✅ Deployment preparation completed!"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://share.streamlit.io"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Select your repository: username/streamlit-sales-analytics"
echo "5. Set main file path to: app_deploy.py"
echo "6. Click 'Deploy'"
echo ""
echo "🌐 Your dashboard will be available at: https://your-app-name.streamlit.app" 