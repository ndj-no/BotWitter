class Coupon:
    # noinspection PyPep8Naming
    def __init__(self, data):
        self.coupon_id = None
        self.couponImage = None
        self.couponTitle = None
        self.couponCode = None
        self.expirationDate = None
        self.discountRate = None
        self.discountAmount = None
        self.couponAmount = None
        self.couponDescription = None
        self.__dict__.update(data)

    def __str__(self):
        return 'id({}) _ title({}) _ code({}) _ date({}) _ rate({} %) _ amount({} đ)'.format(self.coupon_id,
                                                                                             self.couponTitle,
                                                                                             self.couponCode,
                                                                                             self.expirationDate,
                                                                                             self.discountRate,
                                                                                             self.discountAmount)
