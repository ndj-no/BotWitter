class OrderPackage:
    TABLE_NAME = 'order_orderpackage'

    def __init__(self, data):
        self.orderPackage_id = None
        self.user_id = None
        self.dateOrder = None
        self.dateDelivery = None
        self.totalPayment = None
        self.receiver = None
        self.receiverNumber = None
        self.receiverAddress = None
        self.note = None
        self.status = None
        self.__dict__.update(data)

    def __str__(self):
        if int(self.status) == 0:
            status = 'Processing'
        else:
            status = 'Delivered'

        return '[{}] id:{} _ user_id:{} _ receiver:{} _ address:{} _ totalPrice:{}' \
            .format(status, self.orderPackage_id, self.user_id, self.receiver, self.receiverAddress, self.totalPayment)
