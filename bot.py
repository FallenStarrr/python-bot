
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from data import  users_settings_dict
import time
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import requests
import os
import json





class InstagramBot():
    """Instagram Bot на Python by PythonToday"""

    def __init__(self, username, password):
       
        self.username = username
        self.password = password


        #options = Options()
        #options.add_argument(f"--window-size={window_size}")
        #options.add_argument("--headless")
        #self.browser = webdriver.Chrome("../chromedriver/chromedriver", options=options)


        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    # метод для закрытия браузера
    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    # метод логина
    def login(self):

        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(5, 7))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

    # метод ставит лайки по hashtag
    def like_photo_by_hashtag(self, hashtag):

        for item in hashtag:
            browser = self.browser
            browser.get(f'https://www.instagram.com/explore/tags/{item}/')


            for i in range(1, 2):
                browser.execute_script("window.scrollTo(0, 100)")
                time.sleep(random.randrange(3, 5))

                hrefs = browser.find_elements_by_tag_name('a')
                posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
                set(posts_urls)


                for url in posts_urls[0:3]:
                    try:
                        browser.get(url)
                        time.sleep(8)
                        like_button = browser.find_element_by_xpath(
                        '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                        name_btn = '/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div/span/a'
                        browser.find_element_by_xpath(name_btn).click()
                        time.sleep(8)
                        sub_btn = '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button'
                        browser.find_element_by_xpath(sub_btn).click()
                        time.sleep(5)
                        browser.back()
                        browser.back()
                        time.sleep(random.randrange(10))


                    except Exception as ex:
                        print(ex)
                        self.close_browser()


                    time.sleep(5)

        

    # метод проверяет по xpath существует ли элемент на странице
    def xpath_exists(self, url):

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True


        except NoSuchElementException:
            exist = False

        return exist

    # метод собирает ссылки на все посты пользователя
    def get_all_posts_urls(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя не существует, проверьте URL")
            self.close_browser()


        else:
            print("Пользователь успешно найден, ставим лайки!")
            time.sleep(2)

            posts_count = int(browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            loops_count = int(posts_count / 12)
        

            posts_urls = []


            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")

            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

    # метод ставит лайки по ссылке на аккаунт пользователя
    def put_many_likes(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list[0:6]:
                try:
                    browser.get(post_url)
                    time.sleep(2)

                    like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                    browser.find_element_by_xpath(like_button).click()
                    # time.sleep(random.randrange(80, 100))
                    time.sleep(2)

                    print(f"Лайк на пост: {post_url} успешно поставлен!")


                except Exception as ex:
                    print(ex)
                    self.close_browser()

        self.close_browser()

    # метод ставит лайк на пост по прямой ссылке
    def put_exactly_like(self, userpost):

        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого поста не существует, проверьте URL")
            self.close_browser()


        else:
            print("Пост успешно найден, ставим лайк!")
            time.sleep(2)

            like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
            browser.find_element_by_xpath(like_button).click()
            time.sleep(2)

            print(f"Лайк на пост: {userpost} поставлен!")
            self.close_browser()
   

        self.close_browser()


    def download_userpage_content(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        # создаём папку с именем пользователя для чистоты проекта
        if os.path.exists(f"{file_name}"):
            print("Папка уже существует!")


        else:
            os.mkdir(file_name)

        img_and_video_src_urls = []


        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list:
                try:
                    browser.get(post_url)
                    time.sleep(4)

                    img_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img"
                    video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
                    post_id = post_url.split("/")[-2]

                    if self.xpath_exists(img_src):
                        img_src_url = browser.find_element_by_xpath(img_src).get_attribute("src")
                        img_and_video_src_urls.append(img_src_url)

                        # сохраняем изображение
                        get_img = requests.get(img_src_url)
                        with open(f"{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)

                    elif self.xpath_exists(video_src):
                        video_src_url = browser.find_element_by_xpath(video_src).get_attribute("src")
                        img_and_video_src_urls.append(video_src_url)

                        # сохраняем видео
                        get_video = requests.get(video_src_url, stream=True)
                        with open(f"{file_name}/{file_name}_{post_id}_video.mp4", "wb") as video_file:
                            for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    video_file.write(chunk)
                    else:
                        # print("Упс! Что-то пошло не так!")
                        img_and_video_src_urls.append(f"{post_url}, нет ссылки!")
                    print(f"Контент из поста {post_url} успешно скачан!")

                except Exception as ex:
                    print(ex)
                    self.close_browser()

            self.close_browser()

        with open(f'{file_name}/{file_name}_img_and_video_src_urls.txt', 'a') as file:
            for i in img_and_video_src_urls:
                file.write(i + "\n")


    def get_all_followers(self, user):
    
        browser = self.browser
        browser.get(user)
        time.sleep(4)
        file_name = user.split('/')[-2]

    # Папка с именем пользователя для чистоты

        if os.path.exists(f'{file_name}'):
            print(f'Папка есть {file_name}')

        else:
            print(f'Создаем пользователя {file_name}')
            os.mkdir(f'{file_name}')


        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
                print("Такого пользователя не существует, проверьте URL")
                self.close_browser()

        else:
            print("Пользователь успешно найден, скачиваем ссылки!")  
            time.sleep(2)
            follower_btn = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span') 
            #follower_count = follower_btn.text
            #follower_count = int(follower_count.split(' ')[0])
            follower_count = follower_btn.get_attribute('title')

            if ' ' in follower_count:
                follower_count = int(''.join(follower_count.split(' ')))

            else:
                follower_count = int(follower_count)

            print(f'Количество подписчиков: {follower_count}')
            time.sleep(2)

            loop_count = int(follower_count / 12)
            print(f'Число итераций {loop_count}')
            time.sleep(2)
            
            follower_btn.click()
            time.sleep(2)
            
            followers_ul = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')
            
            try:
                followers_urls = []

                
                for i in range(1, loop_count + 1):
                    browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', followers_ul)
                    time.sleep(2)
                    print(f'Итерация #{i}')



                all_urls_div = followers_ul.find_elements_by_tag_name('li')

                for url in all_urls_div:
                    url = url.find_element_by_tag_name('a').get_attribute('href')
                    followers_urls.append(url)

                # сохраняем всех подписчиков в файл
                with open(f'{file_name}/{file_name}.txt', 'a') as text_file:
                     for link in followers_urls:
                         text_file.write(link + '\n')

                with open(f'{file_name}/{file_name}.txt', 'a') as text_file:
                     users_urls = text_file.readlines()

                     for user in users_urls[0:10]:
                        try:

                          try:
                            
                             with open(f'{file_name}/{file_name}.sub_list.txt', 'r') as sub_list_file:
                                      lines = sub_list_file.readlines()
                                      if user in lines:
                                          print(f'Мы уже подписан на {user}, слудующий юзер')
                                          continue


                          except Exception as ex:
                              print('Файл с ссылками нет')
                              print(ex)
                              self.close_browser()

                          browser = self.browser
                          browser.get(user)
                          page_owner = user.split('/')[-2]

                          if self.xpath_exists('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/a'):

                             print('Это профиль мой')

                          elif self.path.exists('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button/div/span'):
                             print('Мы уже подписаны на {page_owner} пропускаем итерацию')         

                          else:
                             time.sleep(2)

                             if self.xpath_exists('/html/body/div[1]/section/main/div/div/article/div[1]/div/h2'):
                                 
                                 try:
                                     follow_btn = browser.find_element_by_xpath(
                                         '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button'
                                     ).click()
                                     print(f'Запросили подписку на юзера {page_owner}. Закрытый акк!')


                                 except Exception as ex:
                                    print(ex)


                             else:


                                 try:


                                     if self.path_exists('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button'):
                                         follower_btn = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button').click()
                                         print(f'Подписались на {page_owner} Открытый акк')


                                     else:
                                         follower_btn = browser.find_element_by_xpath(
                                             '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button'
                                         ).click() 
                                         print(f'Подписались на юзера{page_owner} Открытый акк')

                                 except Exception as e:
                            
                                        print(e) 
                            # записываем данные в файл для ссылок всех подписок если файла нет, создаем, если есть - дополняем
                             with open(f'{file_name}/{file_name}_sub_list.txt', 'a') as sub_list_file:
                                sub_list_file.write(user)


                             time.sleep(7)


                        except Exception as ex:
                                    print(ex)                      
                        

            except Exception as ex:

                print(ex)
        
                self.close_browser()    

            
# метод для отправки сообщений
    def send_message(self, user="", message=""):

        browser = self.browser
        time.sleep(2)

        msg_btn = browser.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a')

       
        msg_btn.click()
        time.sleep(2)

        # отключаем всплывающее окно
        if self.xpath_exists('/html/body/div[5]/div/div/div'):
            browser.find_element_by_xpath('/html/body/div[5]/div/div/div/div[3]/button[2]').click()
        time.sleep(4) 

        # вводим получателя
        btn = browser.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button').click()
        to_input = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/input')
        to_input.send_keys(user)
        time.sleep(2)

        # выбираем получателя из списка
        user_list = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/div[2]').find_element_by_tag_name('button').click()
        time.sleep(2)
        next = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div[2]/div/button').click()
        time.sleep(2)
        message_btn = browser.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
        message_btn.clear()
        message_btn.send_keys(message)
        time.sleep(2)
        message_btn.send_keys(Keys.ENTER)
        self.close_browser()
 

for user, user_data in users_settings_dict.items():
    username = user_data['login']
    password = user_data['password']
    bot = InstagramBot(username, password)
    bot.login()
    bot.like_photo_by_hashtag(
    [
        #'программирование', 
        #'js', 
        'вебразработка',
        'react'
    ]
    )

    
    #bot.get_all_followers('https://www.instagram.com/angdigsthepunkrocks/')
    bot.close_browser()
    time.sleep(2)




#bot = InstagramBot(username1, password2)
#bot.login()
#bot.like_photo_by_hashtag('surfing')
#bot.send_message('fedorchenkovlad9', 'hee are you here?')
#bot.get_all_followers("https://www.instagram.com/angdigsthepunkrocks/")