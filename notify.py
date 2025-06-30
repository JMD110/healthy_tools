import subprocess
import datetime
import time


def is_work_day():
    weekday = datetime.datetime.now().weekday()
    return weekday < 5


def is_work_time():
    now = datetime.datetime.now()
    morning_start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
    morning_end_time = now.replace(hour=11, minute=30, second=0, microsecond=0)
    noon_start_time = now.replace(hour=13, minute=30, second=0, microsecond=0)
    noon_end_time = now.replace(hour=17, minute=30, second=0, microsecond=0)
    return (
        morning_start_time <= now <= morning_end_time
        or noon_start_time <= now <= noon_end_time
    )


def show_alert(title, message, buttons=["OK"]):
    button_string = ", ".join([f'"{btn}"' for btn in buttons])
    command = [
        "osascript",
        "-e",
        f'display alert "{title}" message "{message}" buttons {{{button_string}}} default button "{buttons[0]}"',
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if "button returned:" in result.stdout:
        return result.stdout.split("button returned:")[1].strip()
    return None


class Scheuler(object):
    EVERY_30_MINUTES = ("%M%S", ("3000", "0000"))
    CLOCK_11_14 = ("%H%M%S", ("110000", "140000"))


# examples
if __name__ == "__main__":
    alert_items = [
        # 每半小时站起来活动一下
        (
            Scheuler.EVERY_30_MINUTES,
            "站起来活动一下,喝水",
            "每半小时站起来活动一下，保持身体健康！喝水!",
        ),
        # 每天中午11点,14点提醒眼保健操
        (
            Scheuler.CLOCK_11_14,
            "眼保健操时间",
            "每天中午11点和14点提醒做眼保健操，保护视力！",
        ),
    ]
    while True:
        time.sleep(1)
        now = datetime.datetime.now()
        if not is_work_day() or not is_work_time():
            continue
        for alert_item in alert_items:
            if now.strftime(alert_item[0][0]) in alert_item[0][1]:
                show_alert(alert_item[1], alert_item[2])
