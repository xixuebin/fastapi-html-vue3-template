#!/bin/bash

# 定义颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查Python版本
check_python_version() {
    echo -e "${BLUE}检查Python版本...${NC}"
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &>/dev/null; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}错误: 未找到Python${NC}"
        echo -e "${RED}请安装Python 3.13+后再运行此脚本${NC}"
        exit 1
    fi

    # 获取Python版本
    PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    PYTHON_MAJOR_VERSION=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
    PYTHON_MINOR_VERSION=$($PYTHON_CMD -c "import sys; print(sys.version_info.minor)")

    echo -e "${BLUE}检测到Python版本: $PYTHON_VERSION${NC}"

    # 检查Python版本是否满足要求
    if [ "$PYTHON_MAJOR_VERSION" -lt 3 ] || ([ "$PYTHON_MAJOR_VERSION" -eq 3 ] && [ "$PYTHON_MINOR_VERSION" -lt 8 ]); then
        echo -e "${YELLOW}警告: Python版本低于推荐的3.13+${NC}"
        echo -e "${YELLOW}某些功能可能无法正常工作${NC}"
        read -p "是否继续? [y/N] " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${RED}初始化已取消${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}Python版本符合要求${NC}"
    fi
}

# 创建虚拟环境
create_venv() {
    echo -e "${BLUE}正在创建虚拟环境...${NC}"
    if [ -d ".venv" ]; then
        echo -e "${YELLOW}虚拟环境已存在${NC}"
        read -p "是否重新创建? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}移除旧的虚拟环境...${NC}"
            rm -rf .venv
        else
            echo -e "${GREEN}使用现有虚拟环境${NC}"
            return
        fi
    fi

    $PYTHON_CMD -m venv .venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}创建虚拟环境失败${NC}"
        echo -e "${YELLOW}尝试安装venv模块...${NC}"
        $PYTHON_CMD -m pip install virtualenv
        $PYTHON_CMD -m virtualenv .venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}创建虚拟环境失败，请手动安装venv或virtualenv模块${NC}"
            exit 1
        fi
    fi
    echo -e "${GREEN}虚拟环境创建成功${NC}"
}

# 激活虚拟环境
activate_venv() {
    echo -e "${BLUE}正在激活虚拟环境...${NC}"
    # 尝试激活虚拟环境
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows
        source .venv/Scripts/activate
    else
        # Linux/macOS
        source .venv/bin/activate
    fi

    if [ $? -ne 0 ]; then
        echo -e "${RED}激活虚拟环境失败${NC}"
        exit 1
    fi
    echo -e "${GREEN}虚拟环境已激活${NC}"
}

# 安装依赖
install_dependencies() {
    echo -e "${BLUE}正在安装项目依赖...${NC}"

    # 升级pip
    echo -e "${BLUE}升级pip...${NC}"
    $PYTHON_CMD -m pip install --upgrade pip

    # 安装项目依赖
    if [ -f "requirements.txt" ]; then
        echo -e "${BLUE}从requirements.txt安装依赖...${NC}"
        $PYTHON_CMD -m pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo -e "${RED}安装依赖失败${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}未找到requirements.txt，安装基本依赖...${NC}"
        # 安装基本依赖
        $PYTHON_CMD -m pip install fastapi uvicorn pyyaml fastapi-mcp
    fi

    echo -e "${GREEN}依赖安装成功${NC}"
}

# 创建上传目录
create_upload_dir() {
    echo -e "${BLUE}检查上传目录...${NC}"
    if [ ! -d "uploads" ]; then
        echo -e "${BLUE}创建上传目录...${NC}"
        mkdir -p uploads
        echo -e "${GREEN}上传目录创建成功${NC}"
    else
        echo -e "${GREEN}上传目录已存在${NC}"
    fi
}

# 设置执行权限
set_permissions() {
    echo -e "${BLUE}设置文件权限...${NC}"
    chmod +x run.sh
    echo -e "${GREEN}已设置run.sh为可执行文件${NC}"
}

# 显示完成消息
show_completion() {
    echo -e "\n${GREEN}==========================================${NC}"
    echo -e "${GREEN}项目环境初始化完成!${NC}"
    echo -e "${GREEN}==========================================${NC}"
    echo -e "${BLUE}现在您可以使用以下命令启动服务:${NC}"
    echo -e "${YELLOW}./run.sh start${NC}"
    echo -e "\n${BLUE}使用以下命令查看更多选项:${NC}"
    echo -e "${YELLOW}./run.sh help${NC}"
    echo -e "${GREEN}==========================================${NC}"
}

# 主函数
main() {
    echo -e "${GREEN}==========================================${NC}"
    echo -e "${GREEN}AAD Offer Operations 项目环境初始化${NC}"
    echo -e "${GREEN}==========================================${NC}"

    check_python_version
    create_venv
    activate_venv
    install_dependencies
    create_upload_dir
    set_permissions
    show_completion
}

# 执行主函数
main
