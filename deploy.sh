#!/bin/bash

# Pitch Deck Enhancer - Fixed Version Deployment Script
# This script helps you deploy the fixed app quickly

echo "🚀 Pitch Deck Enhancer (FIXED VERSION) - Quick Deploy"
echo "========================================================"
echo ""

# Check if API key is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  GOOGLE_API_KEY not found in environment"
    echo ""
    echo "🔑 CRITICAL: Get your FREE API key first!"
    echo "   1. Visit: https://aistudio.google.com/"
    echo "   2. Sign in with Google"
    echo "   3. Click 'Get API Key' or 'Create API Key'"
    echo "   4. Copy the key (starts with 'AIza')"
    echo "   5. Test it at: https://aistudio.google.com/app/prompts/new_chat"
    echo ""
    echo "💡 Then set it locally: export GOOGLE_API_KEY='AIza...'"
    echo ""
else
    echo "✅ API key found in environment"
    echo "🔑 Key starts with: ${GOOGLE_API_KEY:0:10}..."
fi

# Check if Git is initialized
if [ ! -d ".git" ]; then
    echo ""
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Pitch Deck Enhancer (FIXED) - Gemini API compatible"
    echo "✅ Git repository created"
else
    echo "📦 Git repository already exists"
fi

echo ""
echo "🚀 DEPLOYMENT STEPS:"
echo "===================="
echo ""
echo "1. 📁 Push to GitHub:"
echo "   git remote add origin YOUR_GITHUB_REPO_URL"
echo "   git push -u origin main"
echo ""
echo "2. 🌐 Deploy on Streamlit Cloud:"
echo "   • Visit: https://share.streamlit.io"
echo "   • Click 'New app'"
echo "   • Connect your GitHub repository"
echo "   • Main file: app.py"
echo "   • Click 'Deploy'"
echo ""
echo "3. 🔐 Add API Key in Streamlit Secrets:"
echo "   • Go to app Settings → Secrets"
echo "   • Add: GOOGLE_API_KEY = \"YOUR_ACTUAL_KEY\""
echo "   • Save and restart app"
echo ""
echo "4. ✅ Verify deployment:"
echo "   • Check for '✅ Connected to Gemini API' in sidebar"
echo "   • Upload test document"
echo "   • Try generating structure analysis"
echo ""
echo "🎉 Your FIXED app will be live at:"
echo "   https://your-app-name.streamlit.app"
echo ""
echo "💡 This version fixes the '404 gemini-pro not found' error!"
