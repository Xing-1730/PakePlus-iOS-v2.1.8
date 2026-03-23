#!/usr/bin/env python3
"""
自动重载服务器
当HTML文件变化时，自动刷新浏览器
"""
import http.server
import socketserver
import os
import time
import threading

# 端口号
PORT = 8002
# 要监控的文件
WATCHED_FILE = "3505路区间车.html"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 移除自动刷新，只在文件变化时手动刷新
        super().end_headers()

def watch_file():
    """监控文件变化"""
    print(f"监控文件变化: {WATCHED_FILE}")
    last_modified = os.path.getmtime(WATCHED_FILE)
    
    while True:
        time.sleep(1)
        try:
            current_modified = os.path.getmtime(WATCHED_FILE)
            if current_modified != last_modified:
                print(f"文件已更新: {WATCHED_FILE}")
                last_modified = current_modified
        except Exception as e:
            pass

def start_server():
    """启动HTTP服务器"""
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"服务器启动在 http://localhost:{PORT}")
        print(f"预览地址: http://localhost:{PORT}/{WATCHED_FILE}")
        print("按 Ctrl+C 停止服务器")
        httpd.serve_forever()

if __name__ == "__main__":
    # 启动文件监控线程
    watch_thread = threading.Thread(target=watch_file, daemon=True)
    watch_thread.start()
    
    # 启动HTTP服务器
    start_server()
