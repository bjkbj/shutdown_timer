import json
import os

class ShutdownSettings:
    def __init__(self):
        self.config_file = "shutdown_settings.json"
        self.language = "en"
        self.shutdown_icon_visible = False
        self._load_settings()
    
    def _load_settings(self):
        """从文件加载设置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.language = data.get('language', 'en')
                    self.shutdown_icon_visible = data.get('shutdown_icon_visible', False)
        except Exception as e:
            print(f"加载设置出错：{str(e)}")
    
    def get_settings(self):
        """获取关机时间和星期设置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('shutdown_time', []), data.get('selected_days', [])
            return [], []
        except Exception as e:
            print(f"获取设置出错：{str(e)}")
            return [], []
    
    def save_settings(self, hour, minute, days):
        """保存关机时间和星期设置"""
        try:
            data = {
                'shutdown_time': [hour, minute],
                'selected_days': days,
                'language': self.language,
                'shutdown_icon_visible': self.shutdown_icon_visible
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存设置出错：{str(e)}")
    
    def clear_settings(self):
        """清空关机时间和星期设置"""
        try:
            data = {
                'shutdown_time': [],
                'selected_days': [],
                'language': self.language,
                'shutdown_icon_visible': self.shutdown_icon_visible
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"清空设置出错：{str(e)}")
    
    def get_language(self):
        """获取语言设置"""
        return self.language
    
    def set_language(self, lang):
        """设置语言"""
        self.language = lang
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                data['language'] = lang
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"设置语言出错：{str(e)}")

# 创建全局实例
shutdown_settings = ShutdownSettings()