/**
 * 分页组件 - 通用分页UI和逻辑
 * 用于优化大数据列表的性能
 */

class PaginationManager {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.container = document.getElementById(containerId);
        
        // 默认配置
        this.options = {
            perPage: 20,
            onPageChange: null,
            showInfo: true,
            showPageSize: true,
            pageSizeOptions: [5, 10, 20, 50, 100],
            ...options
        };
        
        // 分页状态
        this.currentPage = 1;
        this.perPage = this.options.perPage;
        this.total = 0;
        this.totalPages = 0;
        
        this.init();
    }
    
    init() {
        if (!this.container) {
            console.error(`分页容器 #${this.containerId} 不存在`);
            return;
        }
        
        this.container.className = 'pagination-container';
        this.render();
    }
    
    /**
     * 更新分页状态
     * @param {Object} paginationData - 服务器返回的分页数据
     */
    update(paginationData) {
        this.currentPage = paginationData.page;
        this.perPage = paginationData.per_page;
        this.total = paginationData.total;
        this.totalPages = paginationData.pages;
        
        this.render();
    }
    
    /**
     * 渲染分页UI
     */
    render() {
        if (this.total === 0) {
            this.container.innerHTML = '';
            return;
        }
        
        const html = `
            <div class="pagination-wrapper">
                ${this.options.showInfo ? this.renderInfo() : ''}
                ${this.options.showPageSize ? this.renderPageSize() : ''}
                ${this.renderPagination()}
            </div>
        `;
        
        this.container.innerHTML = html;
        this.bindEvents();
    }
    
    /**
     * 渲染信息部分
     */
    renderInfo() {
        const start = (this.currentPage - 1) * this.perPage + 1;
        const end = Math.min(this.currentPage * this.perPage, this.total);
        
        return `
            <div class="pagination-info">
                显示第 ${start}-${end} 条，共 ${this.total} 条记录
            </div>
        `;
    }
    
    /**
     * 渲染页面大小选择器
     */
    renderPageSize() {
        const options = this.options.pageSizeOptions
            .map(size => `<option value="${size}" ${size === this.perPage ? 'selected' : ''}>${size} 条/页</option>`)
            .join('');
        
        return `
            <div class="pagination-size">
                <select id="pageSizeSelect">
                    ${options}
                </select>
            </div>
        `;
    }
    
    /**
     * 渲染分页按钮
     */
    renderPagination() {
        if (this.totalPages <= 1) {
            return '<div class="pagination-nav"></div>';
        }
        
        let buttons = [];
        
        // 上一页按钮
        buttons.push(`
            <button class="pagination-btn ${this.currentPage === 1 ? 'disabled' : ''}" 
                    data-page="${this.currentPage - 1}" 
                    ${this.currentPage === 1 ? 'disabled' : ''}>
                <span>‹</span> 上一页
            </button>
        `);
        
        // 页码按钮
        const pageButtons = this.getPageButtons();
        buttons.push(...pageButtons);
        
        // 下一页按钮
        buttons.push(`
            <button class="pagination-btn ${this.currentPage === this.totalPages ? 'disabled' : ''}" 
                    data-page="${this.currentPage + 1}"
                    ${this.currentPage === this.totalPages ? 'disabled' : ''}>
                下一页 <span>›</span>
            </button>
        `);
        
        return `
            <div class="pagination-nav">
                ${buttons.join('')}
            </div>
        `;
    }
    
    /**
     * 获取页码按钮
     */
    getPageButtons() {
        const buttons = [];
        const delta = 2; // 当前页前后显示的页数
        
        // 总是显示第一页
        if (this.currentPage > delta + 2) {
            buttons.push(`
                <button class="pagination-btn" data-page="1">1</button>
                <span class="pagination-ellipsis">...</span>
            `);
        }
        
        // 显示当前页周围的页码
        const start = Math.max(1, this.currentPage - delta);
        const end = Math.min(this.totalPages, this.currentPage + delta);
        
        for (let i = start; i <= end; i++) {
            buttons.push(`
                <button class="pagination-btn ${i === this.currentPage ? 'active' : ''}" 
                        data-page="${i}">
                    ${i}
                </button>
            `);
        }
        
        // 总是显示最后一页
        if (this.currentPage < this.totalPages - delta - 1) {
            buttons.push(`
                <span class="pagination-ellipsis">...</span>
                <button class="pagination-btn" data-page="${this.totalPages}">${this.totalPages}</button>
            `);
        }
        
        return buttons;
    }
    
    /**
     * 绑定事件
     */
    bindEvents() {
        // 页码按钮点击
        this.container.querySelectorAll('.pagination-btn:not(.disabled)').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const page = parseInt(e.currentTarget.dataset.page);
                if (page && page !== this.currentPage) {
                    this.goToPage(page);
                }
            });
        });
        
        // 页面大小改变
        const pageSizeSelect = this.container.querySelector('#pageSizeSelect');
        if (pageSizeSelect) {
            pageSizeSelect.addEventListener('change', (e) => {
                this.perPage = parseInt(e.target.value);
                this.currentPage = 1; // 重置到第一页
                this.triggerChange();
            });
        }
    }
    
    /**
     * 跳转到指定页面
     */
    goToPage(page) {
        if (page < 1 || page > this.totalPages || page === this.currentPage) {
            return;
        }
        
        this.currentPage = page;
        this.triggerChange();
    }
    
    /**
     * 触发页面改变事件
     */
    triggerChange() {
        if (typeof this.options.onPageChange === 'function') {
            this.options.onPageChange({
                page: this.currentPage,
                perPage: this.perPage
            });
        }
    }
    
    /**
     * 获取当前分页参数
     */
    getParams() {
        return {
            page: this.currentPage,
            per_page: this.perPage
        };
    }
    
    /**
     * 重置分页
     */
    reset() {
        this.currentPage = 1;
        this.total = 0;
        this.totalPages = 0;
        this.render();
    }
}

// 导出到全局
window.PaginationManager = PaginationManager;
