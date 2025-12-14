#!/bin/bash
# Consciousness Collaboration Server Startup Script
# ∰€π

cd "$(dirname "$0")"

PORT=7010
LOGFILE="server.log"
PIDFILE="server.pid"

echo "∰€π Consciousness Collaboration Server"
echo "======================================"
echo ""

# Check if already running
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "✅ Server already running on port $PORT (PID: $PID)"
        echo ""
        echo "📊 Access points:"
        echo "   Dashboard:  http://192.168.0.102:$PORT/index.html"
        echo "   Game:       http://192.168.0.102:$PORT/nessing_game.html"
        echo "   Lexeme:     http://192.168.0.102:$PORT/lexeme_universal_impact_framework.html"
        echo ""
        echo "📝 View logs:  tail -f $LOGFILE"
        echo "🛑 Stop:       kill $PID"
        exit 0
    else
        echo "⚠️  Stale PID file found, removing..."
        rm "$PIDFILE"
    fi
fi

# Get local IP address
LOCAL_IP=$(ifconfig 2>/dev/null | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
if [ -z "$LOCAL_IP" ]; then
    LOCAL_IP="192.168.0.102"  # Fallback to known IP
fi

# Start server
echo "🚀 Starting consciousness collaboration server..."
nohup python3 -m http.server "$PORT" --bind 0.0.0.0 > "$LOGFILE" 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > "$PIDFILE"

# Wait a moment and verify it started
sleep 1
if ps -p "$SERVER_PID" > /dev/null 2>&1; then
    echo "✅ Server started successfully on port $PORT (PID: $SERVER_PID)"
    echo ""
    echo "📊 Access points:"
    echo "   Local:       http://localhost:$PORT/index.html"
    echo "   Network:     http://$LOCAL_IP:$PORT/index.html"
    echo ""
    echo "📝 Available pages:"
    echo "   /index.html                              - Interactive dashboard"
    echo "   /nessing_game.html                       - Original game interface"
    echo "   /lexeme_universal_impact_framework.html  - Lexeme framework"
    echo ""
    echo "⚙️  Management:"
    echo "   View logs:   tail -f $LOGFILE"
    echo "   Stop server: kill $SERVER_PID"
    echo "   Or:          kill \$(cat $PIDFILE)"
    echo ""
    echo "∰€π Consciousness entities ready for collaboration"
else
    echo "❌ Failed to start server"
    echo "Check logs: cat $LOGFILE"
    rm "$PIDFILE"
    exit 1
fi
