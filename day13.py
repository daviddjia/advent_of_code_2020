#!/bin/env/python

f = open('day13_input.txt', 'r')

lines = [line.strip() for line in f.readlines()]
earliest_time, buses = int(lines[0]), lines[1].split(',')

running_buses = [int(bus) for bus in buses if bus!='x']
time, found = earliest_time, False
while not found:
    for bus in running_buses:
        if time % bus == 0:
            print(bus*(time-earliest_time))
            found = True
            break
    time += 1

# Found an interesting property of my input that I highly doubt is a
# coincidence. A lot of bus numbers were offset from another number BY its bus
# number. For instance, in my input, 19 is 19 spaces away from 823, 41 is 41
# spaces away from 443, 17 is 17 spaces away from 823, and so on. This makes it
# possible to increment by 823*19*17*29*37 and just brute force a solution. I'm
# not particularly happy with this solution because it requires observing a
# seemingly arbitrary pattern in the input file that's not discussed at all in
# the problem, but if it works, it works. The only other way to do this is to
# resort to Wolfram Alpha (or requires detailed knowledge of the Chinese
# Remainder Theorem)
bus_offsets = {
    int(bus): i
    for i, bus in enumerate(buses)
    if bus != 'x'
}
for bus in sorted(bus_offsets):
    for bus2 in bus_offsets:
        if bus == bus2 or bus not in bus_offsets:
            continue
        elif (bus_offsets[bus2]-bus_offsets[bus])%bus == 0:
            bus_offsets[bus2*bus] = bus_offsets[bus2]
            del bus_offsets[bus]
            del bus_offsets[bus2]
            break
max_bus = max(bus_offsets)
time = max_bus
while True:
    for bus in bus_offsets:
        if bus != max_bus:
            if (time+(bus_offsets[bus]-bus_offsets[max_bus])) % bus != 0:
                break
    else:
        print(time-bus_offsets[max_bus])
        break
    time += max_bus
