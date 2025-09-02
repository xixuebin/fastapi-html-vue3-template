// 通用权限验证和错误处理工具

class AuthUtils {
    /**
     * 检查用户是否已登录
     * @param {string} apiEndpoint - 验证 API 端点
     * @returns {Promise<Object>} 用户信息或错误信息
     */
    static async checkLoginStatus(apiEndpoint) {
        try {
            const response = await fetch(apiEndpoint, {
                credentials: 'include'
            });
            
            if (response.status === 401) {
                // 用户未登录，重定向到登录页面
                window.location.href = '../login.html';
                return { loggedIn: false, error: '未登录' };
            }
            
            const data = await response.json();
            if (data.success) {
                return { loggedIn: true, username: data.username, data: data };
            } else {
                window.location.href = '../login.html';
                return { loggedIn: false, error: '验证失败' };
            }
        } catch (error) {
            console.error('检查登录状态时出错：', error);
            window.location.href = '../login.html';
            return { loggedIn: false, error: '网络错误' };
        }
    }
    
    /**
     * 处理 iframe 与父页面的通信
     * @param {Function} onUserInfoReceived - 接收到用户信息时的回调函数
     */
    static handleParentCommunication(onUserInfoReceived) {
        // 监听来自父页面的消息
        window.addEventListener('message', (event) => {
            if (event.data.type === 'USER_INFO') {
                // 接收父页面发送的用户信息
                if (onUserInfoReceived) {
                    onUserInfoReceived(event.data.username);
                }
            }
        });
        
        // 请求父页面发送用户信息
        if (window.parent && window.parent !== window) {
            window.parent.postMessage({type: 'GET_USER_INFO'}, '*');
        }
    }
    
    /**
     * 向父页面发送用户信息
     * @param {string} username - 用户名
     * @param {string} tabId - 标签页 ID（可选）
     */
    static sendUserInfoToChildren(username, tabId = null) {
        if (tabId) {
            // 向特定 iframe 发送信息
            const iframe = document.getElementById('iframe-' + tabId);
            if (iframe && iframe.contentWindow) {
                iframe.contentWindow.postMessage({
                    type: 'USER_INFO',
                    username: username
                }, '*');
            }
        } else {
            // 向所有 iframe 发送信息
            const iframes = document.querySelectorAll('iframe');
            iframes.forEach(iframe => {
                if (iframe.contentWindow) {
                    iframe.contentWindow.postMessage({
                        type: 'USER_INFO',
                        username: username
                    }, '*');
                }
            });
        }
    }
}

// 通用错误处理工具
class ErrorUtils {
    /**
     * 显示错误信息
     * @param {string} message - 错误信息
     * @param {string} type - 错误类型 ('error', 'warning', 'info')
     */
    static showError(message, type = 'error') {
        // 创建错误提示元素
        const errorDiv = document.createElement('div');
        errorDiv.className = `message-${type}`;
        errorDiv.textContent = message;
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 4px;
            color: white;
            font-size: 14px;
            z-index: 9999;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            ${type === 'error' ? 'background: #f44336;' : ''}
            ${type === 'warning' ? 'background: #ff9800;' : ''}
            ${type === 'info' ? 'background: #2196f3;' : ''}
        `;
        
        // 添加到页面
        document.body.appendChild(errorDiv);
        
        // 3 秒后自动移除
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 3000);
    }
}

// 通用页面模板
class PageTemplate {
    /**
     * 创建标准页面结构
     * @param {string} title - 页面标题
     * @param {string} content - 页面内容 HTML
     * @returns {string} 完整页面 HTML
     */
    static createStandardPage(title, content) {
        return `
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>${title}</title>
    <link rel="stylesheet" href="/css/style.css">
    <script src="https://unpkg.com/vue@3"></script>
</head>
<body>
<div id="app">
    <div class="page-content">
        <h2>${title}</h2>
        ${content}
    </div>
</div>
<script src="/js/utils.js"></script>
<script>
const { createApp } = Vue;
createApp({
    data() {
        return {
            username: ''
        }
    },
    async mounted() {
        // 检查用户登录状态
        const authResult = await AuthUtils.checkLoginStatus('/api/page'); // 需要根据具体页面修改 API 端点
        
        if (authResult.loggedIn) {
            this.username = authResult.username;
        }
        
        // 处理与父页面的通信
        AuthUtils.handleParentCommunication((username) => {
            this.username = username;
        });
    }
}).mount('#app');
</script>
</body>
</html>
        `;
    }
}