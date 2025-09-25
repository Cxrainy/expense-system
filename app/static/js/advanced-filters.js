/**
 * 高级筛选组件
 * 提供统一的筛选功能，支持多种筛选条件和组合
 */
class AdvancedFilters {
    constructor(containerId, config = {}) {
        this.container = document.getElementById(containerId);
        this.config = {
            title: '高级筛选',
            collapsed: false,
            showQuickFilters: true,
            showSearch: true,
            showSavedFilters: true,
            enableCompoundFilters: false,
            // 新增：URL筛选自动保存为方案
            autoSaveUrlFilters: true,
            urlFilterNamePrefix: 'URL筛选',
            fields: [],
            quickFilters: [],
            onFilterChange: () => {},
            onSearch: () => {},
            ...config
        };
        
        this.currentFilters = {};
        this.activeQuickFilter = null;
        this.savedFilters = this.loadSavedFilters();
        this.searchTimer = null;
        
        this.init();
    }
    
    init() {
        this.render();
        this.bindEvents();
        // 不在初始化时立即加载默认筛选器，避免与外部设置的筛选条件冲突
        // this.loadDefaultFilters();
    }
    
    render() {
        this.container.innerHTML = `
            <div class="advanced-filters">
                <div class="filters-header">
                    <h3 class="filters-title">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M22 3H2l8 9.46V19l4 2v-8.54L22 3z"/>
                        </svg>
                        ${this.config.title}
                    </h3>
                    <button class="filters-toggle ${this.config.collapsed ? 'collapsed' : ''}" data-action="toggle">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="6,9 12,15 18,9"/>
                        </svg>
                    </button>
                </div>
                <div class="filters-content ${this.config.collapsed ? 'collapsed' : ''}">
                    <div class="filters-body">
                        ${this.config.showSearch ? this.renderSearchBox() : ''}
                        ${this.config.showQuickFilters ? this.renderQuickFilters() : ''}
                        ${this.config.showSavedFilters ? this.renderSavedFilters() : ''}
                        ${this.renderFilterTags()}
                        ${this.renderFiltersGrid()}
                        ${this.config.enableCompoundFilters ? this.renderCompoundFilters() : ''}
                        ${this.renderFiltersActions()}
                    </div>
                </div>
            </div>
        `;
    }
    
    renderSearchBox() {
        return `
            <div class="search-box">
                <input type="text" class="search-input" placeholder="搜索标题、描述、申请人..." data-field="search">
                <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"/>
                    <path d="M21 21l-4.35-4.35"/>
                </svg>
                <div class="search-suggestions" id="searchSuggestions" style="display: none;"></div>
            </div>
        `;
    }
    
    renderQuickFilters() {
        if (!this.config.quickFilters.length) return '';
        
        const buttons = this.config.quickFilters.map(filter => 
            `<button class="quick-filter-btn" data-quick-filter="${filter.key}">${filter.label}</button>`
        ).join('');
        
        return `
            <div class="quick-filters">
                ${buttons}
            </div>
        `;
    }
    
    renderSavedFilters() {
        if (!this.savedFilters.length) return '';
        
        const filters = this.savedFilters.map(filter => 
            `<div class="saved-filter-item" data-saved-filter="${filter.id}">
                <span>${filter.name}</span>
                <button class="saved-filter-delete" data-delete-filter="${filter.id}">×</button>
            </div>`
        ).join('');
        
        return `
            <div class="saved-filters">
                <div class="saved-filters-header">
                    <span class="saved-filters-title">已保存筛选</span>
                </div>
                <div class="saved-filters-list">
                    ${filters}
                </div>
            </div>
        `;
    }
    
    renderFilterTags() {
        return '<div class="filter-tags" id="filterTags"></div>';
    }
    
    renderFiltersGrid() {
        const fields = this.config.fields.map(field => this.renderFilterField(field)).join('');
        return `
            <div class="filters-grid">
                ${fields}
            </div>
        `;
    }
    
    renderFilterField(field) {
        switch (field.type) {
            case 'select':
                return this.renderSelectField(field);
            case 'dateRange':
                return this.renderDateRangeField(field);
            case 'amountRange':
                return this.renderAmountRangeField(field);
            case 'multiSelect':
                return this.renderMultiSelectField(field);
            default:
                return this.renderInputField(field);
        }
    }
    
