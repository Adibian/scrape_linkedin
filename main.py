# """ filename: script.py """
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import parameters
from time import sleep
from selenium import webdriver
import json
import threading
import random
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

# req_proxy = RequestProxy() #you may get different number of proxy when  you run this at each time
# proxies = req_proxy.get_proxy_list() #this will create proxy list

import ast
with open('new_persons.txt','r') as f:
   all_new_persons = ast.literal_eval(f.read())
with open('old_persons.txt','r') as f:
   all_old_persons = ast.literal_eval(f.read())
   if not all_old_persons:
       all_old_persons = set()
with open('all_info.json', 'r') as all_info_file:
    # Reading from json file
    all_info = json.load(all_info_file)
# all_new_persons = {'behzad-mahmoudi-76a57572', 'navid-yousefian-25a09040', 'abbas-karimzadeh-a344724a',
#                    'majid-nouri-b7095457', 'businessleadersofiran'}


def get_proxies():
    req_proxy = RequestProxy()  # you may get different number of proxy when  you run this at each time
    proxies = req_proxy.get_proxy_list()  # this will create proxy list
    return proxies
# proxies = get_proxies()
proxies = ['86.105.130.124:6588', 's2.safegozar.in:443', '', '']

# 123456:123456@
def get_info(driver, current_person):

    """
        We want to be sure to connect to page by using proxy
        If it didn't connect try again three times
    """
    name = ''
    description = ''
    new_persons = []
    j = 0
    while j < 3:
        try:
            driver.get('https://www.linkedin.com/in/{}'.format(current_person))
            try:
                name = driver.find_element_by_xpath(
                    '/html/body/div/div/div/div/div/div/div/div/main/div/section/div/div/div/ul/li').text
                description = driver.find_element_by_xpath(
                    '/html/body/div/div/div/div/div/div/div/div/main/div/section/div/div/div/h2').text
                new_persons = driver.find_elements_by_xpath(
                    '/html/body/div/div/div/div/div/div/div/div/div/div/div/section/ul/li[*]/a')
            except:
                name = driver.find_element_by_xpath(
                    '/html/body/main/section[1]/section/section[1]/div/div[1]/div[1]/h1').text
                description = driver.find_element_by_xpath(
                    '/html/body/main/section[1]/section/section[1]/div/div[1]/div[1]/h2').text
                new_persons = driver.find_elements_by_xpath(
                    '/html/body/div/div/div/div/div/div/div/div/div/div/div/section/ul/li[*]/a')
            break
        except:
            driver.execute_script('''window.open("http://bings.com","_blank");''')
            windows = driver.window_handles
            driver.switch_to.window(window_name=windows[-1])
            j += 1
    if j == 3:
        return False

    # skills = driver.find_elements_by_xpath(
    #     '/html/body/div[6]/div[4]/div[3]/div/div/div/div/div[2]/main/div[2]/div[6]/div/section/ol/li[*]')

    person_info = {'urn': current_person, 'name': name, 'description': description}

    """
        Getting new person in this page
    """
    global all_new_persons
    global all_old_persons
    # new_persons = driver.find_elements_by_xpath(
    #     '/html/body/div/div/div/div/div/div/div/div/div/div/div/section/ul/li[*]/a')
    for new_person in new_persons:
        link = new_person.get_attribute('href')
        new_link = link[:link.rfind('/')]
        urn = new_link[new_link.rfind('/') + 1:]
        if urn not in all_old_persons:
            all_new_persons.add(urn)

    """
        We want to be sure to connect to page by using proxy
        If it didn't connect try again three times 
    """
    j = 0
    while j < 3:
        try:
            driver.get('https://www.linkedin.com/in/{}/detail/recent-activity/shares'.format(current_person))
            break
        except:
            driver.execute_script('''window.open("http://bings.com","_blank");''')
            windows = driver.window_handles
            driver.switch_to.window(window_name=windows[-1])
            j += 1
    if j == 3:
        return False

    """
        Checking to be there any posts or not
        If there is no posts it returns person_info
    """
    try:
        test_is_any_posts = driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/div/div/div/p[2]').text
        if test_is_any_posts == 'Check back for any new updates.':
            person_info['posts'] = []
            return person_info
    except:
        pass

    """
        scroll to bottom of page
    """
    SCROLL_PAUSE_TIME = 3
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    i = 0
    while i < 5:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        i += 1
    """
        click on 'comment' button to show comments
    """
    # buttons = driver.find_elements_by_xpath(
    #     '/html/body/div[6]/div[4]/div[3]/div/div/div/div/div/div[2]/div/div[*]/div/div[5]/div/div[2]/span[2]/button')
    # if not buttons:
    #     buttons = driver.find_elements_by_xpath(
    #         '/html/body/div[5]/div[4]/div[3]/div/div/div/div/div/div[2]/div/div[*]/div/div[5]/div/div[2]/span[2]/button')
    # for b in buttons:
    #     driver.execute_script("arguments[0].click();", b)

    posts = driver.find_elements_by_xpath(
        '/html/body/div/div/div/div/div/div/div/div/div/div/div')
    if not posts:
        posts = driver.find_elements_by_xpath(
            '/html/body/div[5]/div[4]/div[3]/div/div/div/div/div/div[2]/div/div')
    print("posts number: " + str(posts.__len__()))
    # file = open('file.txt', 'w', encoding='utf-8')
    current_posts = []
    for post in posts:
        try:
            post_text = post.find_element_by_xpath('./div/div/div/div/div/span/span').text
            current_posts.append(post_text)
            # file.write(post_text)
            # file.write('\n' + 'comments:')
        except:
            continue
        # try:
        #     comments_text = post.find_element_by_xpath('./div/div/div/div/div[2]').text
        #     current_posts[post_text] = comments_text
        #     # file.write(comments_text)
        #     # file.write("\n################\n################\n")
        # except:
        #     current_posts[post_text] = ''
        #     # file.write("\n################\n################\n")
    person_info['posts'] = current_posts
    return person_info


