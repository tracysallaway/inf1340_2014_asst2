#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import re
import datetime
import json


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """
    with open(input_file, "r") as file_reader:
        file_contents = file_reader.read()
        example_entries = json.loads(file_contents)

    with open(countries_file, "r") as file_reader:
        file_contents = file_reader.read()
        countries = json.loads(file_contents)

    with open(watchlist_file, "r") as file_reader:
        file_contents = file_reader.read()
        watchlist = json.loads(file_contents)
    temp=[]
    for i in range(len(example_entries)):
        #validity=True
        #validity=validity and not example_entries[i]["first_name"]==None
        #validity = validity and not example_entries[i]["last_name"] == None
        #validity = validity and valid_date_format(example_entries[i]["birth_date"])
        #validity = validity and valid_passport_format(example_entries[i]["passport"])
        #validity = validity and not example_entries[i]["home"] == None
        choice='Reject'
        if not example_entries[i]["first_name"] == None:
            if not example_entries[i]["last_name"] == None:
                if valid_date_format(example_entries[i]["birth_date"]):
                    if valid_passport_format(example_entries[i]["passport"]):
                        if not example_entries[i]["home"] == None :
                            if not example_entries[i]["home"]["city"] == None:
                                if not example_entries[i]["home"]["region"] == None:
                                    if not example_entries[i]["home"]["country"] == None:
                                        if not example_entries[i]["from"] == None :
                                            if not example_entries[i]["from"]["city"] == None:
                                                if not example_entries[i]["from"]["region"] == None:
                                                    if not example_entries[i]["from"]["country"] == None:
                                                        if not example_entries[i]["entry_reason"] == None:

                                                            if example_entries[i]["home"]["country"] == "KAN":
                                                                if example_entries[i]["entry_reason"] == "returning":
                                                                    choice = "Accept"
                                                            else:
                                                                if example_entries[i]["entry_reason"] == "visit":
                                                                    if countries[example_entries[i]["home"]["country"]]["visitor_visa_required"] == 1:
                                                                        if "visa" in example_entries[i].keys():
                                                                            if True: # validate date example_entries[i]["visa"]["date"]
                                                                                choice = "Accept"
                                                                elif example_entries[i]["entry_reason"] == "transit":
                                                                    if countries[example_entries[i]["home"]["country"]]["transit_visa_required"] == 1:
                                                                        if "visa" in example_entries[i].keys():
                                                                            if True: # validate date example_entries[i]["visa"]["date"]
                                                                                choice = "Accept"
                                                                if choice == "Accept":
                                                                    for j in range(len(watchlist)):
                                                                        not_present=True
                                                                        if True: # not (not_present and ((first_name1==first_name2 and last_name1==last_name4) or passp1==passp2)):
                                                                            choice = "Secondary"

                                                                if "via" in example_entries[i].keys():
                                                                    if not countries[example_entries[i]["via"]["country"]]["medical_advisory"] == None:
                                                                        choice = "Quarantine"
                                                                if not countries[example_entries[i]["home"]["country"]]["medical_advisory"] == None:
                                                                    choice = "Quarantine"
        temp.append(choice)
    return(temp)

    #return ["Reject"]


def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number):
        return True
    else:
        return False


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


print(decide("example_entries.json", "watchlist.json", "countries.json"))



