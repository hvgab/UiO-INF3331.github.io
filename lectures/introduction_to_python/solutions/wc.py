#!/usr/bin/env python3
import sys

filename = sys.argv[1]

word_count = line_count = char_count = 0
with open(filename, 'r') as file:
    for line in file:
        words = line.split()

        if line.endswith('\n'):
            line_count += 1
        word_count += len(words)
        char_count += len(line)

print("%d %d %d %s" % (line_count, word_count, char_count, filename))
