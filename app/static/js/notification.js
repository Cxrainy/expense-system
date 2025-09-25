/**
 * 通知系统 JavaScript 文件
 * 提供统一的通知功能，包括获取、显示、标记已读等
 */

class NotificationManager {
    constructor() {
        this.notifications = [];
        this.unreadCount = 0;
        this.isDropdownOpen = false;
        this.init();
    }

    init() {
        this.createNotificationElements();
        this.bindEvents();
        this.loadNotifications();
        this.loadUnreadCount();
        
        // 定期更新未读计数
        setInterval(() => {
            this.loadUnreadCount();
        }, 30000); // 30秒更新一次
    }

    createNotificationElements() {
        const notificationBtn = document.querySelector('.notification-btn');
        if (!notificationBtn) return;

        // 创建通知包装器
        const wrapper = document.createElement('div');
        wrapper.className = 'notification-wrapper';
        
        // 移动原按钮到包装器中
        notificationBtn.parentNode.insertBefore(wrapper, notificationBtn);
        wrapper.appendChild(notificationBtn);

        // 添加未读计数徽章
        const badge = document.createElement('span');
        badge.className = 'notification-badge hidden';
        badge.id = 'notificationBadge';
        wrapper.appendChild(badge);

        // 创建下拉菜单
        const dropdown = document.createElement('div');
        dropdown.className = 'notification-dropdown';
        dropdown.id = 'notificationDropdown';
        dropdown.innerHTML = `
            <div class="notification-header">
                <h4 class="notification-title">通知</h4>
                <a href="#" class="mark-all-read" id="markAllRead">全部已读</a>
            </div>
            <div class="notification-list" id="notificationList">
                <div class="loading-state">
                    <div class="loading-spinner"></div>
                    <span>加载中...</span>
                </div>
            </div>
        `;
        wrapper.appendChild(dropdown);
    }

