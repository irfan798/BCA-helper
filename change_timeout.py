#!/usr/bin/env python

import sys
from bca_header import BCAObject

def imageBCAUpdate(image, timeout=3000):
	''' Update bootloader configuration area '''
	# Load BCA
	bca = BCAObject()
	bca.fromBytes(image)

	if not bca.isValid():
		print('Warning: Tag is not set!')
		print('Auto setting tag and header for you at the offset', hex(bca.BCA_OFFSET))
		bca.tag = bca.BCA_KEY

    # Timeout in milliseconds for peripheral detection before jumping to application code
	# Update timeout of image 0 means no timeout
	bca.peripheralDetectionTimeoutMs = timeout

	return bca.toBytesFile(image)


if __name__ == "__main__":
	# Collect arguments
    if len(sys.argv) != 4:
        print('usage: change_timeout.py <binary_image> <result_image> <timeout_ms>')
        sys.exit(2)

    filename = sys.argv[1]
    resultFilename = sys.argv[2]
    timeout = int(sys.argv[3])

    # Read Binary Image
    with open(filename, 'rb') as bfile:
        image = bfile.read()

    # Change timeout in milliseconds
    image_result = imageBCAUpdate(image, timeout)

    # Write back the resulted image
    with open(resultFilename, 'wb') as rfile:
        rfile.write(image_result)

