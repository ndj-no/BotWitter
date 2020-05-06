class Image:
    def __init__(self, data):
        self.id = -1
        self.shoe_id = None
        self.shoeImage = None
        self.imageDesc = None
        self.__dict__.update(data)

    def __str__(self):
        return 'Image( id:{:<3}_ shoeId:{:<30}_ imageName:{:<15} )' \
            .format(self.id, self.shoe_id, self.shoeImage)
