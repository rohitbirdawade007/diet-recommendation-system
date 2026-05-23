# -*- coding: utf-8 -*-
"""src/recommendation.py - Diet advice database."""

DIET_ADVICE = {}

def get_diet_advice(diet_label):
    return DIET_ADVICE.get(diet_label, {})

def get_all_diets():
    return DIET_ADVICE