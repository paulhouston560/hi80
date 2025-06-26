import mouse
import time
from DrissionPage import Chromium, ChromiumOptions
from pyvirtualdisplay import Display

url = 'https://test.aiuuo.com/'
ele_for_check_path = 'x:/html/body/pre'
ele_for_check_text = 'Hello World!'

display = Display(visible=0, size=(1920, 1080))
display.start()

co = ChromiumOptions().auto_port()

arguments = [
    "--disable-gpu",
    "--no-sandbox",
#    "--window-size=1920,1080",
    "--disable-dev-shm-usage",
]

for argument in arguments:
    co.set_argument(argument)

# 使用该配置对象创建页面
browser = Chromium(co)

tab = browser.latest_tab


bypass = False

for i in range(2):
    try:
        print(f"正在开始第{i+1}次尝试")
        tab.get(url)
        tab.wait.load_start()
        ele = tab.ele("@name=cf-turnstile-response").parent()
        # 找到复选框并返回元素中点在屏幕的位置
        checkbox = ele.sr('t:iframe')('t:body').sr('t:input')
        loc = checkbox.rect.screen_midpoint
        # 找到'Verify you are human'并返回元素中点在屏幕的位置
        # ele_Confirmhuman = checkbox.next(2)
        # print(ele_Confirmhuman.text)
        # loc = ele_Confirmhuman.rect.screen_midpoint
        print(loc)
        x = loc[0]
        y = loc[1]
        print(x,y)	
        time.sleep(2)
        mouse.move(x, y, absolute=Ture, duration=0.2)
        mouse.click('left')	
        try:
            time.sleep(5)
            ele_for_check = tab.ele(ele_for_check_path)
            if ele_for_check.text == ele_for_check_text:
                print(ele_for_check.text)
                print("恭喜！验证通过。")
                bypass = True
                break
        except:
            time.sleep(1)

    except:
        print(f"第{i+1}次尝试，复选框未找到")

if not bypass:
    print("很遗憾，两次验证没有通过。")

time.sleep(5)
browser.quit()
display.stop()
