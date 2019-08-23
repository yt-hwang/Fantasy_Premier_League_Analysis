# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:43:32 2019

@author: Yun Hwang
"""
'''
Constraints in picking my starting XI

1) XI must cost less or equal to £100
2) Can’t pick the same player more than once
3) Only 1 GK allowed
4) 3 to 5 DEF allowed
5) 3 to 5 MID allowed
6) 1 to 3 STR allowed

'''
import pandas as pd
!pip install xlrd

player_path = 'F:\\OneDrive - Georgia State University\\Data Science\\Personal_Project\\FPL_Analysis\\data\\players.xlsx'
fixture_path = 'F:\\OneDrive - Georgia State University\\Data Science\\Personal_Project\\FPL_Analysis\\data\\fixtures.xlsx'
player_error = 'F:\\OneDrive - Georgia State University\\Data Science\\Personal_Project\\FPL_Analysis\\data\\error.txt'
bootstrap_path = 'F:\\OneDrive - Georgia State University\\Data Science\\Personal_Project\\FPL_Analysis\\data\\bootstrap.xlsx'

players_weekly = pd.read_excel(player_path)
fixture_path = pd.read_excel(fixture_path)
bootstrap = pd.read_excel(bootstrap_path)

