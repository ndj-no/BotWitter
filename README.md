# BotWitter

Chatbot hỗ trợ bán hàng, chạy cùng với project ![https://github.com/ndj-no/WitterShoe-Django](https://github.com/ndj-no/WitterShoe-Django)

## How to run
1. Run project WitterShoe-Django
2. Tạo Fb Page và lấy access token, key -> thay tương ứng vào file credentials.yml
2. Mở CMD hoặc Terminal và gõ

```bash
$ cd BotWitter
$ pip3 install -r requirement.txt
$ rasa run actions
$ rasa run --endpoints endpoints.yml --credentials credentials.yml
```

tham khảo: [miai.vn](https://www.miai.vn/tag/rasa/)

## Một vài hình ảnh

###Chào hỏi đơn giản

![alt](https://i.imgur.com/vL2GMgS.png)



###Giới thiệu hàng

![alt](https://i.imgur.com/HO6geXt.png)



###Hiển thị hoá đơn

![alt](https://i.imgur.com/bWLpoWW.png)

