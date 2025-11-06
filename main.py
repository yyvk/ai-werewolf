"""
AI狼人杀 - Web服务器入口
"""

import sys
import os
from pathlib import Path

# 设置标准输出编码为 UTF-8（解决 Windows GBK 编码问题）
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent))


def run_web_server():
    """运行Web服务"""
    import uvicorn
    from src.web.api import create_app
    from src.utils.config import get_config
    
    config = get_config()
    app = create_app()
    
    print("\n" + "="*60)
    print("  AI狼人杀 Web服务器")
    print("="*60)
    print(f"  后端API: http://{config.web_host}:{config.web_port}")
    print(f"  API文档: http://{config.web_host}:{config.web_port}/docs")
    print(f"  前端地址: http://localhost:3000")
    print("="*60)
    print("\n提示：请在另一个终端运行前端服务：")
    print("  cd frontend")
    print("  npm run dev")
    print()
    
    uvicorn.run(
        app,
        host=config.web_host,
        port=config.web_port
    )


def main():
    """主函数"""
    run_web_server()


if __name__ == "__main__":
    main()

