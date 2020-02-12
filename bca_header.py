#!/usr/bin/env python

# This is a helper object for editing Bootloader Configuration Area (BCA) for 
# MCU Bootloader for NXP microcontrollers previously named Kinetis Bootloader

import sys
import struct
# BCA CONFIG AREA
# typedef struct BootloaderConfigurationData
# {
#     uint32_t tag; //!< [00:03] Tag value used to validate the bootloader configuration data. Must be set to 'kcfg'.
#     uint32_t crcStartAddress;              //!< [04:07]
#     uint32_t crcByteCount;                 //!< [08:0b]
#     uint32_t crcExpectedValue;             //!< [0c:0f]
#     uint8_t enabledPeripherals;            //!< [10:10]
#     uint8_t i2cSlaveAddress;               //!< [11:11]
#     uint16_t peripheralDetectionTimeoutMs; //!< [12:13] Timeout in milliseconds for peripheral detection before jumping
#     //! to application code
#     uint16_t usbVid;                    //!< [14:15]
#     uint16_t usbPid;                    //!< [16:17]
#     uint32_t usbStringsPointer;         //!< [18:1b]
#     uint8_t clockFlags;                 //!< [1c:1c] High Speed and other clock options
#     uint8_t clockDivider;               //!< [1d:1d] One's complement of clock divider, zero divider is divide by 1
#     uint8_t bootFlags;                  //!< [1e:1e] One's complemnt of direct boot flag, 0xFE represents direct boot
#     uint8_t pad0;                       //!< [1f:1f] Reserved, set to 0xFF
#     uint32_t mmcauConfigPointer;        //!< [20:23] Holds a pointer value to the MMCAU configuration
#     uint32_t keyBlobPointer;            //!< [24:27] Holds a pointer value to the key blob array used to configure OTFAD
#     uint8_t qspiPort;                   //!< [28:28] qspi port: 0xFF-PORTE, 0xFE-PORTC
#     uint8_t canConfig1;                 //!< [29:29] ClkSel[1], PropSeg[3], SpeedIndex[4]
#     uint16_t canConfig2;                //!< [2a:2b] Pdiv[8], Pseg1[3], Pseg2[3],  rjw[2]
#     uint16_t canTxId;                   //!< [2c:2d] txId
#     uint16_t canRxId;                   //!< [2e:2f] rxId
#     uint32_t qspi_config_block_pointer; //!< [30:33] QSPI config block pointer.
# } bootloader_configuration_data_t;


class BCAObject:
    """Object to read Boot Configuration Area"""
    # Header style
    header_info = '<4I2B3HI4B2I2B3HI' #4*uint32 2*uint8 3*uint16 uint32 4*uint8 2*uint32 2*uint8 3*uint16 uint32

    tag                             = 0
    crcStartAddress                 = 0
    crcByteCount                    = 0
    crcExpectedValue                = 0
    enabledPeripherals              = 0
    i2cSlaveAddress                 = 0
    peripheralDetectionTimeoutMs    = 0
    usbVid                          = 0
    usbPid                          = 0
    usbStringsPointer               = 0
    clockFlags                      = 0
    clockDivider                    = 0
    bootFlags                       = 0
    pad0                            = 0
    mmcauConfigPointer              = 0
    keyBlobPointer                  = 0
    qspiPort                        = 0
    canConfig1                      = 0
    canConfig2                      = 0
    canTxId                         = 0
    canRxId                         = 0
    qspi_config_block_pointer       = 0

    BCA_KEY = 0x6766636b    # 'kfcg' as a uint32
    BCA_OFFSET = 0x3c0
    header_size = struct.calcsize(header_info)
    
    def __init__(self, bca_offset=0x3c0):
        ''''''
        self.BCA_OFFSET=bca_offset
        self.header_size = struct.calcsize(self.header_info)
        self.original_image = None

    def fromFile(self, path, autoset_tag=False):
        # Read Binary Image
        with open(path, 'rb') as bfile:
            image = bfile.read()
            self.fromBytes(image, autoset_tag)

    def saveToFile(self, path):
        # Write header back to original image
        image_result = self.toBytesFile(self.original_image)

        # Write resulted image to filesystem
        with open(path, 'wb') as rfile:
            rfile.write(image_result)
       
    
    def fromBytes(self, image, autoset_tag=False):
        """ Gets whole image as an input then crops and reads BCA according to BCA_offset"""
        self.original_image = image = bytearray(image)
        image_header = image[self.BCA_OFFSET:self.BCA_OFFSET+self.header_size]
        result = struct.unpack(self.header_info, image_header)

        (
        self.tag,
        self.crcStartAddress,
        self.crcByteCount,
        self.crcExpectedValue,
        self.enabledPeripherals,
        self.i2cSlaveAddress,
        self.peripheralDetectionTimeoutMs,
        self.usbVid,
        self.usbPid,
        self.usbStringsPointer,
        self.clockFlags,
        self.clockDivider,
        self.bootFlags,
        self.pad0,
        self.mmcauConfigPointer,
        self.keyBlobPointer,
        self.qspiPort,
        self.canConfig1,
        self.canConfig2,
        self.canTxId,
        self.canRxId,
        self.qspi_config_block_pointer,
        ) = result

        if not self.isValid():
            print('Warning: Tag is not set!')
            if autoset_tag:
                print('Auto setting tag and header for you at the offset', hex(self.BCA_OFFSET))
                self.tag = self.BCA_KEY

    
    def toBytes(self):
        """ Returns little endian bytes respresentation of BCA """
        return struct.pack(self.header_info,
            self.tag,
            self.crcStartAddress,
            self.crcByteCount,
            self.crcExpectedValue,
            self.enabledPeripherals,
            self.i2cSlaveAddress,
            self.peripheralDetectionTimeoutMs,
            self.usbVid,
            self.usbPid,
            self.usbStringsPointer,
            self.clockFlags,
            self.clockDivider,
            self.bootFlags,
            self.pad0,
            self.mmcauConfigPointer,
            self.keyBlobPointer,
            self.qspiPort,
            self.canConfig1,
            self.canConfig2,
            self.canTxId,
            self.canRxId,
            self.qspi_config_block_pointer,    
        ) 
    
    def toBytesFile(self, image=None):
        ''' Writes Header area back to image'''
        if image is None:
            image = self.original_image
        else:
            image = bytearray(image)
        header_area = self.toBytes()
        image[self.BCA_OFFSET:self.BCA_OFFSET+self.header_size] = header_area
        return image


    def isValid(self):
        """ Checks if BCA tag is valid meaning it will be read by bootloader """
        if self.tag == self.BCA_KEY:
            return True
        else:
            return False
