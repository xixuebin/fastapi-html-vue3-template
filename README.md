# AD Offer Operations 后台管理系统

这是一个基于 FastAPI 框架开发的 Offer 管理后台系统，提供了用户认证、页面访问控制、文件管理等功能。该项目采用前后端分离设计，后端使用 FastAPI 提供 API 服务，前端使用 HTML、CSS、JavaScript 以及 Vue.js 实现用户界面。

## 功能特点

- **用户认证系统**：支持基于会话的登录认证和 API Token 认证
- **权限控制**：提供细粒度的访问控制，确保资源安全
- **文件管理**：支持文件上传、下载和管理功能
- **Offer 管理**：支持 Offer 的创建、列表查看等功能
- **响应式布局**：支持多种设备屏幕大小
- **可扩展架构**：模块化设计，便于扩展功能

## 技术栈

### 后端

- **Python 3.13+**
- **FastAPI 0.116.1+**：高性能的现代化 Web 框架
- **Starlette 0.47.3+**：轻量级 ASGI 框架
- **Uvicorn 0.35.0+**：快速的 ASGI 服务器
- **PyYAML 6.0.2+**：YAML 文件解析
- **Pydantic 2.11.7+**：数据验证和设置管理

### 前端

- **Vue.js 3**：渐进式 JavaScript 框架
- **原生 JavaScript**
- **HTML5/CSS3**

## 项目结构

```
.
├── config.yaml            # 配置文件：用户、API令牌、菜单等
├── init.sh               # 环境初始化脚本
├── main.py               # 应用入口点
├── requirements.txt      # Python依赖
├── run.sh                # 服务管理脚本
├── src/                  # 源代码目录
│   └── com/offer/ops/    
│       ├── controller/   # 控制器
│       ├── middleware/   # 中间件
│       ├── security/     # 安全相关代码
│       └── service/      # 业务逻辑服务
├── static/               # 静态资源
│   ├── css/              # 样式文件
│   ├── js/               # JavaScript文件
│   ├── offer/            # Offer相关页面
│   └── *.html            # 主页面文件
└── uploads/              # 上传文件存储目录
```

## 快速开始

### 系统要求

- Python 3.13+ (推荐)
- pip (Python 包管理器)
- Linux/macOS/Windows系统

### 使用初始化脚本（推荐）

我们提供了一个初始化脚本来简化环境设置过程：

```bash
# 1. 设置执行权限
chmod +x init.sh

# 2. 运行初始化脚本
./init.sh
```

此脚本会自动执行以下操作：
- 检查 Python 版本
- 创建虚拟环境
- 安装所有依赖项
- 创建必要的目录
- 设置文件权限

### 手动安装步骤

如果您不想使用初始化脚本，可以按照以下步骤手动设置环境：

1. **克隆仓库**

```bash
git clone https://github.com/your-username/aad-offer-ops.git
cd aad-offer-ops
```

2. **创建并激活虚拟环境（推荐）**

```bash
# 在Linux/macOS上
python -m venv .venv
source .venv/bin/activate

# 在Windows上
python -m venv .venv
.venv\Scripts\activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **确保上传目录存在**

```bash
mkdir -p uploads
```

### 服务管理

我们提供了一个服务管理脚本，用于控制应用的运行状态：

```bash
# 设置执行权限
chmod +x run.sh

# 启动服务
./run.sh start

# 停止服务
./run.sh stop

# 重启服务
./run.sh restart

# 查看服务状态
./run.sh status

# 查看帮助信息
./run.sh help
```

服务启动后，将在 http://localhost:8000 上运行。

### 手动启动应用

如果不使用服务管理脚本，也可以直接启动应用：

```bash
# 激活虚拟环境（如果使用）
source .venv/bin/activate  # Linux/macOS
# 或者
.venv\Scripts\activate     # Windows

# 启动应用
python main.py

# 或者使用uvicorn
uvicorn main:app --reload
```

### 默认账号

系统自带两个默认账户（在 config.yaml 中配置）：

- 管理员账户：admin / admin123
- 测试账户：test / test123

## 配置说明

系统配置文件为`config.yaml`，主要包含以下配置项：

### 用户配置

```yaml
users:
  - username: admin
    password: admin123
  - username: test
    password: test123
