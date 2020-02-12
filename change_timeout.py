#!/usr/bin/env python

import sys
from bca_header import BCAObject

if __name__ == "__main__":
	# Collect arguments
    if len(sys.argv) != 4:
        print('usage: change_timeout.py <binary_image> <result_image> <timeout_ms>')
        sys.exit(2)

    filename = sys.argv[1]
    resultFilename = sys.argv[2]
    timeout = int(sys.argv[3])

    # Load image from filesystem
    bca = BCAObject()
    # Set tag if it is not set already
    bca.fromFile(filename, autoset_tag=True)

    # Change timeout in milliseconds
    bca.peripheralDetectionTimeoutMs = timeout

    # Write back the resulted image
    bca.saveToFile(resultFilename)

