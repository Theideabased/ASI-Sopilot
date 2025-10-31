#!/bin/bash

# Multi-Agent Runner Script for Solpilot System
# This script runs all three agents simultaneously

echo "🚀 Starting Solpilot Multi-Agent System..."
echo "================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "================================================"
echo "🤖 Launching Agents..."
echo "================================================"

# Function to handle cleanup on script exit
cleanup() {
    echo ""
    echo "🛑 Shutting down agents..."
    kill $(jobs -p) 2>/dev/null
    echo "✅ All agents stopped"
    exit 0
}

# Set trap to cleanup on CTRL+C
trap cleanup INT TERM

# Start Solpilot agent
echo "▶️  Starting Solpilot Agent (Port 8000)..."
python solpilot_agent.py &
SOLPILOT_PID=$!
sleep 2

# Start Sonia agent
echo "▶️  Starting Sonia Agent (Port 8001)..."
python sonia_agent.py &
SONIA_PID=$!
sleep 2

# Start Venice agent
echo "▶️  Starting Venice Agent (Port 8002)..."
python venice_agent.py &
VENICE_PID=$!
sleep 2

echo ""
echo "================================================"
echo "✅ All agents are running!"
echo "================================================"
echo ""
echo "📊 Agent Status:"
echo "  • Solpilot (Main):      PID $SOLPILOT_PID - Port 8000"
echo "  • Sonia (Analyst):      PID $SONIA_PID - Port 8001"
echo "  • Venice (Research):    PID $VENICE_PID - Port 8002"
echo ""
echo "🌐 Visit the Agentverse Inspector URLs shown above"
echo "📬 Connect each agent via Mailbox to make them discoverable on ASI:One"
echo ""
echo "Press CTRL+C to stop all agents"
echo "================================================"

# Wait for all background processes
wait
