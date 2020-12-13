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
