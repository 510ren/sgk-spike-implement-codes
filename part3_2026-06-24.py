from hub import port
import motor_pair
import color, color_sensor
from hub import sound
import runloop

# Setup
motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

# Classes
class Direction:
    CW = 1 # 時計回り
    CCW = -1 # 反時計回り

# Constants
lightGreyReflectionRange = {
    "min": 55,
    "max": 70
}
darkGreyReflectionRange = {
    "min": 35,
    "max": 55
}
blackReflectionRange = {
    "min": 10,
    "max": 35
}

# Utilities

## Chore
def cmToDegrees(cm: int):
    return int(cm * 41 / 2)

def powerPercentageToNumber(p: int):
    return int(1110 * p / 100)

## Motor
async def rotation(degrees: int, power):
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degrees, 100, velocity=powerPercentageToNumber(power))

async def oneRotation(direction: int, power: int = 100):
    await rotation(360 * direction, power)

async def halfRotation(direction: int, power: int = 100):
    await rotation(180 * direction, power)

async def quarterRotation(direction: int, power: int = 100):
    await rotation(90 * direction, power)

async def goingStraightForSpecifiedLength(cm: int, power: int = 100):
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, cmToDegrees(cm), 0, velocity=powerPercentageToNumber(power))

def goingStraightToEternity(power: int = 100):
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=powerPercentageToNumber(power))

def stopMotor():
    motor_pair.stop(motor_pair.PAIR_1)

## Colors
def getCurrentColorSencorData():
    return {
        "A": {
            "color": color_sensor.color(port.A),
            "reflection": color_sensor.reflection(port.A)
        },
        "B": {
            "color": color_sensor.color(port.B),
            "reflection": color_sensor.reflection(port.B)
        }
    }

def isDetectedRed(value):
    return (value is color.RED) or (value is color.UNKNOWN)

def checkSencorReflectionRange(reflection, rangeDic):
    if (reflection < rangeDic['min']) or (reflection > rangeDic['max']):
        return False

    return True

def isSencorDetectedRed():
    colorSencorData = getCurrentColorSencorData()

    return isDetectedRed(colorSencorData['A']['color']) or isDetectedRed(colorSencorData['B']['color'])

def isSencorDetectedSpecifiedRangeReflection(reflectionRange):
    colorSencorData = getCurrentColorSencorData()

    AResults = checkSencorReflectionRange(colorSencorData['A']['reflection'], reflectionRange)
    BResults = checkSencorReflectionRange(colorSencorData['B']['reflection'], reflectionRange)

    return {
        "results": AResults or BResults,
        "a": AResults,
        "b": BResults
    }

## Sounds
async def playSound(hz: int, time: int):
    await sound.beep(int(hz * 2), time, 50)
    await runloop.sleep_ms(5)

# Implementation
async def test1():
    goingStraightToEternity(30)

    while True:
        if isSencorDetectedRed():
            stopMotor()
            break;

        await runloop.sleep_ms(100)

async def test2():
    goingStraightToEternity(30)

    while True:
        if isSencorDetectedSpecifiedRangeReflection(darkGreyReflectionRange)['results']:
            stopMotor()
            break

        await runloop.sleep_ms(100)

async def test3():
    goingStraightToEternity(50)

    while True:
        if isSencorDetectedSpecifiedRangeReflection(lightGreyReflectionRange)['results']:
            print('Detected light grey!')
            goingStraightToEternity(30)
        elif isSencorDetectedSpecifiedRangeReflection(darkGreyReflectionRange)['results']:
            print('Detected dark grey!')
            goingStraightToEternity(20)
        elif isSencorDetectedSpecifiedRangeReflection(blackReflectionRange)['results']:
            print('Detected black!')
            goingStraightToEternity(10)
        else:
            print('Detected other!')
            goingStraightToEternity(30)

        await runloop.sleep_ms(100)

async def test4():
    goingStraightToEternity(30)

    while True:
        results = isSencorDetectedSpecifiedRangeReflection(blackReflectionRange)
        if  results['a']:
            print('Detected black!')
            await quarterRotation(Direction.CW, power=30)
            goingStraightToEternity(30)
        elif results['b']:
            print('Detected black!')
            await quarterRotation(Direction.CCW, power=30)
            goingStraightToEternity(30)

        await runloop.sleep_ms(100)

