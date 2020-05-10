class User:
    TABLE_NAME = 'account_user'

    def __init__(self, data):
        self.user_id = None
        self.username = None
        self.password = None
        self.displayName = None
        self.email = None
        self.phone = None
        self.defaultAddress = None
        self.dateCreated = None
        self.__dict__.update(data)

    def __str__(self):
        return 'User( id:{:<3}_ displayName:{:<10}_ phone:{:<15}_address:{} )'.format(self.user_id,
                                                                                      self.displayName,
                                                                                      self.phone,
                                                                                      self.defaultAddress)
