from selenium import webdriver
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class reviewscrapping:
    def __init__(self,hotel_name):
        self.hotel_name = hotel_name
        self.chrome_path = "C:\Program Files\chromedriver.exe"
        self.driver = webdriver.Chrome(self.chrome_path)
        self.final_review_list = []
        
    def take_review(self):
        wait = ui.WebDriverWait(self.driver,5)
        element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "review_list")))
        review_list = self.driver.find_element_by_class_name('review_list')
        elementList = review_list.find_elements_by_tag_name("li")
        print(len(elementList))
        for i in range(len(elementList)):
            review_div = elementList[i].find_elements_by_class_name('c-review__body')
            for j in range(len(review_div)):
                print(review_div[j].text)
                self.final_review_list.append(review_div[j].text)
        
    def scrapping(self):
        self.driver.get("https://www.booking.com")
        search_field = self.driver.find_element_by_id("ss")
        search_field.clear()
        search_field.send_keys(self.hotel_name)
        self.driver.find_element_by_xpath("""//*[@id="frm"]/div[1]/div[4]/div[2]/button""").click()
        wait = ui.WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.ID, "search_results_table")))
        self.driver.find_element_by_xpath("""//*[@id="search_results_table"]/div/div/div/div/div[6]/div[3]/div[1]/div[2]/div/div/div/div[1]/div/div[1]/div/h3/a""").click()
        #self.driver.find_element_by_xpath("""//*[@id="hotellist_inner"]/div[2]/div[2]/div[1]/div[1]/div[1]/h3/a""").click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element_by_xpath("""//*[@id="show_reviews_tab"]""").click()
        
        # var = 0
        try:
            while True:
                self.take_review()
                self.driver.find_element_by_xpath("""//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[3]/a""").click()
                wait = ui.WebDriverWait(self.driver,10)
                wait.until(EC.visibility_of_element_located((By.XPATH, """//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[3]/a""")))
                element = wait.until(EC.visibility_of_element_located((By.XPATH, """//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[3]/a""")))
                # number = self.driver.find_elements_by_xpath("""//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[2]/div/div[1]""").size()
                # print("The number is :" +number)
        except TimeoutException:
            print("took too much time")
        except Exception as e:
            print('An exception occurred: {}'.format(e))
        except:
            print("close")
            self.driver.close()
        return self.final_review_list
