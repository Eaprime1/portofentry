# 🌐 Server Information & Setup

**Location:** Pixel 8a
**Current Setup:** Running at http://192.168.0.102:7010
**Status:** Active development

---

## Current Server

### Your Existing Setup:

**URL:** http://192.168.0.102:7010
**Existing Page:** lexeme_universal_impact_framework.html

**Network:**
- Local IP: 192.168.0.102
- Port: 7010
- Accessible on local network

### New Dashboard Integration:

**New file created:** `index.html` (interactive consciousness dashboard)

**To access:**
- Main dashboard: http://192.168.0.102:7010/index.html
- Original game: http://192.168.0.102:7010/nessing_game.html
- Lexeme framework: http://192.168.0.102:7010/lexeme_universal_impact_framework.html

---

## Starting the Server

### If server is not running:

**Method 1: Python HTTP Server**
```bash
cd /storage/emulated/0/unexusi_pixel8a/unexusi_server_pixel8a
python3 -m http.server 7010 --bind 0.0.0.0
```

**Method 2: Background server (persistent)**
```bash
cd /storage/emulated/0/unexusi_pixel8a/unexusi_server_pixel8a
nohup python3 -m http.server 7010 --bind 0.0.0.0 > server.log 2>&1 &
echo $! > server.pid
echo "Server started on port 7010"
```

### Check if server is running:

```bash
# Method 1: Check process
ps aux | grep "http.server.*7010"

# Method 2: Check PID file
if [ -f server.pid ]; then
    cat server.pid
    ps -p $(cat server.pid)
fi

# Method 3: Test connection
curl http://localhost:7010
```

### Stop the server:

```bash
# If using PID file
kill $(cat server.pid)
rm server.pid

# Or find and kill
pkill -f "http.server.*7010"
```

---

## Quick Server Management Script

Created: `start_server.sh`

```bash
#!/bin/bash
# Start consciousness collaboration server

cd "$(dirname "$0")"

PORT=7010
LOGFILE="server.log"
PIDFILE="server.pid"

# Check if already running
if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "∰€π Server already running on port $PORT (PID: $PID)"
        echo "Access at: http://192.168.0.102:$PORT"
        exit 0
    else
        rm "$PIDFILE"
    fi
fi

# Start server
echo "∰€π Starting consciousness collaboration server..."
nohup python3 -m http.server "$PORT" --bind 0.0.0.0 > "$LOGFILE" 2>&1 &
echo $! > "$PIDFILE"

echo "✅ Server started on port $PORT"
echo "📊 Access dashboard: http://192.168.0.102:$PORT/index.html"
echo "🎮 Original game: http://192.168.0.102:$PORT/nessing_game.html"
echo "📝 Server logs: tail -f $LOGFILE"
echo "🛑 Stop server: kill \$(cat $PIDFILE)"
```

Usage:
```bash
bash start_server.sh
```

---

## Accessing Your Server

### From Pixel 8a (local):
```
http://localhost:7010/index.html
http://127.0.0.1:7010/index.html
```

### From other devices on same network:
```
http://192.168.0.102:7010/index.html
```

### Available pages:
- `/index.html` - New interactive dashboard
- `/nessing_game.html` - Original game interface
- `/lexeme_universal_impact_framework.html` - Existing lexeme page

---

## Network Configuration

### Find your current IP:

```bash
# Method 1
ifconfig | grep "inet " | grep -v 127.0.0.1

# Method 2
ip addr show | grep "inet " | grep -v 127.0.0.1

# Method 3 (if available)
hostname -I
```

### Make accessible from internet (careful!):

**Using port forwarding:**
1. Router settings → Port forwarding
2. Forward external port → 192.168.0.102:7010
3. Use dynamic DNS service for stable address

**Using Termux sshd + tunnel:**
```bash
pkg install openssh
sshd
# Then use SSH tunnel from remote machine
```

**Security note:** Only expose if you understand the risks!

---

