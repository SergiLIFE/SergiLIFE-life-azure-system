#!/bin/bash
# L.I.F.E. Platform - Cross-Platform Clinical Demo Launcher
# October 15, 2025 University Presentation
# Compatible with Linux, macOS, and WSL

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Clear screen and show header
clear
echo -e "${CYAN}=================================================${NC}"
echo -e "${YELLOW}   L.I.F.E. PLATFORM CLINICAL DEMO LAUNCHER${NC}"
echo -e "${GREEN}   October 15, 2025 University Presentation${NC}"
echo -e "${GREEN}   Teams Demo for 23 Colleagues${NC}"
echo -e "${CYAN}=================================================${NC}"
echo ""

echo -e "${GREEN}🎯 Demo Mode: Clinical Grade EEG Analysis${NC}"
echo -e "${GREEN}👥 Audience: 23 University Colleagues${NC}"
echo -e "${GREEN}📅 Date: October 15, 2025${NC}"
echo -e "${CYAN}⏰ Current Time: $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo ""

# Check if dashboard file exists
DASHBOARD_FILE="LIFE_CLINICAL_GRADE_DASHBOARD.html"

echo -e "${YELLOW}🔍 Pre-flight Checks:${NC}"

if [ -f "$DASHBOARD_FILE" ]; then
    echo -e "   ${GREEN}✅ Clinical dashboard file found${NC}"
    FILE_SIZE=$(du -h "$DASHBOARD_FILE" | cut -f1)
    echo -e "   ${CYAN}📊 File size: $FILE_SIZE${NC}"
else
    echo -e "   ${RED}❌ Clinical dashboard file missing!${NC}"
    echo -e "   ${YELLOW}Expected: $DASHBOARD_FILE${NC}"
    echo ""
    echo -e "${CYAN}Available HTML files:${NC}"
    ls -1 *.html 2>/dev/null || echo "   No HTML files found"
    echo ""
    echo -e "${YELLOW}Please ensure the clinical dashboard is in the current directory.${NC}"
    read -p "Press Enter to exit..."
    exit 1
fi

# Check for templates
if [ -f "teams_chat_templates.txt" ]; then
    echo -e "   ${GREEN}✅ Teams chat templates ready${NC}"
else
    echo -e "   ${YELLOW}⚠️  Teams templates missing (optional)${NC}"
fi

if [ -f "professional_email_templates.md" ]; then
    echo -e "   ${GREEN}✅ Email templates prepared${NC}"
else
    echo -e "   ${YELLOW}⚠️  Email templates missing (optional)${NC}"
fi

echo ""

# Network configuration
PORT=8080
LOCAL_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "localhost")

echo -e "${YELLOW}🌐 Network Configuration:${NC}"
echo -e "   Local Access: http://localhost:$PORT"
echo -e "   Network Access: http://$LOCAL_IP:$PORT"
echo -e "   ${GREEN}Teams Compatible: Yes ✅${NC}"
echo -e "   ${GREEN}GDPR Compliant: Local hosting only ✅${NC}"
echo ""

# Teams sharing guide
echo -e "${BLUE}📢 TEAMS SHARING GUIDE:${NC}"
echo "1. Click 'Share Screen' in Teams meeting"
echo "2. Select 'Chrome/Browser Window'"
echo "3. Navigate to: http://localhost:$PORT"
echo "4. Copy chat message from teams_chat_templates.txt"
echo "5. Paste in Teams chat for 23 colleagues"
echo ""

echo -e "${YELLOW}🎯 READY TO LAUNCH CLINICAL DEMO!${NC}"
echo ""

read -p "Press Enter to start demo server, or 'q' to quit: " LAUNCH
if [ "$LAUNCH" = "q" ]; then
    echo -e "${YELLOW}Demo cancelled by user.${NC}"
    exit 0
fi

echo -e "${GREEN}🚀 Launching Clinical Demo Server...${NC}"
echo ""

# Function to check if port is available
check_port() {
    if command -v netstat >/dev/null 2>&1; then
        if netstat -tuln | grep ":$1 " >/dev/null; then
            return 1
        fi
    elif command -v ss >/dev/null 2>&1; then
        if ss -tuln | grep ":$1 " >/dev/null; then
            return 1
        fi
    fi
    return 0
}

