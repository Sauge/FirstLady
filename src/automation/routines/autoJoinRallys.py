from src.automation.routines.routineBase import TimeCheckRoutine
from src.core.image_processing import find_and_tap_template, find_template
import time
from src.core.adb import press_back, tap_screen
from src.game.controls import navigate_home,humanized_tap
import random
from src.core.logging import app_logger

class AutoJoinRallysRoutine(TimeCheckRoutine):
    def _execute(self) -> bool:
        """Check and click help button if available"""
        return self.execute_with_error_handling(self._execute_internal)

    def _execute_internal(self) -> bool:
        if find_and_tap_template(
            self.device_id,
            "map",
            error_msg="Already on map screen",
            success_msg="Opened map screen"
        ):
            time.sleep(1)

        if find_and_tap_template(self.device_id, 'collect_rally_icon'):
            time.sleep(0.2)

            claim_loc = find_template(self.device_id, 'collect_rally_claim')
            confirm_loc = find_template(self.device_id, 'collect_rally_confirm')
            if claim_loc:
                humanized_tap(self.device_id, claim_loc[0], claim_loc[1])
                time.sleep(0.2)
            if confirm_loc:
                humanized_tap(self.device_id, confirm_loc[0], confirm_loc[1])
                time.sleep(0.2)

        if find_and_tap_template(
            self.device_id,
            "rally_icon",
            error_msg="No rally open at this time",
            success_msg="Starting rally join sequence!"
        ):

            if find_and_tap_template(
                self.device_id,
                "rally_available",
                error_msg="Could not find any rallys",
                success_msg="Starting joining rally!"
            ):
                time.sleep(0.4)

                if find_and_tap_template(
                        self.device_id,
                        "rally_join",
                        error_msg="Could not rally, all squads are out",
                        success_msg="Joined rally!"
                    ):
                        time.sleep(0.2)

                        find_and_tap_template(
                            self.device_id,
                            "rally_back_home",
                            error_msg="Already on home screen",
                            success_msg="Navigated back to home"
                        )
                        time.sleep(round(random.uniform(0.1, 1), 2))
                        return True
                else:
                    navigate_home(self.device_id)

            else:
                navigate_home(self.device_id)

            time.sleep(round(random.uniform(0.1, 1), 2))


        return True
    