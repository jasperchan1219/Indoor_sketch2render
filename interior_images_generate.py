from selenium import webdriver
import time
import urllib
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# 存圖位置
local_path = './data/interior-styles/japanese'
# 頁面網址（在google圖片搜尋關鍵字後複製網址）
url = 'https://www.google.com/search?q=japanese+style+interior+design&sxsrf=APwXEdcAOzrQXkcqBIFJaaWJxB0RPUMbmw:1682679434902&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiDv_Ovtcz-AhWst1YBHf13B9EQ_AUoAXoECAEQAw&biw=1512&bih=834&dpr=2'
chromeDriver = r'/usr/local/bin/chromedriver.exe' # chromedriver檔案放的位置，要先到chrome的設定->關於chrome 看自己的chrome版本，並下載對應的chromedriver.exe到/usr/local/bin/，下載網址：https://chromedriver.chromium.org/downloads
driver = webdriver.Chrome(service=Service(chromeDriver)) 
  
# 最大化窗口，因為每一次爬取只能看到視窗内的圖片
driver.maximize_window()  
  
# 紀錄下載過的圖片網址，避免重複下載  
img_url_dic = {}  

# 瀏覽器打開爬取頁面
driver.get(url)  

# 模擬滾動視窗瀏覽更多圖片
pos = 0  
m = 0 # 圖片編號 
for i in range(100):  
    pos += i*500 # 每次下滾500  
    js = "document.documentElement.scrollTop=%d" % pos  
    driver.execute_script(js)  
    time.sleep(1)
    for j in range(60):
        for k in range(60):
            xpath = '//*[@id="islrg"]/div[1]/div['+str(j)+']/div['+str(k)+']/a[1]/div[1]/img'
            for element in driver.find_elements(By.XPATH,xpath):
                try:
                    img_url = element.get_attribute('src')
                    # 保存圖片到指定路徑
                    if img_url != None and not img_url in img_url_dic:
                        img_url_dic[img_url] = ''  
                        m += 1
                        # print(img_url)
                        # ext = img_url.split('/')[-1]
                        # print(ext)
                        # filename = str(m) + 'interior' + '_' + ext +'.jpg'
                        filename = 'japanese' + str(m+48) +'.jpg'
                        print(filename)
                        # 保存圖片
                        urllib.request.urlretrieve(img_url, os.path.join(local_path , filename))
                except OSError:
                    print('發生OSError!')
                    print(pos)
                    break
            
driver.close()
