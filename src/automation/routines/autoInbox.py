from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template, find_all_templates
from src.game.controls import navigate_home
from src.core.logging import app_logger
from src.core.adb import input_message, press_back, tap_screen
import time
from src.core.config import CONFIG

class AutoInboxRoutine(TimeCheckRoutine):
    def _execute(self) -> bool:
        """Check and click message button if available"""
        return self.execute_with_error_handling(self._execute_internal)
        
    def _execute_internal(self) -> bool:
        
        message = CONFIG['auto_inbox']

        if find_and_tap_template(
            self.device_id,
            "map",
            error_msg="Already on map screen",
            success_msg="Opened map screen"
        ):
            time.sleep(1) 

        if find_and_tap_template(
            self.device_id,
            "message_notifier",
            error_msg="No inbox message at this time",
            success_msg="Found inbox icon, proceeding to inbox"
        ):
            find_and_tap_template(
                self.device_id,
                "message_chat_box",
                error_msg="Could not find message chat box",
                success_msg="Found message chat box"
            )
            time.sleep(1)
            input_message(self.device_id, message)
            time.sleep(1)

            find_and_tap_template(
                self.device_id,
                "message_send",
                error_msg="Could not find send message button",
                success_msg="Send message"
            )
            time.sleep(1)
            find_and_tap_template(
                self.device_id,
                "message_back",
                error_msg="Could not find message back button",
                success_msg="Found message back button"
            )
            
            all_messages = find_all_templates(
                self.device_id,
                "message_indicator"
            )

            app_logger.info(f"Answered initial message")

            for x, y in all_messages:
              tap_screen(self.device_id, x, y)
              find_and_tap_template(
                  self.device_id,
                  "message_chat_box",
                  error_msg="Could not find message chat box",
                  success_msg="Found message chat box"
              )
              time.sleep(1)
              input_message(self.device_id, message)
              time.sleep(1)

              find_and_tap_template(
                  self.device_id,
                  "message_send",
                  error_msg="Could not find send message button",
                  success_msg="Send message"
              )
              time.sleep(1)
              find_and_tap_template(
                  self.device_id,
                  "message_back",
                  error_msg="Could not find message back button",
                  success_msg="Found message back button"
              )

            find_and_tap_template(
                self.device_id,
                "message_back",
                error_msg="Could not find messages back button",
                success_msg="Left messages"
            )
            app_logger.info(f"Answered {len(all_messages)} messages")
          
        return True 
