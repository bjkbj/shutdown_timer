import json
import os

class ConfigManager:
    def __init__(self):
        self.config_file = "app_config.json"
        self.default_config = {
            "language": "cn"  # 默认使用中文
        }
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.default_config
        return self.default_config
    
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