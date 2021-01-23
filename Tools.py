from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import json
import sys


@dataclass
class Tools:
    browser: webdriver
    url = 'https://reseau-ges.percipio.com'

    def connection(self, usr: str, pwd: str)-> bool:
        # On dit au navigateur d'aller sur l'url suivant
        self.browser.get('https://reseau-ges.percipio.com/login.html?state=%2F#/')

        sleep(2)

        # type text
        text_area = self.browser.find_element_by_id('loginName')
        text_area.send_keys(usr)

        # click submit button
        next_btn = self.browser.find_element_by_xpath("//button[@class='Button---root---2BQqW Button---primary---1O3lq "
                                                      "Button---small---3PMLN Button---center---13Oaw']")
        next_btn.click()

        sleep(1)

        # type text
        text_area = self.browser.find_element_by_id('password')
        text_area.send_keys(pwd)

        # click submit button
        submit_button = self.browser.find_element_by_xpath("//button[@class='Button---root---2BQqW "
                                                           "Button---primary---1O3lq Button---small---3PMLN "
                                                           "Button---center---13Oaw']")
        submit_button.click()

        sleep(5)

        return True

    def check_exists_by_xpath(self, xpath)-> bool:
        try:
            self.browser.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def go_to_assignement(self)-> bool:
        self.browser.get('https://reseau-ges.percipio.com/assignments')

        return True

    def get_cours(self, course_id: str)->None:
        self.browser.get(self.url + '/courses/' + course_id)

    def get_videos(self, video_id: str)->None:
        self.browser.get(self.url + '/videos/' + video_id)

    def launch_video(self)->None:
        # Lancement de la vidéo
        try:
            WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'playbackFocus')))
        except TimeoutException:
            sys.exit("Loading took too much time!")

        play = self.browser.find_element_by_id('playbackFocus')

        play.click()

        sleep(1)

        # Gotta go fast
        self.browser.find_element_by_id('video-player-settings-button').click()

        sleep(0.5)

        self.browser.find_element_by_id('speed').click()

        sleep(0.5)

        speed_2 = self.browser.find_element_by_xpath("//span[@id='current_value_prefix'][text()='2']")

        speed_2.click()

    def get_completion_status(self)->bool:
        div_completion_all = self.browser.find_element_by_xpath("//div[@class='ProgressBar---trail---3y2hW']")

        div_completion_status = self.browser.find_element_by_xpath("//div[@class='ProgressBar---stroke---1w8-k']")

        total_width = div_completion_all.value_of_css_property('width')

        actual_width = div_completion_status.value_of_css_property('width')

        return actual_width == total_width

    def check_for_test(self)->str:
        link_to_test = ''

        if self.check_exists_by_xpath("//a[@class='Button---root---2BQqW Button---primary---1O3lq Button---"
                                      "medium---1CC5_ Button---center---13Oaw']"):
            test_btn = self.browser.find_element_by_xpath("//a[@class='Button---root---2BQqW Button---primary---"
                                                          "1O3lq Button---medium---1CC5_ Button---center---13Oaw']")

            return test_btn.get_attribute('href')

        return link_to_test

    def passing_test(self)->bool:
        print("Début du Test")
        sleep(2)

        if self.check_exists_by_xpath("//a[@id='assessment-continue']"):
            btn_launch = self.browser.find_element_by_xpath("//a[@id='assessment-continue']")
        else:
            btn_launch = self.browser.find_element_by_xpath("//button[@class='Button---root---2BQqW Button---primary--"
                                                            "-1O3lq Button---small---3PMLN Button---center---13Oaw']")
        btn_launch.click()

        sleep(2)

        course_title = self.browser.find_element_by_xpath("//h1[@class='PageHeading---title---13psX']").text

        question = self.browser.find_element_by_xpath("//div[@class='QuestionMessages---stem---2uUKi']").text

        instruction = self.browser.find_element_by_xpath("//div[@class='MessageBar---instruction---3-J99']").text

        advancement = self.browser.find_element_by_xpath("//p[@class='PageHeading---subtitle---QX7Ls']").text

        print("Titre du cours")
        print(course_title)

        print("Etape")
        print(advancement)

        print("Question")
        print(question)

        print("Instruction")
        print(instruction)

        with open("test_answer.json", "r") as jsonFile:
            test_answer = json.load(jsonFile)

        # Si le cours n'est pas connu dans le fichier de réponse
        # On ajoute le titre du cours à notre fichier de réponse
        if course_title not in test_answer:
            test_answer[course_title] = {}

        # Si la question n'est pas connu dans le cours
        # On l'ajoute au cours
        if question not in test_answer[course_title]:
            test_answer[course_title][question] = None

        answer_input_id = test_answer[course_title][question]

        # Si la réponse est pas encore connu
        if answer_input_id is None:
            # On prend le premier input
            first_answer = self.browser.find_elements_by_xpath("//input[@class='RadioButton---input---3iHUk']")[0]

            first_answer.click()

            sleep(2)
            # On sauvegarde la réponse
            span_solution = self.browser.find_element_by_xpath("//span[@class='MessageBar---message---1BykM']").text

            if span_solution == "Résultat : Correct. Bravo ! ":
                test_answer[course_title][question] = first_answer.get_attribute('id')

        with open("test_answer.json", "w") as jsonFile:
            json.dump(test_answer, jsonFile)

        return True
