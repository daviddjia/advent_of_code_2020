#!/bin/env/python

import re

f = open('day04_input.txt', 'r')

lines = [line.strip() for line in f.readlines()]

expected_creds = set([
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
])

passports = []
passport = ''
for line in lines:
    if line == '':
        passports.append(passport.strip())
        passport = ''
    else:
        passport += ' ' + line
passports.append(passport.strip())

valid_count = 0
for passport in passports:
    creds = passport.split(' ')
    id_set = set()
    for cred in creds:
        [_id, value] = cred.split(':')
        id_set.add(_id)
    if expected_creds.issubset(id_set):
        valid_count += 1
print(valid_count)

valid_count = 0
for passport in passports:
    creds = passport.split(' ')
    id_set = set()
    for cred in creds:
        [_id, val] = cred.split(':')
        valid_cred = False
        if _id == 'byr':
            valid_cred = bool(re.match('^\d\d\d\d$', val)) and int(val) >= 1920 and int(val) <= 2002
        elif _id == 'iyr':
            valid_cred = bool(re.match('^\d\d\d\d$', val)) and int(val) >= 2010 and int(val) <= 2020
        elif _id == 'eyr':
            valid_cred = bool(re.match('^\d\d\d\d$', val)) and int(val) >= 2020 and int(val) <= 2030
        elif _id == 'hgt':
            valid_cred = (bool(re.match('\d+cm$', val)) and int(val[0:-2]) >= 150 and int(val[0:-2]) <= 193) or (bool(re.match('\d+in$', val)) and int(val[0:-2]) >= 59 and int(val[0:-2]) <= 76)
        elif _id == 'hcl':
            valid_cred = bool(re.match('^#[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]$', val))
        elif _id == 'ecl':
            valid_cred = (val in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'))
        elif _id == 'pid':
            valid_cred = bool(re.match('^\d\d\d\d\d\d\d\d\d$', val))
        if valid_cred == True:
            id_set.add(_id)
    if expected_creds.issubset(id_set):
        valid_count += 1
print(valid_count)