# Check if port is available
if ! check_port $PORT; then
    echo -e "${YELLOW}⚠️  Port $PORT is already in use. Trying port $((PORT+1))...${NC}"
    PORT=$((PORT+1))
    if ! check_port $PORT; then
        echo -e "${RED}❌ Port $PORT is also in use. Please close other servers.${NC}"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Start HTTP server
echo -e "${GREEN}🌐 Starting HTTP server on port $PORT...${NC}"
echo -e "${CYAN}📊 Dashboard URL: http://localhost:$PORT${NC}"
echo -e "${CYAN}🔗 Direct URL: http://localhost:$PORT/$DASHBOARD_FILE${NC}"
echo ""

# Try different server options
if command -v python3 >/dev/null 2>&1; then
    echo -e "${GREEN}Using Python3 HTTP server...${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
    echo ""
    
    # Open browser if possible
    if command -v xdg-open >/dev/null 2>&1; then
        sleep 2 && xdg-open "http://localhost:$PORT/$DASHBOARD_FILE" &
    elif command -v open >/dev/null 2>&1; then
        sleep 2 && open "http://localhost:$PORT/$DASHBOARD_FILE" &
    fi
    
    # Start server
    cd "$(dirname "$0")" || exit
    python3 -m http.server $PORT --bind 127.0.0.1
    
elif command -v python >/dev/null 2>&1; then
    echo -e "${GREEN}Using Python HTTP server...${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
    echo ""
    
    # Open browser if possible
    if command -v xdg-open >/dev/null 2>&1; then
        sleep 2 && xdg-open "http://localhost:$PORT/$DASHBOARD_FILE" &
    elif command -v open >/dev/null 2>&1; then
        sleep 2 && open "http://localhost:$PORT/$DASHBOARD_FILE" &
    fi
    
    # Start server
    cd "$(dirname "$0")" || exit
    python -m SimpleHTTPServer $PORT 2>/dev/null || python -m http.server $PORT --bind 127.0.0.1
    
elif command -v node >/dev/null 2>&1; then
    echo -e "${GREEN}Using Node.js HTTP server...${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
    echo ""
    
    # Create temporary server script
    cat > temp_server.js << EOF
const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const server = http.createServer((req, res) => {
    let pathname = url.parse(req.url).pathname;
    
    if (pathname === '/') {
        pathname = '/$DASHBOARD_FILE';
    }
    
    const filePath = path.join(__dirname, pathname);
    
    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404);
            res.end('404 Not Found');
            return;
        }
        
        const ext = path.extname(filePath);
        let contentType = 'text/html';
        
        if (ext === '.css') contentType = 'text/css';
        else if (ext === '.js') contentType = 'application/javascript';
        else if (ext === '.json') contentType = 'application/json';
        
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(data);
    });
});

server.listen($PORT, '127.0.0.1', () => {
    console.log('L.I.F.E. Clinical Demo Server running on http://localhost:$PORT');
    console.log('Dashboard: http://localhost:$PORT/$DASHBOARD_FILE');
});
EOF
    
    # Open browser if possible
    if command -v xdg-open >/dev/null 2>&1; then
        sleep 2 && xdg-open "http://localhost:$PORT/$DASHBOARD_FILE" &
    elif command -v open >/dev/null 2>&1; then
        sleep 2 && open "http://localhost:$PORT/$DASHBOARD_FILE" &
    fi
    
    node temp_server.js
    rm -f temp_server.js
    
else
    echo -e "${RED}❌ No suitable HTTP server found!${NC}"
    echo ""
    echo -e "${YELLOW}💡 MANUAL ACCESS INSTRUCTIONS:${NC}"
    echo "1. Install Python: sudo apt install python3 (Linux) or brew install python3 (macOS)"
    echo "2. Or open the dashboard file directly in your browser:"
    echo "   file://$(pwd)/$DASHBOARD_FILE"
    echo ""
    echo -e "${CYAN}📋 TEAMS DEMO ALTERNATIVE:${NC}"
    echo "1. Open $DASHBOARD_FILE directly in Chrome/Firefox"
    echo "2. Share the browser window in Teams"
    echo "3. The dashboard will work without a server for basic functionality"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Server stopped
echo ""
echo -e "${GREEN}✅ Clinical Demo Server stopped${NC}"
echo -e "${CYAN}Thank you for using L.I.F.E. Platform!${NC}"
echo ""