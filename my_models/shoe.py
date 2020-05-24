class Shoe:
    TABLE_NAME = 'mainapp_shoe'
    COL_SHOE_MODEL = 'mainapp_shoe'

    def __init__(self, data):
        self.shoe_id = None
        self.shoeName = None
        self.shoeModel = None
        self.shoeThumbnail = None
        self.active = None
        self.quantitySold = None
        self.dateCreated = None
        self.viewCount = None
        self.favouriteCount = None
        self.shoeDesc = None
        self.image_static = None
        self.__dict__.update(data)

    def __str__(self):
        return 'Shoe( id:{:<3}_ name:{:<30}_  quantitySold:{:<5}_ view:{:<4}_ ' \
               'favourite:{:<4} )'.format(self.shoe_id, self.shoeName, self.quantitySold,
                                          self.viewCount, self.favouriteCount)
