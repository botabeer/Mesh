#!/bin/bash
# Bot Mesh - Docker Management Scripts
# Created by: Abeer Aldosari © 2025

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# ============================================
# 1. Build Image
# ============================================
build() {
    echo -e "${BLUE}🔨 Building Docker image...${NC}"
    docker build -t bot-mesh:latest .
    echo -e "${GREEN}✅ Image built successfully!${NC}"
}

# ============================================
# 2. Run Container (Simple)
# ============================================
run() {
    echo -e "${BLUE}🚀 Starting Bot Mesh...${NC}"
    
    if [ ! -f .env ]; then
        echo -e "${RED}❌ .env file not found!${NC}"
        echo "Please create .env file first:"
        echo "cp .env.example .env"
        exit 1
    fi
    
    docker run -d \
        --name bot-mesh \
        -p 5000:5000 \
        --env-file .env \
        -v $(pwd)/data:/app/data \
        --restart unless-stopped \
        bot-mesh:latest
    
    echo -e "${GREEN}✅ Bot Mesh is running!${NC}"
    echo "View logs: docker logs -f bot-mesh"
}

# ============================================
# 3. Run with Docker Compose
# ============================================
compose_up() {
    echo -e "${BLUE}🚀 Starting with Docker Compose...${NC}"
    docker-compose up -d
    echo -e "${GREEN}✅ All services started!${NC}"
    echo ""
    echo "Services:"
    docker-compose ps
}

# ============================================
# 4. Stop Containers
# ============================================
stop() {
    echo -e "${YELLOW}⏹️  Stopping containers...${NC}"
    if docker ps -q -f name=bot-mesh > /dev/null 2>&1; then
        docker stop bot-mesh
        echo -e "${GREEN}✅ Stopped!${NC}"
    else
        echo -e "${YELLOW}No running containers found${NC}"
    fi
}

# ============================================
# 5. Stop Docker Compose
# ============================================
compose_down() {
    echo -e "${YELLOW}⏹️  Stopping Docker Compose...${NC}"
    docker-compose down
    echo -e "${GREEN}✅ Stopped!${NC}"
}

# ============================================
# 6. View Logs
# ============================================
logs() {
    echo -e "${BLUE}📋 Viewing logs...${NC}"
    docker logs -f bot-mesh
}

# ============================================
# 7. Restart Container
# ============================================
restart() {
    echo -e "${YELLOW}🔄 Restarting...${NC}"
    docker restart bot-mesh
    echo -e "${GREEN}✅ Restarted!${NC}"
}

# ============================================
# 8. Clean Up
# ============================================
clean() {
    echo -e "${YELLOW}🧹 Cleaning up...${NC}"
    
    # Stop and remove container
    docker stop bot-mesh 2>/dev/null || true
    docker rm bot-mesh 2>/dev/null || true
    
    # Remove image
    read -p "Remove image too? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker rmi bot-mesh:latest 2>/dev/null || true
    fi
    
    echo -e "${GREEN}✅ Cleaned!${NC}"
}

# ============================================
# 9. Shell Access
# ============================================
shell() {
    echo -e "${BLUE}💻 Opening shell...${NC}"
    docker exec -it bot-mesh /bin/bash
}

# ============================================
# 10. Status Check
# ============================================
status() {
    echo -e "${BLUE}📊 Container Status:${NC}"
    echo ""
    
    if docker ps -q -f name=bot-mesh > /dev/null 2>&1; then
        docker ps -f name=bot-mesh --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        echo ""
        echo -e "${GREEN}✅ Bot is running${NC}"
        
        # Health check
        echo ""
        echo "Health Check:"
        curl -s http://localhost:5000/health | python3 -m json.tool 2>/dev/null || echo "Unable to reach health endpoint"
    else
        echo -e "${RED}❌ Bot is not running${NC}"
    fi
}

# ============================================
# 11. Quick Deploy
# ============================================
deploy() {
    echo -e "${BLUE}🚀 Quick Deploy${NC}"
    echo ""
    
    # Build
    build
    echo ""
    
    # Stop old container
    stop
    echo ""
    
    # Remove old container
    docker rm bot-mesh 2>/dev/null || true
    echo ""
    
    # Run new container
    run
    echo ""
    
    # Show status
    sleep 3
    status
}

# ============================================
# 12. Full Rebuild
# ============================================
rebuild() {
    echo -e "${BLUE}🔄 Full Rebuild${NC}"
    echo ""
    
    # Stop and clean
    clean
    echo ""
    
    # Build fresh
    docker build --no-cache -t bot-mesh:latest .
    echo ""
    
    # Run
    run
    echo ""
    
    # Status
    sleep 3
    status
}

# ============================================
# Main Menu
# ============================================
show_menu() {
    echo "════════════════════════════════════"
    echo "   🎮 Bot Mesh - Docker Manager"
    echo "════════════════════════════════════"
    echo ""
    echo "1)  build       - Build image"
    echo "2)  run         - Run container"
    echo "3)  stop        - Stop container"
    echo "4)  restart     - Restart container"
    echo "5)  logs        - View logs"
    echo "6)  status      - Check status"
    echo "7)  shell       - Open shell"
    echo "8)  clean       - Clean up"
    echo "9)  deploy      - Quick deploy"
    echo "10) rebuild     - Full rebuild"
    echo ""
    echo "Docker Compose:"
    echo "11) up          - Start with compose"
    echo "12) down        - Stop compose"
    echo ""
    echo "q) Quit"
    echo ""
    echo "════════════════════════════════════"
}

# ============================================
# Command Handler
# ============================================
case "${1}" in
    build)
        build
        ;;
    run)
        run
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    status)
        status
        ;;
    shell)
        shell
        ;;
    clean)
        clean
        ;;
    deploy)
        deploy
        ;;
    rebuild)
        rebuild
        ;;
    up)
        compose_up
        ;;
    down)
        compose_down
        ;;
    *)
        show_menu
        ;;
esac