    renderSelectField(field) {
        const options = field.options.map(option => 
            `<option value="${option.value}">${option.label}</option>`
        ).join('');
        
        return `
            <div class="filter-group">
                <label class="filter-label">${field.label}</label>
                <select class="filter-select" data-field="${field.key}">
                    <option value="">全部</option>
                    ${options}
                </select>
            </div>
        `;
    }
    
    renderDateRangeField(field) {
        return `
            <div class="filter-group">
                <label class="filter-label">${field.label}</label>
                <div class="filter-date-range">
                    <input type="date" class="filter-input" data-field="${field.key}_start" placeholder="开始日期">
                    <span class="filter-date-separator">至</span>
                    <input type="date" class="filter-input" data-field="${field.key}_end" placeholder="结束日期">
                </div>
            </div>
        `;
    }
    
    renderAmountRangeField(field) {
        return `
            <div class="filter-group">
                <label class="filter-label">${field.label}</label>
                <div class="filter-amount-range">
                    <input type="number" class="filter-input" data-field="${field.key}_min" placeholder="最小金额" step="0.01" min="0">
                    <span class="filter-date-separator">至</span>
                    <input type="number" class="filter-input" data-field="${field.key}_max" placeholder="最大金额" step="0.01" min="0">
                </div>
            </div>
        `;
    }
    
    renderMultiSelectField(field) {
        const options = field.options.map(option => 
            `<label class="checkbox-label">
                <input type="checkbox" value="${option.value}" data-field="${field.key}"> ${option.label}
            </label>`
        ).join('');
        
        return `
            <div class="filter-group">
                <label class="filter-label">${field.label}</label>
                <div class="multi-select-options">
                    ${options}
                </div>
            </div>
        `;
    }
    
    renderInputField(field) {
        return `
            <div class="filter-group">
                <label class="filter-label">${field.label}</label>
                <input type="${field.inputType || 'text'}" class="filter-input" data-field="${field.key}" placeholder="${field.placeholder || ''}">
            </div>
        `;
    }
    
    renderCompoundFilters() {
        return `
            <div class="compound-filter">
                <div class="compound-filter-header">
                    <span class="compound-filter-title">复合条件</span>
                    <button class="compound-filter-add" data-action="add-rule">+ 添加条件</button>
                </div>
                <div class="compound-filter-rules" id="compoundRules"></div>
            </div>
        `;
    }
    
    renderFiltersActions() {
        return `
            <div class="filters-actions">
                <button class="btn btn-secondary" data-action="reset">重置</button>
                <button class="btn btn-secondary" data-action="save">保存筛选</button>
                <button class="btn btn-primary" data-action="apply">应用筛选</button>
            </div>
        `;
    }
    
    bindEvents() {
        this.container.addEventListener('click', this.handleClick.bind(this));
        this.container.addEventListener('change', this.handleChange.bind(this));
        this.container.addEventListener('input', this.handleInput.bind(this));
    }
    
    handleClick(e) {
        const action = e.target.dataset.action;
        const quickFilter = e.target.dataset.quickFilter;
        const savedFilter = e.target.dataset.savedFilter;
        const deleteFilter = e.target.dataset.deleteFilter;
        
        if (action === 'toggle') {
            this.toggleFilters();
        } else if (action === 'apply') {
            this.applyFilters();
        } else if (action === 'reset') {
            this.resetFilters();
        } else if (action === 'save') {
            this.saveCurrentFilters();
        } else if (quickFilter) {
            this.applyQuickFilter(quickFilter);
        } else if (savedFilter) {
            this.applySavedFilter(savedFilter);
        } else if (deleteFilter) {
            this.deleteSavedFilter(deleteFilter);
        }
        
        if (e.target.classList.contains('filter-tag-remove')) {
            const field = e.target.dataset.field;
            this.removeFilter(field);
        }
    }
    
    handleChange(e) {
        const field = e.target.dataset.field;
        if (field && field !== 'search') {
            this.updateFilter(field, e.target.value);
        }
    }
    
    handleInput(e) {
        const field = e.target.dataset.field;
        if (field === 'search') {
            this.handleSearch(e.target.value);
        }
    }
    
    handleSearch(query) {
        clearTimeout(this.searchTimer);
        this.searchTimer = setTimeout(() => {
            this.updateFilter('search', query);
            this.config.onSearch(query);
        }, 300);
    }
    
