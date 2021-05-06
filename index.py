"""
This files is my solution to the https://gitlab.qualif.io/interview/swapi-dev exercise for the qualifio interview.
Author: Gregory Creupelandt
"""

import sys
import requests
import threading

# Global variable for threads
DIAMETERS = []

####################################################################
########################## BODY ####################################
####################################################################
def main():
    # Get the film index
    good_args, film_index = check_input()
    if not good_args:
        print("Please use following command line: \"python3 index.py film_index\" where film_index is an integer")
        return

    # Get the film planets
    film_exists, film_planets_urls = get_planets(film_index)
    if not film_exists:
        print("It sounds like that film does not exist ! Verify the film index you used.")
        return

    # Get the planets diameters
    planets_exist, planets_diameters = get_diameters(film_planets_urls)
    if not planets_exist:
        print("It looks like some planets there do not answer..? Maybe they got destroyed !")
        return

    # Summ the diameters
    good_diameters, diameters_summ = summ(planets_diameters)
    if not good_diameters:
        print("One planet diameter is not a correct integer value... Strange planet !")
        return

    # Print the final result
    print(diameters_summ)


####################################################################
########################## HELPERS #################################
####################################################################

def check_input():
    """ Verify the inputs, the command line should be "python3 index.py film_index" where film_index is an integer
    First output is a boolean to tell if input is correctly formatted. Second output is the film_index integer"""
    if len(sys.argv) != 2:
        return False, 0
    try:
        film_index = int(sys.argv[1])
    except Exception:
        return False, 0
    return True, film_index


def get_planets(film_index):
    """ Based on the film index, it returns an array of planet_urls
    First output is a boolean to tell if the request to swapi was fine. Second output is the planet_urls"""
    r = requests.get('https://swapi.dev/api/films/'+str(film_index)+'/')
    if r.status_code != 200:
        return False, "error"
    content_dict = r.json()
    planets_urls = content_dict["planets"]
    return True, planets_urls


def get_diameters(film_planets_urls):
    """ Based on an array of planet_urls, it launches parallel requests then returns an array containing the planets diameters
    First output is a boolean to tell if an exception occured. Second output is the diameters array"""
    try:
        threads = []
        for planet_url in film_planets_urls:
            thread = threading.Thread(target=get_planet_diameter, args=(planet_url, ))
            thread.start()
            threads.append(thread)
        for th in threads:
            th.join()
        return True, DIAMETERS
    except Exception:
        return False, 0


def get_planet_diameter(planet_url):
    """ Based on a plantet url, adds the diameter of the planet to the diameters array"""
    try:
        global DIAMETERS
        r = requests.get(planet_url)
        if r.status_code != 200:
            return -1
        content_dict = r.json()
        diameter = content_dict["diameter"]
        terrains = content_dict["terrain"]
        surface_water = content_dict["surface_water"]
        if surface_water != "unknown" and float(surface_water) > 0 and "mountains" in terrains:
            DIAMETERS.append(diameter)
    except Exception:
        pass #This planet will not be taken in account for the final result


def summ(array):
    """ Basedon an array of strings representing diameters, convert them to integers and compute their summ """
    total = 0
    try:
        for diameter in array:
            diameter_int = int(diameter)
            if diameter_int < 0:
                return False, 0
            total += diameter_int
        return True, total
    except Exception:
        return False, 0


####################################################################
########################## Launch ##################################
####################################################################
if __name__ == "__main__":
    main()
