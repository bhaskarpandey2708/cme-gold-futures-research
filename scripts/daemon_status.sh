#!/usr/bin/env bash
# ==============================================================================
# CME Gold Quantitative Microstructure Suite - Daemon Status Monitor
# ==============================================================================

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     🥇 CME GOLD FUTURES RESEARCH — LIVE DAEMON STATUS MONITOR               ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
echo -e " Timestamp: ${BOLD}$(date -u '+%Y-%m-%d %H:%M:%S UTC')${NC} | Local: $(date '+%Y-%m-%d %I:%M:%S %p %Z')"
echo ""

# 1. Background Daemons Status
echo -e "${BOLD}▶ 1. ACTIVE SYSTEM DAEMONS${NC}"
echo "--------------------------------------------------------------------------------"
printf "%-28s %-8s %-8s %-8s %-8s %-12s %s\n" "DAEMON NAME" "STATUS" "PID" "CPU %" "MEM (MB)" "ELAPSED" "COMMAND"
echo "--------------------------------------------------------------------------------"

check_process() {
    local name="$1"
    local pattern="$2"
    local pid=$(pgrep -f "$pattern" | grep -v "$$" | head -n 1)

    if [ -n "$pid" ]; then
        local stats=$(ps -p "$pid" -o %cpu,rss,etime,args 2>/dev/null | tail -n +2)
        if [ -n "$stats" ]; then
            local cpu=$(echo "$stats" | awk '{print $1}')
            local rss_kb=$(echo "$stats" | awk '{print $2}')
            local rss_mb=$(awk "BEGIN {printf \"%.1f\", $rss_kb/1024}")
            local etime=$(echo "$stats" | awk '{print $3}')
            local cmd=$(echo "$stats" | awk '{$1=$2=$3=""; print $0}' | sed -e 's/^[ \t]*//' | cut -c 1-28)
            printf "%-28s ${GREEN}%-8s${NC} %-8s %-8s %-8s %-12s %s...\n" "$name" "ACTIVE" "$pid" "$cpu%" "$rss_mb" "$etime" "$cmd"
        else
            printf "%-28s ${RED}%-8s${NC} %-8s %-8s %-8s %-12s %s\n" "$name" "DEAD" "-" "-" "-" "-" "-"
        fi
    else
        printf "%-28s ${RED}%-8s${NC} %-8s %-8s %-8s %-12s %s\n" "$name" "STOPPED" "-" "-" "-" "-" "-"
    fi
}

check_process "Continuous Harvester" "harvest_continuous_gold.py"
check_process "Google Drive Sync" "chat_convo_sync.py"
check_process "Enterprise Decision Daemon" "enterprise_decision_daemon.py"
check_process "REST & WS Server (8085)" "quant_api_server.py"
check_process "CME FIX 4.4 Gateway (9800)" "fix_protocol_gateway.py"
check_process "Unified Cockpit (8090)" "unified_quant_cockpit_server.py"
echo "--------------------------------------------------------------------------------"
echo ""

# 2. Live Harvest Storage Status
echo -e "${BOLD}▶ 2. RECENT HARVEST ACTIVITY (Data Partition)${NC}"
echo "--------------------------------------------------------------------------------"
TODAY_DIR="$BASE_DIR/data/harvested/$(date -u +%Y-%m-%d)"
if [ -d "$TODAY_DIR" ]; then
    echo -e " Today's Partition: ${CYAN}$TODAY_DIR${NC}"
    ls -lh "$TODAY_DIR"/*.parquet 2>/dev/null | awk '{printf "   • %-45s  Size: %6s  Time: %s\n", $9, $5, $8}'
else
    echo -e " ${YELLOW}Waiting for today's partition flush ($TODAY_DIR)...${NC}"
fi
echo ""

# 3. SQLite Market Store Health
echo -e "${BOLD}▶ 3. SQLITE MARKET STORE STATUS${NC}"
echo "--------------------------------------------------------------------------------"
DB_FILE="$BASE_DIR/data/market_store.db"
if [ -f "$DB_FILE" ]; then
    DB_SIZE=$(ls -lh "$DB_FILE" | awk '{print $5}')
    echo -e " Database Path: ${CYAN}$DB_FILE${NC} (Size: ${BOLD}$DB_SIZE${NC})"
    python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('file:$DB_FILE?mode=ro', uri=True)
    cursor = conn.cursor()
    cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\")
    tables = [r[0] for r in cursor.fetchall() if not r[0].startswith('sqlite_')]
    print(f'   • Registered Market Tables: {len(tables)} tables')
    for t in sorted(tables):
        print(f'     - {t}')
    conn.close()
except Exception as e:
    print(f'   Error reading SQLite: {e}')
"
else
    echo -e " ${RED}Database file not found at $DB_FILE${NC}"
fi
echo "================================================================================"
echo -e "${BOLD}💡 Master CLI Controls:${NC}"
echo -e "  • ${GREEN}Inspect status:${NC}     python3 manage.py status"
echo -e "  • ${GREEN}Inspect PnL:${NC}        python3 manage.py pnl"
echo -e "  • ${YELLOW}Start all daemons:${NC} python3 manage.py start"
echo -e "  • ${RED}Stop all daemons:${NC}  python3 manage.py stop"
echo "================================================================================"
