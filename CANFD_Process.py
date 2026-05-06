import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QIcon

# --- 资源路径处理函数 ---
def resource_path(relative_path):
    """ 获取程序运行时的资源绝对路径，兼容开发环境和 PyInstaller 打包环境 """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的临时解压目录
        return os.path.join(sys._MEIPASS, relative_path)
    # 开发环境下的当前目录
    return os.path.join(os.path.abspath("."), relative_path)

# --- 嵌入式 HTML 内容 ---
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        :root { --primary: #0f172a; --accent: #3b82f6; --danger: #ef4444; --success: #22c55e; --bg: #f8fafc; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); margin: 0; padding: 20px; color: #1e293b; }
        .header { margin-bottom: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
        .main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        .card-title { font-size: 16px; font-weight: bold; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between; }
        .badge { font-size: 11px; padding: 2px 8px; border-radius: 10px; background: #f1f5f9; }
        .badge.valid { background: #dcfce7; color: #166534; }
        .badge.invalid { background: #fee2e2; color: #991b1b; }
        .field-item { background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; margin-bottom: 10px; }
        .field-row { display: grid; grid-template-columns: 1.5fr 0.8fr 1.2fr 40px; gap: 8px; }
        label { display: block; font-size: 11px; color: #64748b; margin-bottom: 4px; }
        input { width: 100%; box-sizing: border-box; border: 1px solid #e2e8f0; padding: 8px 10px; border-radius: 6px; font-size: 13px; outline: none; }
        input:focus { border-color: var(--accent); box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1); }
        input:disabled { background: #f8fafc; color: #94a3b8; }
        .btn { cursor: pointer; border: none; border-radius: 6px; padding: 8px 12px; font-size: 12px; }
        .btn-primary { background: var(--primary); color: white; }
        .btn-danger { background: var(--danger); color: white; }
        .full-width { grid-column: span 2; }
        .result-box { display: flex; gap: 15px; margin-top: 10px; }
        .res-item { flex: 1; background: #f8fafc; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0; }
        .hex-display { font-family: monospace; font-size: 26px; font-weight: 800; }
        .bin-display { font-family: monospace; color: var(--accent); letter-spacing: 1px; font-size: 14px; }
        .detail-row { display: grid; grid-template-columns: 1.2fr 0.8fr 1fr 1.5fr; padding: 10px; border-bottom: 1px solid #f1f5f9; font-size: 13px; }
        .bit-tag { background: #1e293b; color: white; padding: 1px 6px; border-radius: 4px; font-size: 10px; }
    </style>
</head>
<body>
    <div class="header"><h2>CAN FD 29位扩展帧组包工具</h2></div>
    <div class="main-grid">
        <div class="card">
            <div class="card-title">1. 配置分段 <span id="bitTotalBadge" class="badge">总位数: 0 / 29</span></div>
            <div id="configContainer"></div>
            <div style="margin-top:10px; border-top:1px dashed #eee; padding-top:10px;">
                <div class="field-row" style="grid-template-columns: 1.5fr 1fr 1fr;">
                    <input type="text" id="newFieldName" placeholder="字段名称">
                    <input type="text" id="newFieldBits" value="8" oninput="this.value=this.value.replace(/[^0-9]/g,'')">
                    <button class="btn btn-primary" onclick="addNewField()">+ 添加</button>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="card-title">2. 数值设定 (Hex)</div>
            <div id="inputContainer"></div>
            <div style="margin-top:10px; border-top:2px solid #f1f5f9; padding-top:15px;">
                <label>4. 反向解析 (Hex ID)</label>
                <div style="display:flex; gap:8px;">
                    <input type="text" id="reverseHexInput" placeholder="例如: 18DB33F1">
                    <button class="btn btn-primary" onclick="handleReverseParse()">解析</button>
                </div>
            </div>
        </div>
        <div class="card full-width">
            <div class="card-title">3. 生成结果</div>
            <div class="result-box">
                <div class="res-item"><label>二进制排列</label><div class="bin-display" id="binResult"></div></div>
                <div class="res-item"><label>扩展帧 ID (Hex)</label><div class="hex-display" id="hexResult"></div></div>
            </div>
            <div id="mappingDetail" style="margin-top:15px; border-top: 1px solid #eee;"></div>
        </div>
    </div>

    <script>
        let fields = [
            { name: 'Priority', bits: 3, hex: '0' },
            { name: 'Source', bits: 8, hex: '00' },
            { name: 'Target', bits: 8, hex: '00' },
            { name: 'Command', bits: 10, hex: '000' }
        ];
        let lastActiveId = null;
        let lastCursorPos = 0;

        function saveFocus() {
            const el = document.activeElement;
            if (el && el.tagName === 'INPUT') {
                lastActiveId = el.id;
                try { lastCursorPos = el.selectionStart; } catch (e) { lastCursorPos = el.value.length; }
            }
        }

        function restoreFocus() {
            if (lastActiveId) {
                const el = document.getElementById(lastActiveId);
                if (el) {
                    el.focus();
                    const supportsSelection = ['text', 'search', 'url', 'tel', 'password'].includes(el.type);
                    if (supportsSelection) {
                        try { el.setSelectionRange(lastCursorPos, lastCursorPos); } catch (e) {}
                    }
                }
            }
        }

        function refresh() {
            saveFocus();
            renderConfig();
            renderInputs();
            calculate();
            restoreFocus();
        }

        function renderConfig() {
            const container = document.getElementById('configContainer');
            container.innerHTML = '';
            let currentBit = 29;
            let total = 0;
            fields.forEach((f, i) => {
                const start = currentBit - 1;
                const end = currentBit - f.bits;
                total += (parseInt(f.bits) || 0);
                const div = document.createElement('div');
                div.className = 'field-item';
                div.innerHTML = `<div class="field-row">
                    <div><label>名称</label><input type="text" id="conf-n-${i}" value="${f.name}" oninput="fields[${i}].name=this.value; refresh();"></div>
                    <div><label>位数</label><input type="text" id="conf-b-${i}" value="${f.bits}" oninput="this.value=this.value.replace(/[^0-9]/g,''); fields[${i}].bits=parseInt(this.value)||0; refresh();"></div>
                    <div><label>范围</label><input type="text" disabled value="bit ${start}..${end}"></div>
                    <div style="display:flex; align-items:flex-end;"><button class="btn btn-danger" onclick="removeField(${i})">✕</button></div>
                </div>`;
                container.appendChild(div);
                currentBit -= f.bits;
            });
            const badge = document.getElementById('bitTotalBadge');
            badge.innerText = `总位数: ${total} / 29`;
            badge.className = (total === 29) ? 'badge valid' : 'badge invalid';
        }

        function renderInputs() {
            const container = document.getElementById('inputContainer');
            container.innerHTML = '';
            let currentBit = 29;
            fields.forEach((f, i) => {
                const start = currentBit - 1;
                const end = currentBit - f.bits;
                const div = document.createElement('div');
                div.className = 'field-item';
                div.innerHTML = `
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span style="font-weight:bold; font-size:13px;">${f.name}</span>
                        <span class="bit-tag">bit ${start}..${end}</span>
                    </div>
                    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:8px;">
                        <div><label>Hex值</label><input type="text" id="val-h-${i}" value="${f.hex}" oninput="updateFieldHex(${i}, this.value)"></div>
                        <div><label>二进制</label><input type="text" disabled value="${BigInt('0x'+(f.hex||0)).toString(2).padStart(f.bits,'0').slice(-f.bits)}"></div>
                    </div>`;
                container.appendChild(div);
                currentBit -= f.bits;
            });
        }

        function updateFieldHex(i, v) {
            fields[i].hex = v.replace(/[^0-9a-fA-F]/g, '');
            refresh();
        }

        function calculate() {
            let totalVal = 0n;
            let currentShift = 0n;
            let detailHtml = '';
            [...fields].reverse().forEach(f => {
                const b = BigInt(f.bits);
                const val = BigInt("0x" + (f.hex || "0")) & ((1n << b) - 1n);
                totalVal |= (val << currentShift);
                detailHtml = `<div class="detail-row"><span>${f.name}</span><span>0x${f.hex.toUpperCase()}</span><span class="bit-tag">bit ${currentShift+b-1n}..${currentShift}</span><span>${val.toString(2).padStart(f.bits,'0')}</span></div>` + detailHtml;
                currentShift += b;
            });
            document.getElementById('hexResult').innerText = "0x" + totalVal.toString(16).toUpperCase().padStart(8, '0');
            let binStr = totalVal.toString(2).padStart(29, '0');
            document.getElementById('binResult').innerText = (binStr.match(/.{1,4}/g) || []).join(' ');
            document.getElementById('mappingDetail').innerHTML = detailHtml;
        }

        function addNewField() {
            fields.push({ name: document.getElementById('newFieldName').value || 'New', bits: parseInt(document.getElementById('newFieldBits').value) || 8, hex: '0' });
            refresh();
        }

        function removeField(i) { fields.splice(i, 1); refresh(); }

        function handleReverseParse() {
            let input = document.getElementById('reverseHexInput').value.replace(/^0x/i, '');
            if(!input) return;
            let val = BigInt("0x" + input);
            let shift = 0n;
            [...fields].reverse().forEach(f => {
                const b = BigInt(f.bits);
                f.hex = ((val >> shift) & ((1n << b) - 1n)).toString(16).toUpperCase();
                shift += b;
            });
            refresh();
        }
        refresh();
    </script>
</body>
</html>
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CAN FD 29-Bit ID 组包工具")
        self.resize(1100, 850)
        
        # 设置窗口图标（关键：使用 resource_path 确保打包后能找到）
        icon_path = resource_path("logo.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.browser = QWebEngineView()
        self.browser.setHtml(HTML_CONTENT)
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.setContentsMargins(0, 0, 0, 0)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 也可以给 App 设置图标，确保任务栏统一
    app_icon_path = resource_path("logo.ico")
    if os.path.exists(app_icon_path):
        app.setWindowIcon(QIcon(app_icon_path))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())