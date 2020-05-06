class DetailShoe:
    def __init__(self, data):
        self.detailShoe_id = -1
        self.shoe_id = None
        self.color_id = None
        self.size = None
        self.quantityAvailable = None
        self.oldPrice = None
        self.newPrice = None
        self.detailShoeDesc = None
        self.__dict__.update(data)

    def __str__(self):
        return 'DetailShoe( id:{} _ shoeID:{} _ color:{} _ size:{} _ quantityAvailable:{} _ ' \
               'oldPrice:{} _ newPrice:{} )' \
            .format(self.id, self.shoe_id, self.color_id, self.size, self.quantityAvailable,
                    self.oldPrice, self.newPrice)