    bindEvents() {
        const notificationBtn = document.querySelector('.notification-btn');
        const markAllReadBtn = document.getElementById('markAllRead');
        
        if (notificationBtn) {
            notificationBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleDropdown();
            });
        }

        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.markAllAsRead();
            });
        }

        // 点击其他地方关闭下拉菜单
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.notification-wrapper')) {
                this.closeDropdown();
            }
        });
    }

    async loadNotifications() {
        try {
            const response = await fetch('/api/notifications?limit=20');
            if (response.status === 401) {
                console.log('用户未登录');
                return;
            }
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.notifications = await response.json();
            this.renderNotifications();
        } catch (error) {
            console.error('加载通知失败:', error);
            this.renderError();
        }
    }

    async loadUnreadCount() {
        try {
            const response = await fetch('/api/notifications/unread-count');
            if (response.status === 401) {
                return;
            }
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.unreadCount = data.count;
            this.updateBadge();
        } catch (error) {
            console.error('加载未读计数失败:', error);
        }
    }

    updateBadge() {
        const badge = document.getElementById('notificationBadge');
        if (!badge) return;

        if (this.unreadCount > 0) {
            badge.textContent = this.unreadCount > 99 ? '99+' : this.unreadCount;
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }
    }

    renderNotifications() {
        const listContainer = document.getElementById('notificationList');
        if (!listContainer) return;

        if (this.notifications.length === 0) {
            listContainer.innerHTML = `
                <div class="notification-empty">
                    <div class="notification-empty-icon">🔔</div>
                    <h4>暂无通知</h4>
                    <p>您当前没有任何通知消息</p>
                </div>
            `;
            return;
        }

        const html = this.notifications.map(notification => {
            const isUnread = !notification.is_read;
            const timeAgo = this.formatTimeAgo(notification.created_at);
            
            return `
                <div class="notification-item ${isUnread ? 'unread' : ''}" 
                     data-id="${notification.id}" 
                     data-expense-id="${notification.related_expense_id || ''}">
                    <div class="notification-content">
                        <h4>${this.escapeHtml(notification.title)}</h4>
                        <p>${this.escapeHtml(notification.message)}</p>
                        <div class="notification-meta">
                            <span class="notification-time">${timeAgo}</span>
                            <span class="notification-type ${notification.type}">${this.getTypeText(notification.type)}</span>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        listContainer.innerHTML = html;

        // 绑定点击事件
        listContainer.querySelectorAll('.notification-item').forEach(item => {
            item.addEventListener('click', () => {
                this.handleNotificationClick(item);
            });
        });
    }

    renderError() {
        const listContainer = document.getElementById('notificationList');
        if (!listContainer) return;

        listContainer.innerHTML = `
            <div class="notification-empty">
                <div class="notification-empty-icon">⚠️</div>
                <h4>加载失败</h4>
                <p>无法加载通知，请稍后重试</p>
            </div>
        `;
    }

    async handleNotificationClick(item) {
        const notificationId = item.dataset.id;
        const expenseId = item.dataset.expenseId;
        const isUnread = item.classList.contains('unread');

        // 标记为已读
        if (isUnread) {
            await this.markAsRead(notificationId);
            item.classList.remove('unread');
            this.unreadCount = Math.max(0, this.unreadCount - 1);
            this.updateBadge();
        }

        // 如果有关联的报销申请，跳转到详情页
        if (expenseId) {
            window.location.href = `/expense/${expenseId}`;
        }

        this.closeDropdown();
    }

    async markAsRead(notificationId) {
        try {
            const response = await fetch(`/api/notifications/${notificationId}/read`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        } catch (error) {
            console.error('标记已读失败:', error);
        }
    }

    async markAllAsRead() {
        try {
            const response = await fetch('/api/notifications/mark-all-read', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // 更新UI
            document.querySelectorAll('.notification-item.unread').forEach(item => {
                item.classList.remove('unread');
            });

            this.unreadCount = 0;
            this.updateBadge();

        } catch (error) {
            console.error('标记全部已读失败:', error);
        }
    }

    toggleDropdown() {
        const dropdown = document.getElementById('notificationDropdown');
        if (!dropdown) return;

        if (this.isDropdownOpen) {
            this.closeDropdown();
        } else {
            this.openDropdown();
        }
    }

    openDropdown() {
        const dropdown = document.getElementById('notificationDropdown');
        if (!dropdown) return;

        dropdown.classList.add('show');
        this.isDropdownOpen = true;
        
        // 重新加载通知
        this.loadNotifications();
    }

    closeDropdown() {
        const dropdown = document.getElementById('notificationDropdown');
        if (!dropdown) return;

        dropdown.classList.remove('show');
        this.isDropdownOpen = false;
    }

    formatTimeAgo(dateString) {
        const now = new Date();
        const date = new Date(dateString);
        const diffInSeconds = Math.floor((now - date) / 1000);

        if (diffInSeconds < 60) {
            return '刚刚';
        } else if (diffInSeconds < 3600) {
            const minutes = Math.floor(diffInSeconds / 60);
            return `${minutes}分钟前`;
        } else if (diffInSeconds < 86400) {
            const hours = Math.floor(diffInSeconds / 3600);
            return `${hours}小时前`;
        } else if (diffInSeconds < 2592000) {
            const days = Math.floor(diffInSeconds / 86400);
            return `${days}天前`;
        } else {
            return date.toLocaleDateString('zh-CN');
        }
    }

    getTypeText(type) {
        const typeMap = {
            'success': '成功',
            'error': '错误',
            'warning': '警告',
            'info': '信息'
        };
        return typeMap[type] || '信息';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // 公开方法：刷新通知
    refresh() {
        this.loadNotifications();
        this.loadUnreadCount();
    }

    // 公开方法：显示新通知（用于实时通知）
    showNewNotification(notification) {
        // 可以在这里添加实时通知显示逻辑
        console.log('新通知:', notification);
        this.loadUnreadCount();
    }
}

// 全局初始化
let notificationManager;

document.addEventListener('DOMContentLoaded', function() {
    // 只在有通知按钮的页面初始化
    if (document.querySelector('.notification-btn')) {
        notificationManager = new NotificationManager();
        
        // 将实例暴露到全局，便于其他地方调用
        window.notificationManager = notificationManager;
    }
});