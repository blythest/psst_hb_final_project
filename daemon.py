import os 
import sys

def main(command):

    pid = os.fork()

    if 0 != pid:
        return
    sys.stdin.close()
    sys.stdout.close()
    sys.stderr.close()

    # Create a new session.
    os.setsid()


    pid = os.fork()

    if 0 != pid:
        return
    os.system(command)
    sys.exit()

if __name__ == "__main__":

    main(sys.argv[1])