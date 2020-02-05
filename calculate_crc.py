#!/usr/bin/env python
# This is an example to calculate crc and write it back to image BCA
from bca_header import BCAObject

# Bootloader uses Crc32Mpeg2 implementation
from crccheck.crc import Crc32Mpeg2 
import sys

# Start of flash image excluding bootloader
flash_start_offset = 0x0000
# Crc checking offset from starting of the flash image
CRC_START_OFFSET =  0x400

def main():
    filename = sys.argv[1]
    resultFilename = sys.argv[2]

    # Read Binary Image
    with open(filename, 'rb') as bfile:
        image = bfile.read()

    # Calculate CRC
    image_crc = crcUpdate(image, flash_start_offset, CRC_START_OFFSET)

    # Write back the resulted image
    with open(resultFilename, 'wb') as rfile:
        rfile.write(image_crc)

def crcUpdate(image, flash_start_offset, crc_start_offset, programSize=None):
	''' Updates CRC area of Bootloader Config Area(BLA) on image '''
	# Get size of image
	if programSize is None:
		programSize = len(image)

	bca = BCAObject()
	bca.fromBytes(image)

	if not bca.isValid():
		print('Warning: Tag is not set!')
		print('Auto setting tag and header for you at the offset', hex(bca.BCA_OFFSET))
		bca.tag = bca.BCA_KEY

	## Configure CRC areas
	bca.crcStartAddress = flash_start_offset + crc_start_offset
	bca.crcByteCount = programSize-crc_start_offset
	bca.crcExpectedValue = 0xFFFFFFFF # Set default value

	## Write these back to image
	program = bca.toBytesFile(image)

	## Start CRC creation on cropped area
	encript_area = image[crc_start_offset:crc_start_offset+bca.crcByteCount]
	bca.crcExpectedValue = Crc32Mpeg2.calc(encript_area)

	#Update image with crc key
	return bca.toBytesFile(program)


if __name__ == "__main__":
	# Collect arguments
	if len(sys.argv) != 3:
		print('usage: calculate_crc.py <binary_image> <result_image>')
		sys.exit(2)

	main()