    toggleFilters() {
        const toggle = this.container.querySelector('.filters-toggle');
        const content = this.container.querySelector('.filters-content');
        
        toggle.classList.toggle('collapsed');
        content.classList.toggle('collapsed');
    }
    
    updateFilter(field, value) {
        if (value === '' || value === null || value === undefined) {
            delete this.currentFilters[field];
        } else {
            this.currentFilters[field] = value;
        }
        
        this.updateFilterTags();
        this.config.onFilterChange(this.currentFilters);
    }
    
    removeFilter(field) {
        delete this.currentFilters[field];
        
        // 更新UI
        const input = this.container.querySelector(`[data-field="${field}"]`);
        if (input) {
            if (input.type === 'checkbox') {
                input.checked = false;
            } else {
                input.value = '';
            }
        }
        
        this.updateFilterTags();
        this.config.onFilterChange(this.currentFilters);
    }
    
    updateFilterTags() {
        const tagsContainer = this.container.querySelector('#filterTags');
        const tags = [];
        
        Object.entries(this.currentFilters).forEach(([field, value]) => {
            if (value && value !== '') {
                const fieldConfig = this.config.fields.find(f => f.key === field || f.key === field.replace(/_start|_end|_min|_max$/, ''));
                const label = fieldConfig ? fieldConfig.label : field;
                
                tags.push(`
                    <div class="filter-tag">
                        <span>${label}: ${this.formatFilterValue(field, value)}</span>
                        <button class="filter-tag-remove" data-field="${field}">×</button>
                    </div>
                `);
            }
        });
        
        tagsContainer.innerHTML = tags.join('');
    }
    
    formatFilterValue(field, value) {
        if (field.includes('_start') || field.includes('_end')) {
            return new Date(value).toLocaleDateString('zh-CN');
        }
        if (field.includes('_min') || field.includes('_max')) {
            return `$${value}`;
        }
        return value;
    }
    
    /**
     * 更新字段选项
     * @param {string} fieldKey - 字段键名
     * @param {Array} options - 新的选项数组 [{value: '', label: '全部'}]
     */
    updateFieldOptions(fieldKey, options) {
        const selectElement = this.container.querySelector(`select[data-field="${fieldKey}"]`);
        if (selectElement) {
            // 保存当前选中的值
            const currentValue = selectElement.value;
            
            // 清空现有选项
            selectElement.innerHTML = '';
            
            // 添加新选项
            options.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.value;
                optionElement.textContent = option.label;
                selectElement.appendChild(optionElement);
            });
            
