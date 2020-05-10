class OrderPackage:
    TABLE_NAME = 'order_orderpackage'

    def __init__(self, data):
        self.id = None
        self.user_id = None
        self.dateOrder = None
        self.totalPrice = None
        self.receiver = None
        self.address = None
        self.note = None
        self.status = None
        self.discount = None
        self.__dict__.update(data)

    def __str__(self):
        if int(self.status) == 0:
            status = 'Processing'
        else:
            status = 'Delivered'

        return '[{}] OrderPackage( id:{} _ user_id:{} _ receiver:{} _ address:{} _ totalPrice:{} )' \
            .format(status, self.id, self.user_id, self.receiver, self.address, self.totalPrice)
