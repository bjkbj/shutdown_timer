import wx
import wx.adv

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
            cancel_text = "取消"
        else:
            title = "Shutdown Settings"
            time_label_text = "Select shutdown time:"
            weekday_label_text = "Select repeat days:"
            weekdays = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            ok_text = "OK"
            cancel_text = "Cancel"
        
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
        cancel_button = wx.Button(panel, wx.ID_CANCEL, cancel_text)
        button_sizer.Add(ok_button, 0, wx.ALL, 5)
        button_sizer.Add(cancel_button, 0, wx.ALL, 5)
        main_sizer.Add(button_sizer, 0, wx.ALL|wx.LEFT, 10)  # 靠左对齐
        
        panel.SetSizer(main_sizer)
        
        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.on_ok, ok_button)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_button)
    
    def on_ok(self, event):
        """确定按钮事件处理"""
        selected_hour = self.hour_choice.GetSelection()
        selected_minute = self.minute_choice.GetSelection()
        
        # 获取选中的星期
        selected_days = []
        for i, cb in enumerate(self.weekday_boxes):
            if cb.GetValue():
                selected_days.append(i)
        
        # 保存设置到settings_manager
        settings_manager = self.parent.settings_manager
        settings_manager.selected_hour = selected_hour
        settings_manager.selected_minute = selected_minute
        settings_manager.selected_days = selected_days
        
        self.EndModal(wx.ID_OK)
    
    def on_cancel(self, event):
        """取消按钮事件处理"""
        # 清除设置管理器中的数据
        settings_manager = self.parent.settings_manager
        settings_manager.selected_hour = 0
        settings_manager.selected_minute = 0
        settings_manager.selected_days = []
        
        # 清除显示
        if settings_manager.shutdown_time_display:
            settings_manager.shutdown_time_display.SetLabel("")
        if settings_manager.weekday_display:
            settings_manager.weekday_display.SetLabel("")
        if settings_manager.shutdown_status:
            settings_manager.shutdown_status.Hide()
        
        # 关闭对话框
        self.EndModal(wx.ID_CANCEL)
    
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
            self.FindWindow(wx.ID_CANCEL).SetLabel("取消")
        else:
            # 更新英文界面文本
            for i, cb in enumerate(['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']):
                self.weekday_boxes[i].SetLabel(cb)
            self.FindWindow(wx.ID_OK).SetLabel("OK")
            self.FindWindow(wx.ID_CANCEL).SetLabel("Cancel")

class SettingsManager:
    def __init__(self, parent, colors):
        self.parent = parent
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

