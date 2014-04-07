import os 
import sys


def main(command):
    pid = os.fork()
    if 0 != pid:
        sys.exit()
    sys.stdin.close()
    sys.stdout.close()
    sys.stderr.close()
    os.setsid()
    

    pid = os.fork()
    
    if 0 != pid:
        sys.exit()
    os.system(command)
    sys.exit()
   

if __name__ == "__main__":

    main(sys.argv[1])
