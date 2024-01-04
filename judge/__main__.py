import sys
from judge import judge

if len(sys.argv) != 3:
    print('provide two image names as command-line arguemnents')
    exit()

judge.play(sys.argv[1], sys.argv[2])
