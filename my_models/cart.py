class Cart:
    def __init__(self, data):
        self.id = -1
        self.user_id = None
        self.detailShoe_id = None
        self.quantity = None
        self.__dict__.update(data)

    def __str__(self):
        return 'Cart( id:{} _ user_id:{} _ shoe:{} _ quantity:{} )' \
            .format(self.id, self.user_id, self.detailShoe_id, self.quantity)
