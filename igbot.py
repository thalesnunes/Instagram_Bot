from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
from secrets import ig_username, ig_password
from ferramentas import header, menu



class InstagramBot:

    def __init__(self, username, password):
        '''
        Bot that interacts with Instagram, it can comment, like follow and unfollow

        Args:
            username:string: username to an Instagram account
            password:string: password to an Instagram account
            
        Attributes:
            username:string: username given
            password:string: password given
            base_url:string: instagram website (https://www.instagram.com)
            driver:selenium.webdriver.Chrome: driver that performs actions in the browser
        '''
        
        self.username = username
        self.password = password
        self.base_url = 'https://www.instagram.com'

        self.driver = webdriver.Chrome('chromedriver.exe')
        self.driver.get(self.base_url)

        sleep(1)

        self.login()


    def login(self):
        '''
        Logs in to the instagram account with the given username and password

        Args:   
            None
        '''

        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        sleep(1)
        self.driver.find_elements_by_xpath("//div[contains(text(), 'Entrar')]")[0].click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Agora não')]").click()
        sleep(2)
        try:
            self.driver.find_element_by_xpath("//button[contains(text(), 'Agora não')]").click()
        except:
            pass


    def go_to_profile(self, user):
        '''
        Goes to the given profile page 
        
        Args:
            user:str: profile to go to
        '''

        self.driver.get(f'{self.base_url}/{user}/')


    def comment(self, users, post_url, n_users=1, msg=''):
        '''
        Comments the only post in a page, choosing a random string from the users list

        Args:
            users:list: list of users to pick from
            url:string: url from the post to go to
            n_users(optional):int: number of users to pick from the list
            msg(optional):str: message to be added after the mentions
        '''

        self.driver.get(post_url)
        sleep(2)

        comm = self.driver.find_element_by_xpath('//textarea[@aria-label="Adicione um comentário..."]')
        self.driver.execute_script("arguments[0].scrollIntoView(false);", comm)
        n_interactions = 0
        while True:
            if n_interactions == 30:
                n_interactions = 0
                sleep(random.randint(900, 1200))
            try:
                self.driver.find_element_by_xpath('//textarea[@aria-label="Adicione um comentário..."]').click()
                sleep(random.randint(1, 4))
                comm = self.driver.find_element_by_xpath('//textarea[@aria-label="Adicione um comentário..."]')
                text = f'{" ".join(random.sample(users, n_users))} {msg}'
                self.person_typing(text, comm)
                sleep(random.randint(45, 120))
                self.driver.find_element_by_xpath('//button[contains(text(), "Publicar")]').click()
                n_interactions += 1
            except Exception as e:
                print(e)


    @staticmethod
    def person_typing(sentence, writing_box):
        '''
        Types letter by letter, with random intervals of time in between

        Args:
            sentence:string: text to be written
            writing_box:selenium.webdriver.Chrome.find_element_by_xpath: path to the writing box
        '''
        for letter in sentence:
            writing_box.send_keys(letter)
            sleep(random.randint(1, 5)/20)

    
    def scroll_end_page(self):

        last_height, height = 0, 1
        while last_height != height:
            last_height = height
            height = self.driver.execute_script('''
                     window.scrollTo(0, document.body.scrollHeight);
                     return window.scrollHeight;
                         ''')
            sleep(random.randint(3, 5))


    def follow_profiles(self, n_profiles):
        '''
        Follows number of profiles going to the Explore page. Excludes unwanted profiles

        Args:
            n_profiles:int: number of profiles to be followed
        '''

        self.driver.find_element_by_xpath('//a[@href="/explore/people/"]').click()
        sleep(4)

        class_user = '                    Igw0E   rBNOH        eGOV_     ybXk5    _4EzTm                                                                                   XfCBB          HVWg4                 '
        class_followers = '_7UhW9  PIoXz       MMzan   _0PwGv            fDxYl     '
        unwanted = ['Seguido por thalesnunes1 + mais 1 pessoas', 'Seguido por thalesnunes1',
                    'Seguido por _nataliaaguiar + mais 1 pessoas', 'Seguido por _nataliaaguiar']
        
        while n_profiles > 0:
            
            self.scroll_end_page()
            
            blocks = self.driver.find_elements_by_xpath(f'//div[@class="{class_user}"]')
            unique_tags = [elem.get_attribute('aria-labelledby') for elem in blocks]
            
            for tag in unique_tags:
                following = self.driver.find_element_by_xpath(f'//div[@aria-labelledby="{tag}"]//div[@class="{class_followers}"]').text
                if following in unwanted:
                    continue
                else:
                    prof_path = self.driver.find_element_by_xpath(f'//div[@aria-labelledby="{tag}"]//button[contains(text(), "Seguir")]')
                    self.driver.execute_script("arguments[0].scrollIntoView(false);", prof_path)
                    sleep(1)
                    prof_path.click()
                    n_profiles -= 1
                    if n_profiles == 0:
                        break
                    sleep(1)

            if n_profiles > 0:
                self.driver.refresh()
            else:
                break

    
    def like_pics_feed(self, n_pics):

        while n_pics > 0:
            for i in range (4):
                print(i)
                pic = self.driver.find_elements_by_xpath('//span[@class="fr66n"]//button[@class="wpO6b "]')[i]
                if random.randint(1, 100) > 64:
                    self.driver.execute_script("arguments[0].scrollIntoView(false);", pic)
                    sleep(random.randint(10, 30)/10)
                    pic.click()
                    n_pics -= 1
                    if n_pics == 0:
                        break
                    sleep(random.randint(30, 45)/3)
                else:
                    continue
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    
    def like_pics_hash(self, n_likes, hash_pics):

        self.driver.find_element_by_xpath('//span[contains(text(), "Pesquisar")]').click()
        sleep(1)
        search_box = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
        hash_text = f'#{hash_pics}'
        self.person_typing(hash_text, search_box)
        sleep(1)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(Keys.ENTER)
        sleep(1)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(Keys.ENTER)
        sleep(3)

        hrefs = self.driver.find_elements_by_tag_name('a')
        pic_href = [elem.get_attribute('href') for elem in hrefs if '/p/' in elem.get_attribute('href')]
        while len(pic_href) < n_likes:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            hrefs = self.driver.find_elements_by_tag_name('a')
            pic_href = [elem.get_attribute('href') for elem in hrefs if '/p/' in elem.get_attribute('href')]

        
        for href in pic_href:

            self.driver.get(href)
            like = self.driver.find_element_by_xpath('//span[@class="fr66n"]//button[@class="wpO6b "]')
            self.driver.execute_script("arguments[0].scrollIntoView(false);", like)
            sleep(random.randint(40, 60)/10)
            try:
                self.driver.find_element_by_xpath('//span[@class="fr66n"]//button[@class="wpO6b "]').click()
            except:
                pass
            sleep(random.randint(10, 40)/10)
            n_likes -= 1
            if n_likes == 0:
                break
            else:
                continue



