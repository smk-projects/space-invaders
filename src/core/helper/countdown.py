from core.screen.screen_manager import ScreenManager
import time

class Countdown:
    def __init__(self, seconds: int = 0):
        self.__seconds = seconds
        self.__started_seconds = 0
        self.__remaining_seconds = 0
        self.__is_running = False

    def start(self):
        """
        啟用計時器
        """
        screen = ScreenManager.instance().get_current_screen()
        if screen is None:
            raise ValueError("Screen instance is None")
        
        self.__started_seconds = screen.elapse_seconds
        self.__is_running = True
        self.__remaining_seconds = self.__seconds
        
    def reset(self):
        """
        重設計時器
        """
        self.start()
        
    def stop(self):
        """
        強制停止計時
        """
        self.__is_running = False

    def is_running(self): 
        """
        取得計時器是否正在運行
        """
        return self.__is_running
    
    @property
    def remaining_seconds(self):
        """
        取得剩餘時間 (呼叫此方法會觸發計時器的檢查)
        """
        remaining_seconds = self.__get_remainig_seconds()
        if remaining_seconds == 0:
            self.stop()
        return  remaining_seconds
    
    @property
    def seconds(self):
        """
        取得計時器的總秒數
        """
        return self.__seconds
    
    def __get_remainig_seconds(self):
        screen = ScreenManager.instance().get_current_screen()
        if screen is None:
            raise ValueError("Screen instance is None")
        
        if not self.__is_running:
            return self.__remaining_seconds
        seconds = self.__seconds
        started_seconds = self.__started_seconds
        elapse_seconds = screen.elapse_seconds
        self.__remaining_seconds = max(0, seconds - (elapse_seconds - started_seconds))
        return self.__remaining_seconds