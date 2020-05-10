class Cart:
    def __init__(self, data):
        self.cart_id = None
        self.user_id = None
        self.detailShoe_id = None
        self.quantityOnCart = None
        self.__dict__.update(data)

    def __str__(self):
        return 'Cart( id:{} _ user_id:{} _ shoe:{} _ quantity:{} )' \
            .format(self.cart_id, self.user_id, self.detailShoe_id, self.quantityOnCart)