if __name__ == '__main__':

    header('INSTAGRAM BOT')
    menu(['Follow Profiles', 'Like Posts from Feed', 'Like Posts from a Hashtag', 'Comment on a Post'])
    
    while True:
        try:
            choice = int(input('What do you want to do? '))
        except:
            print('ENTER A VALID NUMBER!')
        else:
            break

    if choice == 1:

        n_profiles = int(input('Number of profiles to follow: '))

        igbot = InstagramBot(ig_username, ig_password)
        sleep(1)

        igbot.follow_profiles(n_profiles)
        sleep(3)

        igbot.driver.quit()

    if choice == 2:

        n_pics = int(input('Number of pictures to like on feed: '))

        igbot = InstagramBot(ig_username, ig_password)
        sleep(1)

        igbot.like_pics_feed(n_pics)
        sleep(3)

        igbot.driver.quit()

    if choice == 3:

        n_likes = int(input('Number of pictures to like: '))
        hash_pics = str(input('Hashtag to look for: '))

        igbot = InstagramBot(ig_username, ig_password)
        sleep(1)

        igbot.like_pics_hash(n_likes, hash_pics)
        sleep(3)

        igbot.driver.quit()

    if choice == 4:

        users = ['@_nataliaaguiar', '@sunmoonphases']
        post_url = str(input("Paste the posts' url: "))
        n_users = int(input('How many users do you have to tag? '))
        
        igbot = InstagramBot(ig_username, ig_password)
        sleep(2)

        igbot.comment(users, post_url, n_users)
        sleep(3)

        igbot.driver.quit()