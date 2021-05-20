import time
import spacy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from collections import Counter

nlp = spacy.load('en_core_web_lg')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--start-maximized")
driver = webdriver.Chrome('chromedriver.exe', options=options)

action = ActionChains(driver)
wait = WebDriverWait(driver, 600)

driver.get("https://codenames.game/room/rose-popcorn-sweat")

input_box = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="nickname-input"]')))
input_box.send_keys('Anya')
wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()
dictionary = {}
exclude = []
once = True
onetime = True


def guess(x, y, z):
    print(x, y, z)
    clues = '-'.join(z.split(' ')[:-1])
    no = z.split(' ')[-1]
    for i in y:
        try:
            del x[i]
        except KeyError:
            pass
    temp = {}
    for word in x.keys():
        tokens = nlp(clues + ' ' + word)
        token1, token2 = tokens[0], tokens[1]
        temp[word] = token1.similarity(token2)
        print(clues, ' and ', word, ' = ', token1.similarity(token2))
    k = Counter(temp)
    if no == '∞':
        high = k.most_common(len(x.keys()/2))
    else:
        high = k.most_common(int(no))
    print(high)
    return [ans[0] for ans in high]


while True:
    ready = wait.until(EC.presence_of_element_located((By.XPATH,
                                                       '//div[@class="jsx-2970148226 bg-white px-2 py-1 rounded-lg text-base landscape:text-2xl font-bold mx-12 text-center"]'))).text
    print(ready)
    if ready == 'Try to guess a word.':
        if once:
            words = driver.find_elements_by_xpath('//div[@class="absolute"]')
            for i in words:
                dictionary[i.text] = i
            once = False
        time.sleep(2)
        exc = driver.find_elements_by_tag_name('em')
        exclude = [i.text for i in exc if ' ' not in i.text]
        clue = exc[-1].text
        if onetime:
            for res in guess(dictionary, exclude, clue):
                print(res)
                time.sleep(1.5)
                try:
                    dictionary[res].click()
                except:
                    pass
            onetime = False
    else:
        time.sleep(2)
        onetime = True
