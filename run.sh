#!/bin/bash

# 定义颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 定义变量
APP_NAME="aad-offer-ops"
PID_FILE=".pid"
LOG_FILE="app.log"
APP_PORT=8000

# 检查系统是否支持systemd
has_systemd() {
    if command -v systemctl >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# 启动应用
start() {
    echo -e "${BLUE}正在启动 ${APP_NAME}...${NC}"

    # 检查服务是否已经在运行
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo -e "${YELLOW}服务已经在运行，PID: $PID${NC}"
            return
        else
            # 如果PID文件存在但进程不存在，则删除PID文件
            rm -f "$PID_FILE"
        fi
    fi

    # 检查虚拟环境
    if [ -d ".venv" ]; then
        # 激活虚拟环境并启动应用
        echo -e "${GREEN}使用虚拟环境启动...${NC}"
        source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate 2>/dev/null
        nohup python main.py > "$LOG_FILE" 2>&1 &
    else
        # 直接使用系统Python启动应用
        echo -e "${YELLOW}未检测到虚拟环境，使用系统Python启动...${NC}"
        echo -e "${YELLOW}建议使用 ./init.sh 初始化项目环境${NC}"
        nohup python main.py > "$LOG_FILE" 2>&1 &
    fi

    # 保存PID
    PID=$!
    echo $PID > "$PID_FILE"

    echo -e "${GREEN}服务已启动，PID: $PID${NC}"
    echo -e "${GREEN}应用运行在 http://localhost:$APP_PORT${NC}"
    echo -e "${BLUE}日志文件: $LOG_FILE${NC}"
}

# 停止应用
stop() {
    echo -e "${BLUE}正在停止 ${APP_NAME}...${NC}"

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            # 杀掉进程
            kill "$PID"
            # 等待进程结束
            for i in {1..10}; do
                if ! ps -p "$PID" > /dev/null 2>&1; then
                    break
                fi
                sleep 1
            done

            # 如果进程还在运行，强制杀死
            if ps -p "$PID" > /dev/null 2>&1; then
                echo -e "${YELLOW}服务未能正常停止，正在强制终止...${NC}"
                kill -9 "$PID" > /dev/null 2>&1
            fi

            rm -f "$PID_FILE"
            echo -e "${GREEN}服务已停止${NC}"
        else
            echo -e "${YELLOW}服务不在运行，但PID文件存在，已清理${NC}"
            rm -f "$PID_FILE"
        fi
    else
        echo -e "${YELLOW}未找到PID文件，服务可能不在运行${NC}"
        # 尝试查找并杀死所有相关Python进程
        echo -e "${BLUE}尝试查找相关进程...${NC}"
        PIDS=$(ps aux | grep "python main.py" | grep -v grep | awk '{print $2}')
        if [ -n "$PIDS" ]; then
            echo -e "${YELLOW}找到相关进程: $PIDS${NC}"
            for PID in $PIDS; do
                kill "$PID" > /dev/null 2>&1
                echo -e "${GREEN}已停止进程 $PID${NC}"
            done
        else
            echo -e "${RED}未找到运行中的服务进程${NC}"
        fi
    fi
}

# 检查应用状态
status() {
    echo -e "${BLUE}检查 ${APP_NAME} 状态...${NC}"

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo -e "${GREEN}服务正在运行，PID: $PID${NC}"
            echo -e "${GREEN}应用运行在 http://localhost:$APP_PORT${NC}"

            # 显示运行时间
            RUNTIME=$(ps -o etime= -p "$PID")
            echo -e "${BLUE}运行时长: $RUNTIME${NC}"

            # 显示最近的日志
            if [ -f "$LOG_FILE" ]; then
                echo -e "${BLUE}最近日志 (最后10行):${NC}"
                tail -n 10 "$LOG_FILE"
            fi
        else
            echo -e "${RED}服务不在运行，但PID文件存在${NC}"
            rm -f "$PID_FILE"
        fi
    else
        echo -e "${RED}服务不在运行${NC}"
    fi

    # 显示系统资源使用情况
    echo -e "${BLUE}系统资源使用情况:${NC}"
    echo -e "${BLUE}CPU & 内存使用情况:${NC}"
    PROCESS_INFO=$(ps aux | grep "python main.py" | grep -v grep)
    if [ -n "$PROCESS_INFO" ]; then
        echo "$PROCESS_INFO" | awk '{printf "CPU: %s%%, 内存: %s%%\n", $3, $4}'
    else
        echo -e "${RED}未找到相关进程${NC}"
    fi
}

# 重启应用
restart() {
    echo -e "${BLUE}正在重启 ${APP_NAME}...${NC}"
    stop
    sleep 2
    start
}

# 显示帮助信息
show_help() {
    echo -e "${GREEN}AAD Offer Operations 服务管理脚本${NC}"
    echo -e "${BLUE}用法: $0 [选项]${NC}"
    echo -e "选项:"
    echo -e "  ${YELLOW}start${NC}     启动服务"
    echo -e "  ${YELLOW}stop${NC}      停止服务"
    echo -e "  ${YELLOW}restart${NC}   重启服务"
    echo -e "  ${YELLOW}status${NC}    查看服务状态"
    echo -e "  ${YELLOW}help${NC}      显示此帮助信息"
}

# 根据命令行参数执行不同功能
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac

exit 0
