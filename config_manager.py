import json
import os

class ConfigManager:
    def __init__(self):
        self.config_file = "app_config.json"
        self.default_config = {
            "language": "cn"  # 默认使用中文
        }
        self.config = {
            'language': 'cn',
            'shutdown_time': None,  # 格式: {'hour': hour, 'minute': minute}
            'selected_days': []     # 选中的星期列表
        }
        self.load_config()
    
    def save_shutdown_settings(self, hour, minute, selected_days):
        """保存关机设置"""
        self.config['shutdown_time'] = {'hour': hour, 'minute': minute}
        self.config['selected_days'] = selected_days
        self.save_config()
    
    def get_shutdown_settings(self):
        """获取关机设置"""
        return self.config.get('shutdown_time'), self.config.get('selected_days')
    
    def clear_shutdown_settings(self):
        """清除关机设置"""
        self.config['shutdown_time'] = None
        self.config['selected_days'] = []
        self.save_config()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 更新配置到self.config
                    self.config.update(loaded_config)
            except:
                self.config.update(self.default_config)
        else:
            self.config.update(self.default_config)
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存配置文件失败：{str(e)}")
    
    def get_language(self):
        """获取语言设置"""
        return self.config.get("language", "cn")
    
    def set_language(self, lang):
        """设置语言"""
        self.config["language"] = lang
        self.save_config()