            // 恢复选中的值（如果仍然存在）
            if (options.some(opt => opt.value === currentValue)) {
                selectElement.value = currentValue;
            }
        }
    }
    
    applyFilters() {
        this.config.onFilterChange(this.currentFilters);
    }
    
    resetFilters() {
        this.currentFilters = {};
        
        // 重置所有表单控件
        this.container.querySelectorAll('.filter-input, .filter-select').forEach(input => {
            if (input.type === 'checkbox') {
                input.checked = false;
            } else {
                input.value = '';
            }
        });
        
        // 重置快速筛选
        this.container.querySelectorAll('.quick-filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        this.activeQuickFilter = null;
        
        this.updateFilterTags();
        this.config.onFilterChange(this.currentFilters);
    }
    
    applyQuickFilter(key) {
        // 重置之前的快速筛选
        this.container.querySelectorAll('.quick-filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        const quickFilter = this.config.quickFilters.find(f => f.key === key);
        if (quickFilter) {
            // 激活按钮
            this.container.querySelector(`[data-quick-filter="${key}"]`).classList.add('active');
            this.activeQuickFilter = key;
            
            // 应用筛选条件
            this.currentFilters = { ...this.currentFilters, ...quickFilter.filters };
            this.updateFormValues();
            this.updateFilterTags();
            this.config.onFilterChange(this.currentFilters);
        }
    }
    
    updateFormValues() {
        Object.entries(this.currentFilters).forEach(([field, value]) => {
            const input = this.container.querySelector(`[data-field="${field}"]`);
            if (input) {
                if (input.type === 'checkbox') {
                    input.checked = true;
                } else {
                    input.value = value;
                }
            }
        });
    }
    
    saveCurrentFilters() {
        const name = prompt('请输入筛选配置名称:');
        if (name) {
            const filterId = Date.now().toString();
            const filter = {
                id: filterId,
                name,
                filters: { ...this.currentFilters }
            };
            
            this.savedFilters.push(filter);
            this.saveSavedFilters();
            this.render();
            this.bindEvents();
        }
    }
    
    // 新增：根据筛选条件生成可读方案名（避免使用时间戳导致重复）
    generateUrlPresetName(filters) {
        const prefix = this.config.urlFilterNamePrefix || 'URL筛选';
        const parts = [];
        if (filters.category) parts.push(`类别:${filters.category}`);
        if (filters.currency) parts.push(`货币:${filters.currency}`);
        if (filters.status) parts.push(`状态:${filters.status}`);
        if (filters.search) parts.push(`搜索:${filters.search}`);
        return parts.length ? `${prefix}-${parts.join('/')}` : `${prefix}`;
    }

    // 新增：判断是否存在相同筛选条件的已保存方案
    hasSameSavedFilters(filters) {
        const target = JSON.stringify(filters);
        return this.savedFilters.some(f => JSON.stringify(f.filters) === target);
    }

    applySavedFilter(id) {
        const savedFilter = this.savedFilters.find(f => f.id === id);
        if (savedFilter) {
            this.currentFilters = { ...savedFilter.filters };
            this.updateFormValues();
            this.updateFilterTags();
            this.config.onFilterChange(this.currentFilters);
        }
    }
    
    deleteSavedFilter(id) {
        this.savedFilters = this.savedFilters.filter(f => f.id !== id);
        this.saveSavedFilters();
        this.render();
        this.bindEvents();
    }
    
    loadSavedFilters() {
        try {
            return JSON.parse(localStorage.getItem('advancedFilters_saved') || '[]');
        } catch {
            return [];
        }
    }
    
    saveSavedFilters() {
        localStorage.setItem('advancedFilters_saved', JSON.stringify(this.savedFilters));
    }
    
    loadDefaultFilters() {
        // 从URL参数加载筛选条件
        const urlParams = new URLSearchParams(window.location.search);
        let hasFilters = false;
        urlParams.forEach((value, key) => {
            if (value) {
                this.currentFilters[key] = value;
                hasFilters = true;
            }
        });
        
        if (hasFilters) {
            this.updateFormValues();
            this.updateFilterTags();
            // 如果有URL筛选参数，则触发筛选更新
            this.config.onFilterChange(this.currentFilters);
        }
    }
    
    // 公共API
    getFilters() {
        return { ...this.currentFilters };
    }
    
    setFilterValue(key, value) {
        if (value === '' || value === null || value === undefined) {
            delete this.currentFilters[key];
        } else {
            this.currentFilters[key] = value;
        }
        
        this.updateFormValues();
        this.updateFilterTags();
        // 修复：设置筛选值后立即触发筛选更新
        this.config.onFilterChange(this.currentFilters);
    }
    
    setFilters(filters) {
        this.currentFilters = { ...filters };
        this.updateFormValues();
        this.updateFilterTags();
        // 修复：设置多个筛选值后立即触发筛选更新
        this.config.onFilterChange(this.currentFilters);
    }
    
    // 新增方法：初始化时加载URL参数筛选条件
    initializeWithUrlParams() {
        // 从URL参数加载筛选条件
        const urlParams = new URLSearchParams(window.location.search);
        let hasFilters = false;
        urlParams.forEach((value, key) => {
            if (value) {
                this.currentFilters[key] = value;
                hasFilters = true;
            }
        });
        
        if (hasFilters) {
            // 确保UI更新后再触发筛选
            setTimeout(() => {
                this.updateFormValues();
                this.updateFilterTags();
                // 触发筛选更新
                this.config.onFilterChange(this.currentFilters);
                
                // 新增：将URL参数持久化为保存的筛选方案（避免重复）
                if (this.config.autoSaveUrlFilters) {
                    const filtersCopy = { ...this.currentFilters };
                    if (!this.hasSameSavedFilters(filtersCopy)) {
                        const filter = {
                            id: Date.now().toString(),
                            name: this.generateUrlPresetName(filtersCopy),
                            filters: filtersCopy
                        };
                        // 置顶新增方案
                        this.savedFilters.unshift(filter);
                        this.saveSavedFilters();
                        // 重新渲染保存方案区域
                        this.render();
                        this.bindEvents();
                    }
                }
            }, 50);
        }
    }
    
    clearFilters() {
        this.resetFilters();
    }
}