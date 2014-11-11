#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Jodie Church and Tracy Sallaway'
__email__ = "jodie.church@mail.utoronto.ca, tracy.armstrong@mail.utoronto.ca"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import re
import datetime
import json


def decide(input_file, watchlist, countries):
    """
    Decides whether a traveller's entry into Kanadia should be accepted
    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """
    with open(input_file, "r") as file_reader:
        file_contents = file_reader.read()
        input_file = json.loads(file_contents)

    with open(countries, "r") as file_reader:
        file_contents = file_reader.read()
        countries = json.loads(file_contents)

    with open(watchlist, "r") as file_reader:
        file_contents = file_reader.read()
        watchlist = json.loads(file_contents)
    temp = []  # create empty list to store results
    for i in range(len(input_file)):  # loop through entries in input file
        choice = ""
        # assign Quarantine to travellers arriving from countries with a medical advisory - priority 1
        if not countries[input_file[i]["from"]["country"]]["medical_advisory"] == "":
            choice = "Quarantine"
        elif "via" in input_file[i].keys():
            if not countries[input_file[i]["via"]["country"]]["medical_advisory"] == "":
                choice = "Quarantine"
        # assign Reject to entries that do not have all required information - priority 2
        if input_file[i]["first_name"] is None:
                choice = "Reject"
        elif input_file[i]["last_name"] is None:
            choice = "Reject"
        elif not valid_date_format(input_file[i]["birth_date"]):
            choice = "Reject"
        elif not valid_passport_format(input_file[i]["passport"]):
            choice = "Reject"
        elif input_file[i]["home"] is None:
            choice = "Reject"
        elif input_file[i]["home"]["city"] is None:
            choice = "Reject"
        elif input_file[i]["home"]["region"] is None:
            choice = "Reject"
        elif input_file[i]["home"]["country"] is None:
            choice = "Reject"
        elif input_file[i]["from"] is None:
            choice = "Reject"
        elif input_file[i]["from"]["city"] is None:
            choice = "Reject"
        elif input_file[i]["from"]["region"] is None:
            choice = "Reject"
        elif input_file[i]["from"]["country"] is None:
            choice = "Reject"
        elif input_file[i]["entry_reason"] is None:
            choice = "Reject"
        # loop through watchlist entries and assign Secondary if not already Quarantine or Reject - priority 3
        for j in range(len(watchlist)):
            if choice != "Quarantine":
                if choice != "Reject":
                    if watchlist[j]["first_name"].upper() == input_file[i]["first_name"].upper():
                        if watchlist[j]["last_name"].upper() == input_file[i]["last_name"].upper():
                            choice = "Secondary"
                    elif watchlist[j]["passport"].upper() == input_file[i]["passport"].upper():
                        choice = "Secondary"
        # assign Accept to returning travellers who live in KAN as long as no other condition holds
        if input_file[i]["home"]["country"].upper() == "KAN":
            if input_file[i]["entry_reason"] == "returning":
                if choice != "Quarantine":
                    if choice != "Reject":
                        if choice != "Secondary":
                            choice = "Accept"
        else:  # assign Accept to visitors and those in transit as long as no other condition holds
            if input_file[i]["entry_reason"] == "visit":
                if choice != "Quarantine":
                    if choice != "Reject":
                        if countries[input_file[i]["home"]["country"]]["visitor_visa_required"] == "1":
                            if "visa" in input_file[i]:
                                # check visa code for valid format
                                if not valid_visa_format(input_file[i]["visa"]["code"]):
                                    choice = "Reject"
                                else:  # if visa format passes, check that the visa was issued within the last two years
                                    today = datetime.date.today()
                                    today_string = today.strftime("%Y-%m-%d")  # convert time to string
                                    visa_date = input_file[i]["visa"]["date"]
                                    # parse times to ensure strings are in matching formats
                                    today1 = datetime.datetime.strptime(today_string, "%Y-%m-%d").date()
                                    visa_date1 = datetime.datetime.strptime(visa_date, "%Y-%m-%d").date()
                                    # subtract parsed times to check validity - if less than two years old, accept
                                    difference = (today1 - visa_date1).days
                                    if difference < 730:
                                        choice = "Accept"
                                    else:
                                        choice = "Reject"
                            else:  # if visitor visa is required but not provided
                                choice = "Reject"
                        else:  # if visitor visa not required
                            if choice != "Secondary":
                                choice = "Accept"
            elif input_file[i]["entry_reason"] == "transit":
                if choice != "Quarantine":
                    if choice != "Reject":
                        if countries[input_file[i]["home"]["country"]]["transit_visa_required"] == "1":
                            if "visa" in input_file[i]:
                                if not valid_visa_format(input_file[i]["visa"]["code"]):
                                    choice = "Reject"
                                else:
                                    today = datetime.date.today()
                                    today_string = today.strftime("%Y-%m-%d")
                                    visa_date = input_file[i]["visa"]["date"]
                                    today1 = datetime.datetime.strptime(today_string, "%Y-%m-%d").date()
                                    visa_date1 = datetime.datetime.strptime(visa_date, "%Y-%m-%d").date()
                                    difference = (today1 - visa_date1).days
                                    if difference < 730:
                                        choice = "Accept"
                                    else:
                                        choice = "Reject"
                            else:  # if transit visa required but not provided
                                choice = "Reject"
                        else:  # if transit visa not required
                            if choice != "Secondary":
                                choice = "Accept"
        temp.append(choice)  # populate list with results
    return temp


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('^.{5}-.{5}-.{5}-.{5}-.{5}$')

    if passport_format.match(passport_number):
        return True
    else:
        return False


def valid_visa_format(visa_number):
    """
    Checks whether a visa number is two sets of five alpha-number characters separated by dashes
    :param visa_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    visa_format = re.compile('^.{5}-.{5}$')

    if visa_format.match(visa_number):
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