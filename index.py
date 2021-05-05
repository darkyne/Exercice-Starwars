"""
This files is my solution to the https://gitlab.qualif.io/interview/swapi-dev exercise for the qualifio interview.
Author: Gregory Creupelandt
"""

import sys
import requests

####################################################################
########################## BODY ####################################
####################################################################
def homework():
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
        print("It looks like some planets there do not exist...? Maybe they got destroyed !")
        return

    # Summ the diameters
    good_diameters, diameters_summ = summ(planets_diameters)
    if not good_diameters:
        print("One planet diameter is not an integer value... Strange planet !")
        return

    # Print the final result
    print(diameters_summ)


####################################################################
########################## HELPERS #################################
####################################################################

def check_input():
    if len(sys.argv) != 2:
        return False, 0
    try:
        film_index = int(sys.argv[1])
    except Exception:
        return False, 0
    return True, film_index


def get_planets(film_index):
    r = requests.get('https://swapi.dev/api/films/'+str(film_index)+'/')
    if r.status_code != 200:
        return False, "error"
    content_dict = r.json()
    planets_urls = content_dict["planets"]
    return True, planets_urls


def get_diameters(film_planets_urls):
    diameters = []
    for planet_url in film_planets_urls:
        planet_exists, planet_diameter = get_planet_diameter(planet_url)
        if not planet_exists:
            return False, "error"
        diameters.append(planet_diameter)
    return True, diameters


def get_planet_diameter(planet_url):
    r = requests.get(planet_url)
    if r.status_code != 200:
        return False, "error"
    content_dict = r.json()
    diameter = content_dict["diameter"]
    return True, diameter


def summ(array):
    total=0
    try:
        for diameter in array:
            total += int(diameter)
        return True, total
    except Exception:
        return False, 0


####################################################################
########################## Launch ##################################
####################################################################
if __name__ == "__main__":
    homework()
