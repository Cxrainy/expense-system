/**
 * 文件预览和下载功能 JavaScript 文件
 * 支持图片、PDF、Markdown、视频的模态框预览
 * 其他文件类型仅提供下载功能
 */

class FilePreviewManager {
    constructor() {
        this.currentModal = null;
        this.init();
    }

    init() {
        this.createPreviewModal();
        this.bindEvents();
    }

    createPreviewModal() {
        // 创建模态框HTML
        const modalHTML = `
            <div class="file-preview-modal" id="filePreviewModal">
                <div class="file-preview-content">
                    <div class="file-preview-header">
                        <h3 class="file-preview-title" id="filePreviewTitle">文件预览</h3>
                        <button class="file-preview-close" id="filePreviewClose">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="18" y1="6" x2="6" y2="18"/>
                                <line x1="6" y1="6" x2="18" y2="18"/>
                            </svg>
                        </button>
                    </div>
                    <div class="file-preview-body" id="filePreviewBody">
                        <div class="file-preview-loading">
                            <div class="loading-spinner"></div>
                            <span>加载中...</span>
                        </div>
                    </div>
                    <div class="file-preview-actions">
                        <button class="btn btn-secondary btn-sm" id="fileDownloadBtn">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                                <polyline points="7,10 12,15 17,10"/>
                                <line x1="12" y1="15" x2="12" y2="3"/>
                            </svg>
                            下载文件
                        </button>
                    </div>
                </div>
            </div>
        `;

        // 添加到body
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.currentModal = document.getElementById('filePreviewModal');
    }

