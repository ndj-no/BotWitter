## greet path
* greet
  - utter_greet
* introduce
  - act_save_name
  - utter_introduce
  - act_show_menu
  

## path view menu
* ask_view_menu
  - act_show_menu
* deny
  - utter_thank

  
## path get new shoe
* ask_new_shoe
  - act_register_user
  - act_show_new_shoes
* deny
  - act_show_hot_shoes
  
  
## path get new shoe
* ask_new_shoe
  - act_register_user
  - act_show_new_shoes
* ask_shoe_next
  - act_show_hot_shoes


## path get hot shoe
* ask_hot_shoe
  - act_register_user
  - act_show_hot_shoes
* deny
  - act_show_new_shoes


## path get hot shoe 2
* ask_hot_shoe
  - act_register_user
  - act_show_hot_shoes
* ask_shoe_next
  - act_show_new_shoes

## check the size
* ask_shoe_by_size
  - act_check_size
  

## chose color after chose shoe
* ask_specific_shoe
  - act_set_shoe_id
  - act_choose_color
* ask_shoe_by_color
  - act_set_color_id
  - act_check_color
* ask_shoe_by_size
  - act_check_size


## add to cart
* ask_add_to_cart
  - act_register_user
  - act_add_to_cart
  - act_show_cart
* ask_place_order
  - act_place_order


## ask view cart
* ask_view_cart
  - act_show_cart
  
  
## ask edit cart
* ask_edit_cart
  - act_show_cart


## get coupon
* ask_coupon
  - act_register_user
  - act_show_coupons
* ask_save_coupon
  - act_set_coupon_id
  - act_show_menu


## view shoes by category
* ask_list_category
  - act_register_user
  - act_show_list_category
* ask_shoes_by_category
  - act_show_shoes_by_category


## ask help
* ask_help
  - utter_hdsd
  
  
## user thank
* thank
  - utter_thank