#!/usr/bin/python3

import os
import subprocess
import sys
import json

project_path = os.path.dirname(os.path.realpath(__file__))

def run_extraction(image_path):
    bashCommand = project_path + "/scripts/extract " + image_path
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf8')

    # Remove blank lines
    lines = "\n".join([s for s in output.split("\n") if s]).split("\n")
    return {
        "question": " ".join([s for s in lines[:-3] if s]),
        "a_1": lines[-3],
        "a_2": lines[-2],
        "a_3": lines[-1]
    }


def main():
    try:
        print(json.dumps(run_extraction(sys.argv[1]), indent=4))
    except:
        raise ValueError("Errore nell'estrazione OCR")


if __name__ == '__main__':
    main()
