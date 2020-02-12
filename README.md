
# BCA Header

This is a helper python script for editing Bootloader Configuration Area (BCA) for MCU Bootloader (NXP Kinetis Bootloader 2) previously named [Kinetis Bootloader](https://www.nxp.com/design/software/development-software/mcuxpresso-software-and-tools/mcuboot-mcu-bootloader-for-nxp-microcontrollers:MCUBOOT)

## Usage of calculate_crc.py
```bash
python calculate_crc.py <binary_image> <result_image>
```

## Required Packages
```
crccheck
```

# TODO
- [ ] Fix CRC check calculation according to manual
- [ ] Fix default values
- [ ] GUI

# Notes
MCU Bootloader uses **Crc32Mpeg2**

## CRC calculation taken from MCU Bootloader manuel page 23
[Manuel Link](https://www.nxp.com/docs/en/reference-manual/MCUBOOTRM.pdf)

The following procedure shows the steps in CRC calculation.
1.  CRC initialization
   - Set the initial CRC as 0xFFFFFFFF, which clears the CRC byte count to 0
2.  CRC calculation
   - Check if the crcExpectedValue field in BCA resides in the address rangespecified for CRC calculation.•  
   - If the crcExpectedValue does not reside in the address range, then computeCRC over every byte value in the address range.
   - If the crcExpectedValue does reside in the address range, then split theaddress range into two parts, splitting at the address of crcExpectedValuefield in BCA excluding crcExpectedValue. 
   - Then, compute the CRC on thetwo parts.
   - Adjust the CRC byte count according to the actual bytes computed.
3.  CRC finalization
   - Check if the CRC byte count is not 4-bytes aligned. If it is 4-bytes aligned, thenpad it with necessary zeroes to finalize the CRC. Otherwise, return the currentcomputed CRC.



# BCA
```c
typedef struct BootloaderConfigurationData
{
    uint32_t tag; //!< [00:03] Tag value used to validate the bootloader configuration data. Must be set to 'kcfg'.
    uint32_t crcStartAddress;              //!< [04:07]
    uint32_t crcByteCount;                 //!< [08:0b]
    uint32_t crcExpectedValue;             //!< [0c:0f]
    uint8_t enabledPeripherals;            //!< [10:10]
    uint8_t i2cSlaveAddress;               //!< [11:11]
    uint16_t peripheralDetectionTimeoutMs; //!< [12:13] Timeout in milliseconds for peripheral detection before jumping
    //! to application code
    uint16_t usbVid;                    //!< [14:15]
    uint16_t usbPid;                    //!< [16:17]
    uint32_t usbStringsPointer;         //!< [18:1b]
    uint8_t clockFlags;                 //!< [1c:1c] High Speed and other clock options
    uint8_t clockDivider;               //!< [1d:1d] One's complement of clock divider, zero divider is divide by 1
    uint8_t bootFlags;                  //!< [1e:1e] One's complemnt of direct boot flag, 0xFE represents direct boot
    uint8_t pad0;                       //!< [1f:1f] Reserved, set to 0xFF
    uint32_t mmcauConfigPointer;        //!< [20:23] Holds a pointer value to the MMCAU configuration
    uint32_t keyBlobPointer;            //!< [24:27] Holds a pointer value to the key blob array used to configure OTFAD
    uint8_t qspiPort;                   //!< [28:28] qspi port: 0xFF-PORTE, 0xFE-PORTC
    uint8_t canConfig1;                 //!< [29:29] ClkSel[1], PropSeg[3], SpeedIndex[4]
    uint16_t canConfig2;                //!< [2a:2b] Pdiv[8], Pseg1[3], Pseg2[3],  rjw[2]
    uint16_t canTxId;                   //!< [2c:2d] txId
    uint16_t canRxId;                   //!< [2e:2f] rxId
    uint32_t qspi_config_block_pointer; //!< [30:33] QSPI config block pointer.
} bootloader_configuration_data_t;
```