```

### API 令牌

用于非登录状态下的 API 访问：

```yaml
api_token: "sk-1234567890abcdef"
```

### 菜单配置

```yaml
menus:
  - id: welcome
    title: 主页
    url: /welcome.html
    icon: home
    default: true
  # 更多菜单项...
```

## API 文档

系统启动后，可以通过以下 URL 访问自动生成的 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 认证机制

系统支持两种认证方式：

### 1. 会话认证（用于 Web 页面）

- 用户通过`/api/login`接口登录
- 系统创建会话并在 Cookie 中存储会话 ID
- 用户可以通过`/api/logout`接口登出

### 2. API 令牌认证（用于 API 访问）

- 客户端在请求头中提供`X-API-Token`
- 系统验证令牌的有效性
- 适用于第三方系统集成或自动化脚本

## 核心模块

### 认证模块 (`auth.py`)

提供了用户认证和权限验证的装饰器和依赖项：

- `requires_login()`：要求用户登录的装饰器
- `requires_api_token()`：要求 API 令牌的装饰器
- `verify_login()`：用于 FastAPI 依赖注入的登录验证函数
- `verify_api_token()`：用于 FastAPI 依赖注入的 API 令牌验证函数

### 静态文件中间件 (`static_middleware.py`)

处理静态文件请求，实现以下功能：

- 对受保护的静态资源进行登录验证
- 未登录用户会被重定向到登录页面
- 允许指定部分路径无需登录即可访问

### 文件管理 (`offer_files_controller.py`)

提供文件上传、下载和管理功能：

- 文件上传：`/api/files/upload`
- 文件列表：`/api/files`
- 文件下载：`/files/download/{filename}`
- 文件删除：`/api/files/{filename}`

## 前端结构

前端页面位于`static/`目录，主要包括：

- `index.html`: 主页面框架，包含导航菜单和标签页管理
- `login.html`: 登录页面
- `welcome.html`, `page1.html`, `page2.html`: 基本内容页面
- `offer/create.html`, `offer/list.html`: Offer 管理页面
- `offer/files.html`: 文件管理页面

## 如何扩展功能

### 添加新的 API 端点

1. 在`src/com/offer/ops/controller/`目录下创建新的控制器文件
2. 定义路由器并添加路由处理函数
3. 在`main.py`中导入并注册新的路由器

例如：

```python
# 创建新控制器 new_feature_controller.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.com.offer.ops.security.auth import requires_login

router = APIRouter()

@router.get("/api/new-feature", response_class=JSONResponse)
@requires_login()
async def get_new_feature(request: Request):
    return {"message": "这是一个新功能"}

# 在 main.py 中添加
from src.com.offer.ops.controller.new_feature_controller import router as new_feature_router
app.include_router(new_feature_router)
```

### 添加新的页面

1. 在`static/`目录或适当的子目录中创建新的 HTML 文件
2. 在`config.yaml`的菜单配置中添加新页面

例如：

```yaml
menus:
  # 已有菜单...
  - id: new_feature
    title: 新功能
    url: /new-feature.html
    icon: star
```

### 修改认证规则

认证规则在`src/com/offer/ops/security/auth.py`中定义，可以根据需要修改现有装饰器或添加新的装饰器。

## 安全建议

对于生产环境，请考虑以下安全增强措施：

1. 更改`config.yaml`中的默认密码和 API 令牌
2. 考虑使用环境变量或更安全的方式存储敏感信息
3. 将会话中间件的密钥 (`secret_key`) 设置为强随机值
4. 实施 HTTPS
5. 考虑添加请求速率限制
6. 实现更强大的密码存储机制（如密码哈希）

## 故障排除

### 常见问题

1. **无法启动应用**
   - 确保所有依赖已正确安装
   - 检查端口 8000 是否被占用

2. **登录失败**
   - 验证 config.yaml 中的用户凭据
   - 检查会话中间件是否正确配置

3. **静态文件无法访问**
   - 确保文件路径正确
   - 检查静态文件中间件配置

### 日志记录

系统日志可以帮助诊断问题。可以在启动应用时启用详细日志：

```bash
uvicorn main:app --log-level debug
```

## 贡献指南

欢迎贡献代码、提出问题或建议！请遵循以下步骤：

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

## 许可证

该项目采用[MIT 许可证](LICENSE)。

## 联系方式

有问题或建议？请通过以下方式联系我们：

- GitHub Issue: [创建 issue](https://github.com/your-username/aad-offer-ops/issues)
- Email: your-email@example.com
