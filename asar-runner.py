import pprint
import sys

from asar import Asar

def main():
    usage = """
    asar-runner.py action args
        extract app.asar ./output-dir
        extract app.asar file-to-extract output-file
        list app.asar
    """

    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print(usage)
        return

    if sys.argv[1] == "extract" and len(sys.argv) == 4:
        Asar(sys.argv[2]).extractFiles(sys.argv[3])
    elif sys.argv[1] == "extract" and len(sys.argv) == 5:
        Asar(sys.argv[2]).extractFile(sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "list" and len(sys.argv) == 3:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(Asar(sys.argv[2]).listFiles())
    else:
        print(usage)


if __name__ == "__main__":
    main()
