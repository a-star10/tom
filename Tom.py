# -*- coding: utf-8 -*-

import subprocess
import os
import time
import logging
import requests  # Assurez-vous que ce module est installé
import threading


# Configuration de la journalisation
logging.basicConfig(filename='tor_change_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command):
    """
    Exécute une commande système avec gestion des erreurs et journalisation.
    """
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        logging.info(f"Commande exécutée avec succès: {command}")
        print(result)  # Affiche le résultat de la commande pour une meilleure visibilité
        return result
    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur lors de l'exécution de la commande {command}: {e.output}")
        print(f"Erreur lors de l'exécution de la commande. Vérifiez les logs pour plus de détails.")
        return None

def install_package(package_name):
    """
    Vérifie et installe le paquet spécifié si nécessaire.
    """
    print(f"Vérification de l'installation de {package_name}...")
    if run_command(f'dpkg -s {package_name}') is None:
        print(f"{package_name} n'est pas installé. Installation en cours...")
        run_command(f'sudo apt update && sudo apt install {package_name} -y')
        print(f"{package_name} a été installé avec succès.")

def check_and_install_dependencies():
    """
    Vérifie et installe les dépendances requises : pip3, requests, tor.
    """
    install_package('python3-pip')
    if run_command('pip3 list | grep requests') is None:
        run_command('pip3 install requests')
    install_package('tor')

def start_tor_service():
    """
    Démarre le service Tor.
    """
    display_banner("ANONYMOUS TOM")
    print("\033[1;40;31m [+] V0.1 Created by Léon Meizou, Cybersecurity Evangelist [+] \n")
    
    
    print(f"[+] Démarrage de Tor")
    run_command('sudo service tor start')
    

def change_ip():
    """
    Change l'IP en rechargeant le service Tor et affiche la nouvelle IP.
    """
    run_command('sudo service tor reload')
    new_ip = requests.get("http://httpbin.org/ip", proxies=dict(http='socks5://127.0.0.1:9050', https='socks5://127.0.0.1:9050')).text
    print(f"[+] Votre IP a été changée en : {new_ip}")

def change_ip_continuously(delay, count):
    if delay == 0:
        delay = 1  # Assurez un minimum de délai pour éviter la surcharge
    if count == 0:
        try:
            while True:
                change_ip()
                time.sleep(delay)
        except KeyboardInterrupt:
            print("\nArrêt du changement automatique d'IP.")
    else:
        for _ in range(count):
            change_ip()
            time.sleep(delay)


    
def display_banner(text):
    """
    Affiche la bannière du projet avec ASCII Art.
    """
    os.system(f'echo "{text}" | figlet | lolcat')

def main():
    display_banner("TOM")
    
    check_and_install_dependencies()
    os.system("clear")
    start_tor_service()

    print("\033[93m[+] Enter the delay between each IP change (in seconds): \033[0m", end="")
    delay = int(input())
    print("\033[93m[+] How many times do you want to change your IP? (0 for infinite): \033[0m", end="")
    count = int(input())
    
    
    # Création et démarrage d'un thread pour le processus de changement d'IP
    thread = threading.Thread(target=change_ip_continuously, args=(delay, count))
    thread.start()
    
    

    print("Le changement d'IP s'exécute en arrière-plan. Vous pouvez continuer à travailler.")

if __name__ == "__main__":
    main()
