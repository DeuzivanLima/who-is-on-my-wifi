# author: DeuzivanLima
# repository: https://github.com/DeuzivanLima/who-is-on-my-wifi
# version: 0.0.1
import nmap, sqlite3, datetime

SQL_CODE_CREATE_TABLE = '''
CREATE TABLE IF NOT EXISTS device (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT NOT NULL,
    MAC TEXT NOT NULL,
    IP TEXT NOT NULL,
    CTIMES_ONLINE INTEGER NOT NULL,
    LAST_TIME_ONLINE TEXT NOT NULL,
    DISPLAY_NAME TEXT
);
'''
print('========= Who Is On My Wi-Fi (0.0.1) =========')

scanner = nmap.PortScanner()
sqlite_conn = sqlite3.connect('devices.db')
cursor = sqlite_conn.cursor()

ip_addr = str(input('IPv4/24?: ')) or '192.168.1.1/24'

print('[+] Scanning...')
scanner.scan(hosts=ip_addr, arguments='-n -sP -PE -PA21,23,80,3389')
hosts_list = [(x, scanner[x]) for x in scanner.all_hosts()]
NULL_MAC = '00:00:00:00:00:00'

cursor.execute(SQL_CODE_CREATE_TABLE)
sqlite_conn.commit()

print('[+] Done!\n')
for host in hosts_list:
    IP = host[1]['addresses']['ipv4']
    NAME = 'Unknow'
    MAC = NULL_MAC

    try:
        MAC = host[1]['addresses']['mac']
        NAME = host[1]['vendor'][MAC]
    except:
        pass

    print(f'\033[32m{MAC}\033[0m<{IP}>: {NAME}')


    device = cursor.execute('SELECT * FROM device WHERE MAC = ?', (MAC,)).fetchall()
    now = datetime.datetime.now()
    if len(device) == 0:

        cursor.execute('INSERT INTO device(MAC, IP, CTIMES_ONLINE, LAST_TIME_ONLINE, NAME) VALUES(?, ?, ?, ?, ?)', (MAC, IP, 1, now, NAME,))
        sqlite_conn.commit()
    else:
        device = device[0]
        cursor.execute('UPDATE device SET CTIMES_ONLINE = ?, LAST_TIME_ONLINE = ? WHERE MAC = ?', (device[4] + 1, now, device[2],))
        sqlite_conn.commit()
        
        if device[2] == MAC and device[3] != IP:
            cursor.execute('UPDATE device SET IP = ? WHERE MAC = ?', (IP, device[2],))
            print(f'IP changed at MAC {device[2]}')
            sqlite_conn.commit()

sqlite_conn.close()
