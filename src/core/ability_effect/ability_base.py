from abc import abstractmethod
from core.helper import Countdown

class AbilityBase:
    def __init__(self, keep_sec: int = 10, cooldown_sec: int = 10):
        """
        升級物件的基底類別
        - keep_sec: 升級效果持續時間
        - colddown_sec: 升級效果冷卻時間
        """
        self.__keep_sec = keep_sec
        self.__cooldown_sec = cooldown_sec
        self.__effect_countdown = Countdown(keep_sec)
        self.__cooldown_countdown = Countdown(cooldown_sec)
        self._enabled = False

    def enable(self):
        """
        啟用升級效果
        """
        if self._enabled:
            return        
        self.__effect_countdown.start()
        self.__cooldown_countdown.start()
        self._enabled = True
        
    def disable(self):
        """
        停用升級效果
        """
        if not self._enabled:
            return
        self.__effect_countdown.stop()
        self._enabled = False
    
    def is_enabled(self):
        """
        判斷升級效果是否啟用
        """
        return self._enabled
    
    @property
    def effect_remaining(self):
        """
        取得升級效果剩餘時間(秒)
        """
        if not self.__effect_countdown.is_running():
            return 0
        remaining = self.__effect_countdown.remaining_seconds        
        return remaining
    
    @property
    def cooldown_remaining(self):
        """
        取得升級效果冷卻剩餘時間(秒)
        """
        remaining = self.__cooldown_countdown.remaining_seconds        
        return remaining

    @property
    def effect_seconds(self):
        """
        取得升級效果持續時間
        """
        return self.__keep_sec
    
    @property
    def cooldown_seconds(self):
        """
        取得升級效果冷卻時間
        """
        return self.__cooldown_sec

    def reset(self):
        """
        重置升級物件的狀態
        """
        self.__effect_countdown.reset()
        self.__cooldown_countdown.reset()
        pass