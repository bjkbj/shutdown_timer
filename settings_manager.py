import wx
import wx.adv

from setting_data import shutdown_settings

import json  # 添加json模块导入

class SettingsDialog(wx.Dialog):
    def __init__(self, parent):
        # 获取当前语言设置
        is_chinese = parent.lang_toggle.GetValue()
        # 根据语言设置文本
        if is_chinese:
            title = "定时关机设置"
            time_label_text = "选择关机时间："
            weekday_label_text = "选择重复日期："
            weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
            ok_text = "确定"
        else:
            title = "Shutdown Settings"
            time_label_text = "Select shutdown time:"
            weekday_label_text = "Select repeat days:"
            weekdays = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            ok_text = "OK"
        
        super().__init__(parent, title=title, size=(500, 300))
        self.parent = parent
        
        # 创建主面板
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#ffffff')
        
        # 使用BoxSizer进行布局
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 添加时间选择器
        time_sizer = wx.BoxSizer(wx.HORIZONTAL)
        time_label = wx.StaticText(panel, label=time_label_text)
        self.hour_choice = wx.ComboBox(
            panel,
            choices=[f"{i:02d}" for i in range(24)],
            style=wx.CB_DROPDOWN|wx.CB_READONLY
        )
        self.minute_choice = wx.ComboBox(
            panel,
            choices=[f"{i:02d}" for i in range(60)],
            style=wx.CB_DROPDOWN|wx.CB_READONLY
        )
        colon_label = wx.StaticText(panel, label=":")
        
        time_sizer.Add(time_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        time_sizer.Add(self.hour_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        time_sizer.Add(colon_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        time_sizer.Add(self.minute_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        main_sizer.Add(time_sizer, 0, wx.ALL, 10)
        
        # 添加星期选择
        weekday_label = wx.StaticText(panel, label=weekday_label_text)
        main_sizer.Add(weekday_label, 0, wx.ALL, 10)
        
        weekday_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.weekday_boxes = []
        for i, day in enumerate(weekdays):
            cb = wx.CheckBox(panel, label=day)
            if i <= 4:  # 默认选中周一到周五
                cb.SetValue(True)
            self.weekday_boxes.append(cb)
            weekday_sizer.Add(cb, 0, wx.ALL, 5)
        main_sizer.Add(weekday_sizer, 0, wx.ALL|wx.EXPAND, 5)
        
        # 添加按钮（靠左对齐）
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, wx.ID_OK, ok_text)
        button_sizer.Add(ok_button, 0, wx.ALL, 5)
        main_sizer.Add(button_sizer, 0, wx.ALL|wx.LEFT, 10)  # 靠左对齐
        
        panel.SetSizer(main_sizer)
        
        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.on_ok, ok_button)
    
    def on_ok(self, event):
        """确定按钮事件处理"""
        try:
            # 获取选择的时间和星期
            hour_str = self.hour_choice.GetStringSelection()
            minute_str = self.minute_choice.GetStringSelection()
            
            # 获取选中的星期
            selected_days = []
            for i, cb in enumerate(self.weekday_boxes):
                if cb.GetValue():
                    selected_days.append(i)
            
            # 如果没有选择时间或星期，直接保存空设置
            if not hour_str or not minute_str:
                self.save_settings_to_file(-1, -1, [])
                self.EndModal(wx.ID_OK)
                return
            
            # 安全转换时间
            try:
                hour = int(hour_str)
                minute = int(minute_str)
            except (ValueError, TypeError):
                # 如果转换失败，保存空设置
                self.save_settings_to_file(-1, -1, [])
                self.EndModal(wx.ID_OK)
                return
            
            # 保存设置到文件
            self.save_settings_to_file(hour, minute, selected_days)
            self.EndModal(wx.ID_OK)
            
        except:
            # 静默处理所有错误，保存空设置并关闭
            self.save_settings_to_file(-1, -1, [])
            self.EndModal(wx.ID_OK)
    
    def save_settings_to_file(self, hour, minute, days):
        """保存设置到文件"""
        import json
        from setting_data import shutdown_settings
        
        # 检查时间和星期是否都有选择
        if hour == -1 or minute == -1 or not days:
            data = {
                'shutdown_time': [-1, -1],  # 改为保存-1而不是空数组
                'selected_days': [],
                'language': shutdown_settings.language,
                'shutdown_icon_visible': shutdown_settings.shutdown_icon_visible
            }
        else:
            data = {
                'shutdown_time': [hour, minute],
                'selected_days': days,
                'language': shutdown_settings.language,
                'shutdown_icon_visible': shutdown_settings.shutdown_icon_visible
            }
        
        # 保存到文件
        with open(shutdown_settings.config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def update_main_window_display(self, hour, minute, days):
        """更新主窗口显示"""
        # 如果时间和星期都为空，清除显示
        if hour == -1 or minute == -1 or not days:
            self.parent.shutdown_time_display.SetLabel("")
            self.parent.weekday_display.SetLabel("")
            self.parent.shutdown_status.Hide()
            return
        
        # 更新显示
        is_chinese = self.parent.lang_toggle.GetValue()
        if is_chinese:
            shutdown_text = f"关机时间设置为: {hour:02d}:{minute:02d}"
            weekdays = ['一', '二', '三', '四', '五', '六', '日']
            selected_weekdays = [f"周{weekdays[i]}" for i in days]
            weekday_text = f"选中的星期: {', '.join(selected_weekdays)}"
        else:
            shutdown_text = f"Shutdown time set to: {hour:02d}:{minute:02d}"
            weekdays = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            selected_weekdays = [weekdays[i] for i in days]
            weekday_text = f"Repeat on: {', '.join(selected_weekdays)}"
        
        self.parent.shutdown_time_display.SetLabel(shutdown_text)
        self.parent.weekday_display.SetLabel(weekday_text)
        self.parent.shutdown_status.Show()
    
    def SetTitle(self, title):
        """重写标题设置方法以支持语言切换"""
        super().SetTitle(title)
        # 根据标题判断语言
        is_chinese = "定时" in title
        if is_chinese:
            # 更新中文界面文本
            for i, cb in enumerate(['周一', '周二', '周三', '周四', '周五', '周六', '周日']):
                self.weekday_boxes[i].SetLabel(cb)
            self.FindWindow(wx.ID_OK).SetLabel("确定")
        else:
            # 更新英文界面文本
            for i, cb in enumerate(['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']):
                self.weekday_boxes[i].SetLabel(cb)
            self.FindWindow(wx.ID_OK).SetLabel("OK")

class SettingsManager:
    def __init__(self, main_frame, colors):
        # 修复参数传递问题
        self.parent = main_frame  # 将 main_frame 赋值给 parent
        self.colors = colors
        self.shutdown_status = None
        self.shutdown_time_display = None
        self.weekday_display = None
        self.selected_hour = 0
        self.selected_minute = 0
        self.selected_days = []
        self.current_dialog = None

    def show_settings(self):
        """显示设置对话框"""
        # 创建对话框
        dialog = SettingsDialog(self.parent)
        self.current_dialog = dialog
        
        # 显示对话框并等待结果
        if dialog.ShowModal() == wx.ID_OK:
            # 获取所选时间
            self.selected_hour = int(dialog.hour_choice.GetStringSelection())
            self.selected_minute = int(dialog.minute_choice.GetStringSelection())
            
            # 获取所选星期
            self.selected_days = []
            for i, cb in enumerate(dialog.weekday_boxes):
                if cb.GetValue():
                    self.selected_days.append(i)
            
            # 更新显示
            is_chinese = self.parent.lang_toggle.GetValue()
            if is_chinese:
                shutdown_text = f"关机时间设置为: {self.selected_hour:02d}:{self.selected_minute:02d}"
            else:
                shutdown_text = f"Shutdown time set to: {self.selected_hour:02d}:{self.selected_minute:02d}"
            
            self.shutdown_time_display.SetLabel(shutdown_text)
            
            # 显示警告图标
            if self.shutdown_status:
                self.shutdown_status.Show()
        
        # 销毁对话框
        dialog.Destroy()
        self.current_dialog = None
        return dialog

    def set_shutdown_status(self, status_label):
        """设置关机状态标签"""
        self.shutdown_status = status_label
    
    def set_displays(self, time_display, weekday_display):
        """设置时间和星期显示标签"""
        self.shutdown_time_display = time_display
        self.weekday_display = weekday_display
    
    def get_shutdown_time(self):
        """获取关机时间设置"""
        return bool(self.selected_hour or self.selected_minute)
    
    def get_selected_days(self):
        """获取选中的星期"""
        return self.selected_days
    
    def get_current_dialog(self):
        """获取当前打开的设置对话框"""
        return self.current_dialog

    def save_settings(self):
        """保存设置"""
        from setting_data import shutdown_settings
        
        if self.selected_hour is not None and self.selected_minute is not None:
            shutdown_settings.save_settings(
                self.selected_hour,
                self.selected_minute,
                self.selected_days
            )
        else:
            shutdown_settings.clear_settings()

    def set_language(self, lang):
        """设置语言
        
        Args:
            lang: 语言代码，'cn' 为中文，'en' 为英文
        """
        from setting_data import shutdown_settings
        shutdown_settings.set_language(lang)