    bindEvents() {
        const closeBtn = document.getElementById('filePreviewClose');
        const downloadBtn = document.getElementById('fileDownloadBtn');
        const modal = this.currentModal;

        // 关闭按钮
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                this.closePreview();
            });
        }

        // 点击模态框外部关闭
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closePreview();
            }
        });

        // ESC键关闭
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('show')) {
                this.closePreview();
            }
        });

        // 下载按钮
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => {
                if (this.currentFileData) {
                    this.downloadFile(this.currentFileData.filename, this.currentFileData.original_filename);
                }
            });
        }
    }

    async previewFile(fileData) {
        this.currentFileData = fileData;
        const modal = this.currentModal;
        const title = document.getElementById('filePreviewTitle');
        const body = document.getElementById('filePreviewBody');

        // 设置标题
        title.textContent = fileData.original_filename;

        // 显示模态框
        modal.classList.add('show');

        // 显示加载状态
        body.innerHTML = `
            <div class="file-preview-loading">
                <div class="loading-spinner"></div>
                <span>加载中...</span>
            </div>
        `;

        try {
            await this.renderFileContent(fileData, body);
        } catch (error) {
            console.error('文件预览失败:', error);
            this.renderError(body, '文件预览失败，请尝试下载文件');
        }
    }

    async renderFileContent(fileData, container) {
        const fileUrl = `/uploads/${fileData.filename}`;
        
        switch (fileData.file_category) {
            case 'image':
                this.renderImage(fileUrl, fileData.original_filename, container);
                break;
            case 'pdf':
                this.renderPDF(fileUrl, container);
                break;
            case 'markdown':
                await this.renderMarkdown(fileUrl, container);
                break;
            case 'video':
                this.renderVideo(fileUrl, container);
                break;
            default:
                this.renderError(container, '此文件类型不支持预览，请下载查看');
        }
    }

    renderImage(fileUrl, filename, container) {
        container.innerHTML = `
            <img src="${fileUrl}" alt="${this.escapeHtml(filename)}" 
                 onload="this.style.opacity=1" 
                 style="opacity: 0; transition: opacity 0.3s ease;">
        `;
    }

    renderPDF(fileUrl, container) {
        container.innerHTML = `
            <iframe src="${fileUrl}" 
                    title="PDF预览"
                    onload="this.style.opacity=1"
                    style="opacity: 0; transition: opacity 0.3s ease;">
            </iframe>
        `;
    }

    async renderMarkdown(fileUrl, container) {
        try {
            const response = await fetch(fileUrl);
            if (!response.ok) {
                throw new Error('Failed to fetch markdown file');
            }
            
            const content = await response.text();
            const html = this.markdownToHtml(content);
            
            container.innerHTML = `
                <div class="markdown-content">
                    ${html}
                </div>
            `;
        } catch (error) {
            throw new Error('Markdown文件加载失败');
        }
    }

    renderVideo(fileUrl, container) {
        container.innerHTML = `
            <video controls 
                   onloadstart="this.style.opacity=1"
                   style="opacity: 0; transition: opacity 0.3s ease;">
                <source src="${fileUrl}" type="video/mp4">
                <source src="${fileUrl}" type="video/webm">
                <source src="${fileUrl}" type="video/ogg">
                您的浏览器不支持视频播放。
            </video>
        `;
    }

    renderError(container, message) {
        container.innerHTML = `
            <div class="file-preview-error">
                <div class="error-icon">📄</div>
                <h4>无法预览</h4>
                <p>${message}</p>
            </div>
        `;
    }

    markdownToHtml(markdown) {
        // 简单的Markdown转HTML实现
        let html = markdown
            // 标题
            .replace(/^### (.*$)/gim, '<h3>$1</h3>')
            .replace(/^## (.*$)/gim, '<h2>$1</h2>')
            .replace(/^# (.*$)/gim, '<h1>$1</h1>')
            
            // 粗体和斜体
            .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/gim, '<em>$1</em>')
            
            // 代码块
            .replace(/```([\s\S]*?)```/gim, '<pre><code>$1</code></pre>')
            .replace(/`([^`]*)`/gim, '<code>$1</code>')
            
            // 链接
            .replace(/\[([^\]]+)\]\(([^\)]+)\)/gim, '<a href="$2" target="_blank">$1</a>')
            
            // 段落
            .replace(/\n\s*\n/gim, '</p><p>')
            .replace(/^(.+)$/gim, '<p>$1</p>')
            
            // 清理多余的p标签
            .replace(/<p><\/p>/gim, '')
            .replace(/<p>(<h[1-6]>.*?<\/h[1-6]>)<\/p>/gim, '$1')
            .replace(/<p>(<pre>.*?<\/pre>)<\/p>/gim, '$1');

        return html;
    }

    closePreview() {
        if (this.currentModal) {
            this.currentModal.classList.remove('show');
            this.currentFileData = null;
        }
    }

    downloadFile(filename, originalName) {
        const link = document.createElement('a');
        link.href = `/uploads/${filename}`;
        link.download = originalName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // 静态方法：创建文件列表项的HTML
    static createFileListItem(file) {
        const typeIcons = {
            'image': '🖼️',
            'pdf': '📄',
            'markdown': '📝',
            'video': '🎥',
            'other': '📎'
        };

        const icon = typeIcons[file.file_category] || typeIcons.other;
        const fileSize = FilePreviewManager.formatFileSize(file.file_size);
        
        const previewBtn = file.can_preview ? `
            <button class="file-preview-btn" onclick="filePreviewManager.previewFile(${JSON.stringify(file).replace(/"/g, '&quot;')})">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                </svg>
                预览
            </button>
        ` : '';

        return `
            <div class="file-item">
                <div class="file-info">
                    <span class="file-type-icon ${file.file_category}">${icon}</span>
                    <div class="file-details">
                        <div class="file-name">${FilePreviewManager.escapeHtml(file.original_filename)}</div>
                        <div class="file-meta">${fileSize} • ${file.file_type}</div>
                    </div>
                </div>
                <div class="file-actions">
                    ${previewBtn}
                    <a href="/uploads/${file.filename}" 
                       download="${FilePreviewManager.escapeHtml(file.original_filename)}" 
                       class="file-download-btn">
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                            <polyline points="7,10 12,15 17,10"/>
                            <line x1="12" y1="15" x2="12" y2="3"/>
                        </svg>
                        下载
                    </a>
                </div>
            </div>
        `;
    }

    // 静态方法：格式化文件大小
    static formatFileSize(bytes) {
        if (!bytes) return '0 B';
        
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }

    // 静态方法：HTML转义
    static escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// 全局初始化
let filePreviewManager;

document.addEventListener('DOMContentLoaded', function() {
    filePreviewManager = new FilePreviewManager();
    
    // 将实例暴露到全局，便于其他地方调用
    window.filePreviewManager = filePreviewManager;
    window.FilePreviewManager = FilePreviewManager;
});