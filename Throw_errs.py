from PyQt5.QtWidgets import QMessageBox

class Throw_errs():
    """
    抛出异常
    """
    def __init__(self) -> None:
        pass
    
    # 添加一个方法来验证最小值和最大值  
    def validate_serial_range(self, max_content, min_content) -> bool:  
        max_value = max_content.text()  
        min_value = min_content.text()  
        
        if not max_value or not min_value:  
            # 如果任一值为空，则不进行验证，或者可以显示错误消息  
            return False  
        
        try:  
            max_value = int(max_value)  
            min_value = int(min_value)  
            
            if min_value > max_value:  
                # 如果最小值大于最大值，显示错误消息或采取其他措施  
                QMessageBox.warning(self, "Error", "输入的数值范围不正确")  
                return False  
            else:  
                return True  
        except ValueError:  
            # 如果转换到整数失败，显示错误消息或采取其他措施  
            QMessageBox.warning(self, "Error", "请输入有效的数字")  
            return False  
