import bme280
import mpu9250
import time
import sys


bme = bme280.Bme280()
mpu = mpu9250.MPU9250()

while True:
    try:
        press = bme.getPressure()
        temp = bme.getTemperature()
        hum = 0
        accXYZ, gyrXYZ = mpu.readAccGyro()
        magXYZ = mpu.readMag()
        temp = mpu.readTemp()

        strAcc ="{:6.2f}, {:6.2f}, {:6.2f}, ".format(accXYZ[0], accXYZ[1], accXYZ[2])
        strGyro ="{:6.2f}, {:6.2f}, {:6.2f}, ".format(gyrXYZ[0], gyrXYZ[1], gyrXYZ[2])
        strMag ="{:6.2f}, {:6.2f}, {:6.2f}, ".format(magXYZ[0], magXYZ[1], magXYZ[2])
        print(strAcc + strGyro + strMag, end='')
        print(f"{press:6.2f}, {temp:6.2f}, {hum:6.2f}")
        sys.stdout.flush()

        bme.readData()
    except KeyboardInterrupt:
        pass
    time.sleep(0.2)


