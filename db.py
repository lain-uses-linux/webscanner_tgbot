
import sqlite3

class BotDB:
    def __init__(self, db_file):
        # DB initialization
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()


    def user_exists(self, user_id):
        # checking user exists or not
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))


    def get_user_id(self, user_id):
        # getting id of user(users_id) by user_id
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        users_id = result.fetchall()[0][0]
        return users_id

    
    def add_user(self, user_id):
        # adding new user to DB
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()
    

    def add_scan(self, user_id, target, scan_type, scan_output):
        # adding new scan result to DB
        self.cursor.execute(f"INSERT INTO `scans` (`users_id`, `target`, `{scan_type}`) VALUES (?, ?, ?)", (self.get_user_id(user_id), target, scan_output))
        return self.conn.commit()

    
    def get_scans(self, user_id, target, scan_type):
        # getting scan results
        result = self.cursor.execute(f"SELECT {scan_type} FROM `scans` WHERE `users_id` = ? AND `target` = ? AND {scan_type} IS NOT NULL LIMIT 1", (str(self.get_user_id(user_id)), target))
        return result.fetchall()

    
    def get_targets(self, user_id):
        # getting scanned targets
        targets = self.cursor.execute("SELECT DISTINCT `target` FROM `scans` WHERE `users_id`=?", (str(self.get_user_id(user_id)))).fetchall()      
        all_targets = ''
        for i in targets:
            all_targets += str(i[0]) + '\n'
        return all_targets



    def close(self):
        # closing db connection
        self.conn.close()



