import motor
import motor_pair
import runloop
from hub import port, sound

async def test1():
    motor.run_for_degrees(port.C, -216, 216)
    motor.run_for_degrees(port.D, -216, 216)

#runloop.run(test1())

async def test2():
    motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 410, 0, velocity=333)

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 410, 0, velocity=-333)

#runloop.run(test2())

async def yajuu():
    v = 100
    n4 = 600
    n8 = 300
    n16 = 150

    await sound.beep(466, n4, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(466, n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(311, n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(392, n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(311, n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(466, n8, volume=v);
    await runloop.sleep_ms(5 + n16);

    await sound.beep(390, n8 + n16, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(350, n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(311, n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(294, n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(277, n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(294, n8, volume=v);
    await runloop.sleep_ms(5 + n8);
    await sound.beep(350, n8, volume=v);

    await runloop.sleep_ms(5);
    await sound.beep(392, n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(392, n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(466, n4, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(392, n4, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(466, n4, volume=v);

    await runloop.sleep_ms(5);
    await sound.beep(587, n4 + n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(523, n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(466, n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(392, n8, volume=v);
    await runloop.sleep_ms(5);
    await sound.beep(466, n8, volume=v);

runloop.run(yajuu())
