import pywifi
import time
import sys
from pywifi import const
import multiprocessing
import os

lock = multiprocessing.Lock()
lock_timeout = 60
latest_lock_at = None


def switch_wifi(fromwifi={'ssid': 'dianmei', 'key': 'dianmei2019'},
                towifi={'ssid': 'Tamcony iphone', 'key': 'asdfghjk'}):
    global lock, latest_lock_at
    switch_id = os.getpid()
    print(f'latest_lock_at: {latest_lock_at}')
    # if latest_lock_at and (time.time()-latest_lock_at)>lock_timeout:
    #     release_switch_wifi_lock()
    #     latest_lock_at = None

    if os.path.exists('_switch_pid'):
        if not latest_lock_at:
            latest_lock_at = time.time()
        return

    with open('_switch_pid', 'w+') as f:
        f.write(str(switch_id))
    print('start switching....')
    max_retry = 5
    retry_count = 0
    while True:
        try:
            r = lock.acquire(block=False)
            print(f'get switch lock: {r}')
            if r:
                connect(fromwifi['ssid'], fromwifi['key'])
                time.sleep(2)
                connect(towifi['ssid'], towifi['key'])
                time.sleep(2)
                break
            else:
                break
        except Exception as e2:
            print(f'switch error: {e2}')
            retry_count += 1
        finally:
            lock.release()

        if retry_count == max_retry and max_retry > 1:
            release_switch_wifi_lock()

        time.sleep(2)

    release_switch_wifi_lock()


def release_switch_wifi_lock():
    if os.path.exists('_switch_pid'):
        os.remove('_switch_pid')


def connect(ssid, key):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    # wifiname = iface.scan_results()[0].ssid

    # for i in wifi.interfaces():
    #     print(i.status())
    #     for r in i.scan_results():
    #         print(r.__dict__)
    #     # if i.status() == const.IFACE_CONNECTED:
    #     #     wifiname = i.scan_results()[0].ssid
    #     #     break

    print('.....wifi disconnectting')
    iface.disconnect()
    time.sleep(1)
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = key

    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(1)
    assert iface.status() == const.IFACE_CONNECTED
    print('.....wifi connectted: ', ssid)


if __name__ == '__main__':
    # connect(ssid='dianmei',key='dianmei2019')
    # time.sleep(2)
    # connect(ssid='Tamcony iphone',key='asdfghjk')
    # connect(ssid='MAXHUB-40V',key='12345678')
    # connect(ssid='dianmei',key='dianmei2019')
    switch_wifi()
    time.sleep(100)