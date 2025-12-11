#!/bin/bash
# Quick start script to initialize database and run a test export

set -e

echo "🚀 Quick Start - Database Connection and Export Tool"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Initialize database
echo "🗄️  Initializing sample database..."
python scripts/init_database.py

# Run export
echo "📊 Exporting table to Excel..."
python -m src.main --table sample_table --output report.xlsx

echo ""
echo "✅ Done! Check report.xlsx for the exported data."

