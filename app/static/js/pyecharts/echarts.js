// 确保echarts库正确加载
(function() {
    if (typeof echarts === 'undefined') {
        var script = document.createElement('script');
        script.src = '/static/js/pyecharts/echarts.min.js';
        script.async = false;
        document.head.appendChild(script);
    }
})();
