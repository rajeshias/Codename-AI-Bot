import time
import spacy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from collections import Counter
from collections import defaultdict

nlp = spacy.load('en_core_web_lg')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--start-maximized")
driver = webdriver.Chrome('chromedriver.exe', options=options)

action = ActionChains(driver)
wait = WebDriverWait(driver, 600)

driver.get("https://codenames.game/room/temple-field-yellowstone")

input_box = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="nickname-input"]')))
input_box.send_keys('Anya')
wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()
dictionary = {}
exclude = []
once = True
onetime = True


def guess(x, y, z):
    print(x, y, z)
    clues = ' '.join(z.split(' ')[:-1])
    no = z.split(' ')[-1]
    for i in y:
        try:
            del x[i]
        except KeyError:
            pass
    temp = defaultdict(int)
    for word in x.keys():
        tokens = nlp(clues + ' ' + word)
        print(tokens)
        LastToken = tokens[-1]
        for token in tokens[:-1]:
            temp[word] += token.similarity(LastToken)
    print(temp)
    k = Counter(temp)
    if no == '∞':
        high = k.most_common(len(x.keys())//2)
    else:
        high = k.most_common(int(no)*2)
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
        try:
            exc = driver.find_elements_by_tag_name('em')
            exclude = [i.text for i in exc if ' ' not in i.text]            
            clue = exc[-1].text
        except:
            dictionary = {}
            exclude = []
            once = True
            onetime = True
            continue
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
