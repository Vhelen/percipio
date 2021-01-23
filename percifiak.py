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

    sleep(1)

    # TODO Récupération des cours à faire
    courses = ['f44f856e-1bcc-11e7-b15b-0242c0a80b07', 'f44fac7d-1bcc-11e7-b15b-0242c0a80b07',
               'f44ffa91-1bcc-11e7-b15b-0242c0a80b07', 'f44ffa9b-1bcc-11e7-b15b-0242c0a80b07',
               'f45021ad-1bcc-11e7-b15b-0242c0a80b07', 'f45096d8-1bcc-11e7-b15b-0242c0a80b07',
               'f450e4f9-1bcc-11e7-b15b-0242c0a80b07', 'fe198c4e-e4cb-11e6-8282-0242c0a80a04',
               'fe19da6a-e4cb-11e6-8282-0242c0a80a04', 'fe1a0171-e4cb-11e6-8282-0242c0a80a04',
               'fe1a0183-e4cb-11e6-8282-0242c0a80a04']

    videos = ['67c3943a-7d5d-48a1-af4b-bf4d36cfa2e3', '42a31e08-ff7d-11e6-8638-0242c0a80b06']

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

        # test_url = tools.check_for_test()
        #
        # if test_url != '':
        #     browser.get(test_url)
        #
        #     tools.passing_test()

    print('Tout les cours sont fini !')

    # Fin du programme
    browser.quit()


if __name__ == "__main__":
    main()