async def test5():
    goingStraightToEternity(30)

    while True:
        results = isSencorDetectedSpecifiedRangeReflection(blackReflectionRange)
        if results['b']:
            await rotation(30, power=30)
            await goingStraightForSpecifiedLength(-1, 30)
            goingStraightToEternity(30)
        elif results['a']:
            await rotation(-60, power=30)
            await goingStraightForSpecifiedLength(-1, 30)
            goingStraightToEternity(30)

        await runloop.sleep_ms(100)

async def test6():
    while True:
        results = isSencorDetectedSpecifiedRangeReflection(blackReflectionRange)
        if results['b']:
            motor_pair.move(motor_pair.PAIR_1, -60, velocity=powerPercentageToNumber(30))
        else:
            motor_pair.move(motor_pair.PAIR_1, 60, velocity=powerPercentageToNumber(30))

        await runloop.sleep_ms(100)

async def test7():
    goingStraightToEternity(30)

    while True:
        sencorData = getCurrentColorSencorData()
        diff = sencorData['A']['reflection'] - sencorData['B']['reflection']

        if abs(diff) < 10:
            goingStraightToEternity(30)
        elif diff > 10:
            await rotation(45, power=30)
            await goingStraightForSpecifiedLength(2, 30)
            goingStraightToEternity(30)
        else:
            await rotation(-45, power=30)
            await goingStraightForSpecifiedLength(2, 30)

        await runloop.sleep_ms(100)

async def yajuu():
    n4 = 600
    n8 = 300
    n16 = 150

    await playSound(392, n8)
    await playSound(466, n8)
    await playSound(392, n8)
    await playSound(466, n8)
    await playSound(622, n4)

    await playSound(440, n8)
    await playSound(587, n8)
    await playSound(349, n8)

    await playSound(587, n8)
    await playSound(523, n8)
    await playSound(587, n8)
    await playSound(698, n4)

    await playSound(392, n8)
    await playSound(392, n8)
    await playSound(294, n8)
    await playSound(392, n8)
    await playSound(440, n8)
    await playSound(466, n8)
    await playSound(196, n4)

    await playSound(233, n8)
    await playSound(262, n8)
    await playSound(294, n8)
    await playSound(262, n8)
    await playSound(233, n8)
    await playSound(233, n4 + n8)
    await runloop.sleep_ms(n8)

    await playSound(466, n4)
    await playSound(466, n8)
    await playSound(311, n8)
    await playSound(392, n8)
    await playSound(311, n8)
    await playSound(466, n8)
    await runloop.sleep_ms(n16)

    await playSound(390, n8 + n16)
    await playSound(350, n8)
    await playSound(311, n8)
    await playSound(294, n8)
    await playSound(277, n8)
    await playSound(294, n8)
    await runloop.sleep_ms(n8)

    await playSound(350, n8)
    await playSound(392, n8)
    await playSound(392, n8)
    await playSound(466, n4)
    await playSound(392, n4)
    await playSound(466, n4)

    await playSound(587, n4 + n8)
    await playSound(523, n8)
    await playSound(466, n8)
    await playSound(392, n8)
    await playSound(466, n8)
    await runloop.sleep_ms(n8)

    await playSound(466, n4)
    await playSound(466, n8)
    await playSound(311, n8)
    await playSound(392, n8)
    await playSound(311, n8)
    await playSound(466, n8)
    await runloop.sleep_ms(n16)

    await playSound(390, n8 + n16)
    await playSound(350, n8)
    await playSound(311, n8)
    await playSound(294, n8)
    await playSound(277, n8)
    await playSound(294, n8)
    await runloop.sleep_ms(n8)

    await playSound(350, n8)
    await playSound(392, n8)
    await playSound(392, n8)
    await playSound(466, n4)
    await playSound(392, n4)
    await playSound(466, n4)

    await playSound(466, n8)
    await playSound(392, n16)
    await playSound(466, n8)
    await playSound(392, n16)
    await playSound(524, n8)
    await playSound(466, n4)

    await runloop.sleep_ms(n4)

    await yajuu()

runloop.run(yajuu(), test7())
