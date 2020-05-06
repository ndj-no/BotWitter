class OrderItem:
    def __init__(self, data):
        self.id = -1
        self.orderPackage_id = None
        self.detailShoe_id = None
        self.quantity = None
        self.unitPrice = None
        self.__dict__.update(data)

    def __str__(self):
        return 'OrderItem( id:{} _ orderPackage_id:{} _ detailShoe_id:{} _ quantity:{} _ unitPrice:{} )' \
            .format(self.id, self.orderPackage_id, self.detailShoe_id, self.quantity, self.unitPrice)
