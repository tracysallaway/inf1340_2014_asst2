#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Jodie Church and Tracy Sallaway'
__email__ = "jodie.church@mail.utoronto.ca, tracy.armstrong@mail.utoronto.ca"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import pytest
from papers import decide


def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine", "Quarantine"]


def test_files():
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")


def test_letter_case():
    assert decide("test_letter_case.json", "watchlist.json", "countries.json") == ["Accept", "Secondary"]


def test_visa_format():
    assert decide("test_visa_format.json", "watchlist.json", "countries.json") == ["Accept", "Reject"]

