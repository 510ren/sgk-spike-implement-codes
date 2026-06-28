from hub import port
import motor_pair
from hub import sound
import runloop

# Setup
motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

# Classes
class Direction:
    CW = 1 # 時計回り
    CCW = -1 # 反時計回り

# Utilities
def cmToDegrees(cm: int):
    return int(cm * 41 / 2) # 調整必須

def powerPercentageToNumber(p: int):
    return int(1110 * p / 100)

async def rotation(degrees: int, power):
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, degrees, 100, velocity=powerPercentageToNumber(power))

async def oneRotation(direction: int, power: int = 100):
    await rotation(360 * direction, power)

async def halfRotation(direction: int, power: int = 100):
    await rotation(180 * direction, power)

async def goingStraight(cm: int, power: int = 100):
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, cmToDegrees(cm), 0, velocity=powerPercentageToNumber(power))

async def playSound(hz: int, time: int):
    await sound.beep(int(hz * 2), time, 100)
    await runloop.sleep_ms(5)

# Implementation
async def test1():
    await goingStraight(45, power=30)
    await goingStraight(-45, power=30)

async def test2():
    await goingStraight(45, power=30)
    await oneRotation(Direction.CW, power=30)
    await goingStraight(45, power=30)

async def test3():
    for i in range(3):
        print(str(i + 1) + '回目')
        await test2()
        await oneRotation(Direction.CW, power=30)

async def test4():
    shortSide = 40
    longSide = 52

    await goingStraight(shortSide)
    await halfRotation(Direction.CW)
    await goingStraight(longSide)
    await halfRotation(Direction.CW)
    await goingStraight(shortSide + 4)
    await halfRotation(Direction.CW)
    await goingStraight(longSide + 2)

async def test5():
    shortSide = 40
    longSide = 52

    longSideHalf = int(longSide / 2) + 1

    await goingStraight(10)
    await halfRotation(Direction.CCW)
    await goingStraight(longSideHalf)
    await halfRotation(Direction.CW)
    await goingStraight(shortSide + 4)
    await halfRotation(Direction.CW)
    await goingStraight(longSideHalf)
    await halfRotation(Direction.CCW)
    await goingStraight(20)

async def test6():
    await goingStraight(60)
    await halfRotation(Direction.CCW)
    await goingStraight(90)

async def test7():
    await test6()
    await oneRotation(Direction.CCW)
    await goingStraight(90)
    await halfRotation(Direction.CCW)
    await goingStraight(60)

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

runloop.run(yajuu())
