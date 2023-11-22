
import sqlite3


try:
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    '''
    cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (1339,))
    users = cursor.execute("SELECT * FROM `users`")
    print(users.fetchall())
    '''
    
    #cursor.execute("INSERT INTO `scans` (`users_id`, `target`, `wappalyzer`) VALUES (?, ?, ?)", (1337, 'http://youtube3.com', 'test'))
    '''
    scans = cursor.execute("SELECT wappalyzer FROM `scans` WHERE (users_id=3 AND target='http://hackerone.com' AND wappalyzer IS NOT NULL) LIMIT 1;")
    print(scans.fetchall())
    scans = cursor.execute("SELECT subdomains FROM `scans` WHERE users_id=3 AND target='http://hackerone.com' AND subdomains IS NOT NULL LIMIT 1")
    print(scans.fetchall())
    scans = cursor.execute("SELECT dirbuster FROM `scans` WHERE users_id=3 AND target='http://hackerone.com' AND dirbuster IS NOT NULL LIMIT 2,1")
    print(scans.fetchall())
    '''

    scans = cursor.execute("SELECT DISTINCT target FROM `scans` WHERE users_id=1337")
    #print(scans.fetchall())
    for i in scans.fetchall():
        print(i[0])

    conn.commit()

except sqlite3.Error as error:
    print("Database error", error)

finally:
    if(conn):
        conn.close()


