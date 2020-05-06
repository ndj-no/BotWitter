class User:
    TABLE_NAME = 'account_user'

    def __init__(self, data):
        self.id = -1
        self.username = None
        self.password = None
        self.displayName = None
        self.email = None
        self.phone = None
        self.address = None
        self.dateCreated = None
        self.__dict__.update(data)

    def __str__(self):
        return 'User( id:{:<3}_ username:{:<10}_ displayName:{:<15} )'.format(self.id, self.username, self.displayName)
