// 工具函数库

// API 请求封装
const api = {
    // GET 请求
    async get(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('GET request failed:', error);
            throw error;
        }
    },

    // POST 请求
    async post(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('POST request failed:', error);
            throw error;
        }
    },

    // PUT 请求
    async put(url, data) {
        try {
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('PUT request failed:', error);
            throw error;
        }
    },

    // DELETE 请求
    async delete(url) {
        try {
            const response = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('DELETE request failed:', error);
            throw error;
        }
    }
};

// 通用功能函数
const utils = {
    // 格式化日期
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-CN');
    },

    // 格式化金额（支持多货币）
    formatAmount(amount, currency = 'USD') {
        const currencySymbols = {
            'CNY': '¥',
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'KRW': '₩',
            'HKD': 'HK$',
            'SGD': 'S$',
            'AUD': 'A$',
            'CAD': 'C$'
        };
        
        const symbol = currencySymbols[currency] || currency;
        const formattedAmount = parseFloat(amount).toLocaleString('zh-CN', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
        
        return `${symbol} ${formattedAmount}`;
    },
    
    // 格式化多货币金额显示（原币种 + 美元）
    formatMultiCurrencyAmount(originalAmount, currency, usdAmount) {
        if (currency === 'USD') {
            return this.formatAmount(originalAmount, currency);
        }
        
        const originalFormatted = this.formatAmount(originalAmount, currency);
        const usdFormatted = this.formatAmount(usdAmount, 'USD');
        
        return `${originalFormatted} (≈ ${usdFormatted})`;
    },

    // 显示消息提示
    showMessage(message, type = 'info') {
        // 创建提示元素
        const messageEl = document.createElement('div');
        messageEl.className = `alert alert-${type}`;
        messageEl.textContent = message;
        messageEl.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 300px;
            padding: 12px 16px;
            border-radius: 6px;
            box-shadow: var(--shadow-lg);
            animation: slideInRight 0.3s ease-out;
        `;

        // 添加样式
        if (type === 'success') {
            messageEl.style.backgroundColor = '#f0f9ff';
            messageEl.style.color = '#10b981';
            messageEl.style.borderColor = '#10b981';
        } else if (type === 'error') {
            messageEl.style.backgroundColor = '#fef2f2';
            messageEl.style.color = '#ef4444';
            messageEl.style.borderColor = '#ef4444';
        }

        document.body.appendChild(messageEl);

        // 3秒后自动移除
        setTimeout(() => {
            messageEl.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                if (messageEl.parentNode) {
                    messageEl.parentNode.removeChild(messageEl);
                }
            }, 300);
        }, 3000);
    },

    // 确认对话框
    async confirm(message) {
        return new Promise((resolve) => {
            const result = window.confirm(message);
            resolve(result);
        });
    },

    // 获取状态中文文本
    getStatusText(status) {
        const statusMap = {
            'pending': '待审批',
            'approved': '已通过',
            'rejected': '已拒绝'
        };
        return statusMap[status] || status;
    },

    // 获取状态样式类
    getStatusClass(status) {
        const classMap = {
            'pending': 'badge-warning',
            'approved': 'badge-success',
            'rejected': 'badge-danger'
        };
        return classMap[status] || 'badge-secondary';
    },

    // 防抖函数
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// 添加动画CSS
const animationCSS = `
@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes slideOutRight {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}
`;

// 注入动画样式
if (!document.getElementById('utils-animations')) {
    const style = document.createElement('style');
    style.id = 'utils-animations';
    style.textContent = animationCSS;
    document.head.appendChild(style);
}