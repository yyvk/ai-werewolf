"""
日志模块
统一的日志管理
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logger(
    name: str = "werewolf",
    log_file: Optional[str] = None,
    log_level: str = "INFO",
    log_dir: str = "data/logs"
) -> logging.Logger:
    """设置日志器"""
    
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_file is None:
        log_file = f"werewolf_{datetime.now().strftime('%Y%m%d')}.log"
    
    file_handler = logging.FileHandler(
        log_path / log_file,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


class GameLogger:
    """游戏专用日志器"""
    
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.logger = setup_logger(f"game_{game_id}")
        self.events = []
    
    def log_event(self, event_type: str, data: dict):
        """记录游戏事件"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        }
        self.events.append(event)
        self.logger.info(f"[{event_type}] {data}")
    
    def get_events(self):
        """获取所有事件"""
        return self.events
    
    def save_events(self, filename: Optional[str] = None):
        """保存事件到文件"""
        import json
        from pathlib import Path
        
        if filename is None:
            filename = f"game_{self.game_id}_events.json"
        
        log_dir = Path("data/logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        with open(log_dir / filename, 'w', encoding='utf-8') as f:
            json.dump(self.events, f, ensure_ascii=False, indent=2)