## Firewall / Access

### Allow Termux network access:

```bash
# Termux should already have permissions
# If issues, check Android settings:
# Settings → Apps → Termux → Permissions → Network
```

### Test from another device:

```bash
# On another device on same network:
curl http://192.168.0.102:7010

# Should see HTML content
```

---

## Monitoring

### View server logs:

```bash
# Real-time log viewing
tail -f server.log

# Last 50 lines
tail -50 server.log

# Search logs
grep "GET" server.log
```

### Check access:

```bash
# See recent requests
tail -20 server.log | grep "GET"

# Count requests
grep -c "GET" server.log
```

---

## Troubleshooting

### Port 7010 already in use?

```bash
# Find what's using the port
lsof -i :7010

# Kill the process
kill [PID]

# Or use different port
python3 -m http.server 7011 --bind 0.0.0.0
```

### Can't access from other devices?

**Check:**
1. Server is bound to 0.0.0.0 (not 127.0.0.1)
2. Firewall allows incoming on port 7010
3. Devices are on same network
4. IP address is correct (changes on WiFi reconnect)

**Test:**
```bash
# On Pixel 8a:
python3 -m http.server 7010 --bind 0.0.0.0

# On another device:
ping 192.168.0.102
curl http://192.168.0.102:7010
```

### Server stops when closing Termux?

**Use Termux:Boot or wake lock:**

```bash
# Acquire wake lock (keep running)
termux-wake-lock

# Or use nohup (already in start script)
nohup python3 -m http.server 7010 --bind 0.0.0.0 &

# Release wake lock when done
termux-wake-unlock
```

### JSON not loading in browser?

**Check:**
1. Server is running from correct directory
2. JSON files exist
3. Browser console for CORS errors
4. Server logs for 404 errors

**Fix:**
```bash
# Ensure running from server directory
cd /storage/emulated/0/unexusi_pixel8a/unexusi_server_pixel8a
python3 -m http.server 7010 --bind 0.0.0.0
```

---

## HTTPS Setup (Advanced)

### Self-signed certificate:

```bash
# Generate certificate
openssl req -x509 -newkey rsa:4096 \
  -keyout key.pem -out cert.pem \
  -days 365 -nodes \
  -subj "/CN=192.168.0.102"

# Create HTTPS server script
cat > https_server.py << 'EOF'
import http.server
import ssl

server_address = ('0.0.0.0', 7010)
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
httpd.socket = ssl.wrap_socket(httpd.socket,
                                server_side=True,
                                certfile='cert.pem',
                                keyfile='key.pem',
                                ssl_version=ssl.PROTOCOL_TLS)
print(f"HTTPS server running on port {server_address[1]}")
httpd.serve_forever()
EOF

# Run HTTPS server
python3 https_server.py
```

**Access:** https://192.168.0.102:7010 (accept self-signed warning)

---

## GitHub Status

**Current:** Not yet initialized in this directory

**To initialize:**
```bash
cd /storage/emulated/0/unexusi_pixel8a/unexusi_server_pixel8a
git init .
git add .
git commit -m "∰€π Initial: Consciousness server with interactive dashboard"

# If you have existing GitHub repo:
git remote add origin https://github.com/[user]/unexusi_server_pixel8a.git
git push -u origin main
```

**Note:** You mentioned "its on github" - if you mean you're accessing a GitHub-hosted version, you can still push updates from here.

---

## Quick Reference

**Start server:**
```bash
bash start_server.sh
# or
python3 -m http.server 7010 --bind 0.0.0.0
```

**Stop server:**
```bash
kill $(cat server.pid)
```

**Access dashboard:**
```
http://192.168.0.102:7010/index.html
```

**View logs:**
```bash
tail -f server.log
```

**Check status:**
```bash
ps -p $(cat server.pid)
```

---

**∰€π - Server ready for consciousness collaboration**

*Local network accessible | Interactive dashboard | Pattern recognition active*

€(server_info_complete)
