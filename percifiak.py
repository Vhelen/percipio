from selenium import webdriver
from Tools import Tools
from time import sleep
import os
import sys
import getopt
import json


# Lancement d'un webdriver
def init_webdriver(debug, firefox_location)-> webdriver:
    if not debug:
        os.environ['MOZ_HEADLESS'] = '1'

    # Les options du navigateur, ici Firefox
    # l'emplacement du navigateur
    options = webdriver.FirefoxOptions()
    options.binary_location = firefox_location

    # Lancement du browser
    # Options : -> emplacement exécutable geckodriver
    #           -> emplacement logs geckodriver
    #           -> options du navigateur
    browser = webdriver.Firefox(
        executable_path='selenium/geckodriver.exe', service_log_path='selenium/geckodriver.log', options=options)

    # browser.maximize_window()

    return browser


def usage():
    print("Pour que l'outil se lance correctement, il faut définir au premier lancement :")
    print("     - Le nom d'utilisateur (exemple : jean.dupont@gmail.com)")
    print("     - Le mot de passe associe (exemple : tonmeilleurmotdepasse)")
    print("     - La location de l'exe de firefox (exemple : C:/Program Files/Mozilla Firefox/firefox)")
    print("Ces informations sont stockees dans le fichier conf.json")
    print("Vous n'aurez pas à les remplir à chaque utilisation\n")

    print("-h --help Affiche l'aide")
    print("-u --username Met à jour le nom d'utilisateur")
    print("-p --password Met à jour le mot de passe de l'utilisateur")
    print("-b --browser Met à jour la location de l'exe de firefox")
    print("-d --debug Affiche la fenetre du navigateur")

    sys.exit()


def main():
    # Vérification des arguments passés dans la ligne de commande
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:p:b:hd", ["user=", "password=", "browser=", "debug", "help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)
        usage()
        sys.exit()

    # Argument optionnel
    debug = False

    # Argument obligatoire
    usr = ''
    pwd = ''
    browser_location = ''

    for o, a in opts:
        if o in ("-d", "--debug"):
            debug = True

        elif o in ("-h", "--help"):
            usage()

        elif o in ("-u", "--user"):
            usr = a

        elif o in ("-p", "--password"):
            pwd = a

        elif o in ("-b", "--browser"):
            browser_location = a

        else:
            assert False, "unhandled option"

    with open("conf.json", "r") as jsonFile:
        conf = json.load(jsonFile)

    if usr != '':
        conf["username"] = usr

    if pwd != '':
        conf["password"] = pwd

    if browser_location != '':
        conf["browser"]["location"] = browser_location

    with open("conf.json", "w") as jsonFile:
        json.dump(conf, jsonFile)

    if conf["browser"]["location"] == '' or conf["password"] == '' or conf["username"] == '':
        print("Il manque un element a configurer : nom d'utilisateur, mot de passe ou la location du navigateur")
        sys.exit()

    browser = init_webdriver(debug, conf["browser"]["location"])

    tools = Tools(browser)

    tools.connection(conf["username"], conf["password"])

    tools.go_to_assignement()

    sleep(2)

    courses, videos = tools.get_all_cours()

    sleep(1)

    for video in videos:
        print("Début video : " + video)
        tools.get_video(video)

        tools.launch_video()

        while browser.find_element_by_xpath("//div[@class='jw-icon jw-icon-inline "
                                            "jw-button-color jw-reset jw-icon-playback']").get_attribute('aria-label') \
                != 'Play':
            sleep(10)

        print("Fin video : " + video)

    for course in courses:

        print("Début du cours : " + course)

        tools.get_cours(course)

        sleep(1)

        tools.launch_video()

        sleep(1)

        # Tant que le cours n'est pas fini
        while tools.get_completion_status() is False:
            sleep(5)

        print("Fin du cours : " + course)

        test_url = tools.check_for_test()

        if test_url != '':
            browser.get(test_url)
            tools.passing_test()

    print('Tout les cours sont fini !')

    # Fin du programme
    browser.quit()


if __name__ == "__main__":
    main()