def start_scrap(i, proxy_index):
    global proxies
    # # print(proxies[])
    # PROXY = proxies[proxy_index].get_address()
    PROXY = proxies[proxy_index]
    if PROXY:
        chrome_options = Options()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "proxyType": "MANUAL",
            "socksUsername": '123456',
            "socksPassword": '123456',
        }
        # chrome_options = webdriver.ChromeOptions()
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('chromedriver_win32/chromedriver.exe', options=chrome_options)
        # driver = webdriver.Chrome('chromedriver2_win32/chromedriver.exe', options=chrome_options)
    else:
        driver = webdriver.Chrome('chromedriver_win32/chromedriver.exe')

    """
        We want to be sure to connect to page by using proxy
        If it didn't connect try again three times 
    """
    username_part = None
    password_part = None
    sign_in_button = None
    j = 0
    while j < 3:
        try:
            driver.get('https://www.linkedin.com/login')
            username_part = driver.find_element_by_id('username')
            password_part = driver.find_element_by_id('password')
            sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
            break
        except:
            driver.execute_script('''window.open("http://bings.com","_blank");''')
            windows = driver.window_handles
            driver.switch_to.window(window_name=windows[-1])
            j += 1
    if j == 3:
        driver.quit()
        return False
    sleep(1)
    if i == 0:
        username = parameters.linkedin_username1
        password = parameters.linkedin_password1
    elif i == 1:
        username = parameters.linkedin_username2
        password = parameters.linkedin_password2
    elif i == 2:
        username = parameters.linkedin_username3
        password = parameters.linkedin_password3
    else:
        username = parameters.linkedin_username4
        password = parameters.linkedin_password4

    # username_part = driver.find_element_by_id('username')
    username_part.send_keys(username)
    # sleep(0.5)

    # password_part = driver.find_element_by_id('password')
    password_part.send_keys(password)
    # sleep(0.5)

    # sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    sign_in_button.click()
    # sleep(0.5)

    global all_info
    global all_new_persons
    global all_old_persons
    numbers_of_this_scrap = 0
    while all_new_persons.__len__() and all_old_persons.__len__() < 100 and numbers_of_this_scrap < 60:
        current_person = all_new_persons.pop()
        # witch_new_persons = 1
        person_info = get_info(driver, current_person)
        if not person_info:
            driver.quit()
            return False
        # witch_new_persons += 1
        all_info[current_person] = person_info
        all_old_persons.add(current_person)
        print(person_info)
        print("##########")
        numbers_of_this_scrap += 1
        sleep(random.choice([0.5, 1, 2]))
        print("numbers of old persons = " + str(len(all_old_persons)))
        print("numbers of new persons = " + str(len(all_new_persons)))
    return True


def start_thread(i):
    global proxies
    number_of_try = i
    this_try = start_scrap(i, number_of_try)
    while not this_try:
        # number_of_try += 4
        if number_of_try > len(proxies):
            break
        this_try = start_scrap(i, number_of_try)

start_time = time.time()
# t1 = threading.Thread(target=start_thread, args=(0,))
# t2 = threading.Thread(target=start_thread, args=(1,))
t3 = threading.Thread(target=start_thread, args=(2,))
# t4 = threading.Thread(target=start_thread, args=(3,))
# t5 = threading.Thread(target=start_thread, args=(4,))
# t1.start()
# sleep(1)
# t2.start()
# sleep(2)
t3.start()
sleep(3)
# t4.start()
# sleep(2)
# t5.start()
# t1.join()
# t2.join()
t3.join()
# t4.join()
# t5.join()
print("all thread are finished")
print("#######################")
end_time = time.time()

json_info = json.dumps(all_info)
f1 = open("all_info.json", "w")
f1.write(json_info)
f1.close()

f2 = open("new_persons.txt", "w")
f2.write(str(all_new_persons))
f2.close()

f3 = open("old_persons.txt", "w")
f3.write(str(all_old_persons))
f3.close()

print(end_time - start_time)
# driver.quit()
