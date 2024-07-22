# Who Is On My Wifi

## How to run it
You need run with root access to get MAC address and other things.
`~ $ sudo python3 main.py`

## To see all infos on device.db
I'm working to improve a UI to see it, but you can use sqlite3 tool to see

`~ $ sqlite3 device.db`

Enter in box mode
`sqlite3> .mode box`

And print all
`sqlite3> SELECT * FROM device;`
