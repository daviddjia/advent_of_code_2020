#!/bin/env/perl

for my $i (2..25) {
    my $day = sprintf("%02d", $i);
    `cp day01.py day$day.py`;
    `sed -i.bak 's/day01/day$day/g' day$day.py`;
    `rm day$day.py.bak`;
}
