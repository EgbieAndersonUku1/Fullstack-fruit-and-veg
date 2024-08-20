def get_product_category_choices():
    """
    Returns a list of tuples representing product category choices for a form field.

    Each tuple in the list represents a category group or a single category, formatted as follows:
    
    - A tuple with a string label and a list of tuples for grouped categories:
      - The first element is the category group label (e.g., 'Fruits & Vegetables').
      - The second element is a list of tuples where each tuple represents a category within that group.
        Each category tuple contains:
        - A value (e.g., 'fresh_fruits') used for form submission.
        - A human-readable label (e.g., 'Fresh Fruits').

    - A tuple with a single string label and an optional value for non-grouped categories.

    The list begins with a placeholder option for the user to select a category. This placeholder has an empty value and
    is marked as 'Select a category'.

    Returns:
        list: A list of tuples where each tuple represents a choice for a form field. The first element of the tuple is 
        the value to be sent to the server upon form submission, and the second element is the display label for that value.
        Category groups are represented as tuples with a list of category tuples.

    Example:
        [
            ('', 'Select a category'),
            ('new', 'New Category'),
            ('Fruits & Vegetables', [
                ('fresh_fruits', 'Fresh Fruits'),
                ('fresh_vegetables', 'Fresh Vegetables'),
                ('organic_greens', 'Organic Greens'),
            ]),
            ...
        ]
    """
    return [
        ('', 'Select a category'),  # Placeholder option
        ('new', 'New Category'),
        ('Fruits & Vegetables', [
            ('fresh_fruits', 'Fresh Fruits'),
            ('fresh_vegetables', 'Fresh Vegetables'),
            ('organic_greens', 'Organic Greens'),
        ]),
        ('Dairy Products', [
            ('milk', 'Milk'),
            ('cheese', 'Cheese'),
            ('yogurt', 'Yogurt'),
        ]),
        ('Meat & Seafood', [
            ('meat', 'Meat'),
            ('poultry', 'Poultry'),
            ('seafood', 'Seafood'),
        ]),
        ('Pantry Staples', [
            ('grains_rice', 'Grains & Rice'),
            ('pasta_noodles', 'Pasta & Noodles'),
            ('baking_essentials', 'Baking Essentials'),
            ('canned_goods', 'Canned Goods'),
        ]),
        ('Beverages', [
            ('juices', 'Juices'),
            ('teas', 'Teas'),
            ('coffee', 'Coffee'),
            ('smoothies', 'Smoothies'),
        ]),
        ('Snacks & Sweets', [
            ('chips_crackers', 'Chips & Crackers'),
            ('cookies_bars', 'Cookies & Bars'),
            ('dried_fruits_nuts', 'Dried Fruits & Nuts'),
            ('chocolates_candies', 'Chocolates & Candies'),
        ]),
        ('Frozen Foods', [
            ('frozen_meals', 'Frozen Meals'),
            ('frozen_vegetables_fruits', 'Frozen Vegetables & Fruits'),
            ('frozen_desserts', 'Frozen Desserts'),
        ]),
        ('Baby & Kids', [
            ('baby_food', 'Baby Food'),
            ('snacks_for_kids', 'Snacks for Kids'),
            ('baby_formula', 'Baby Formula'),
        ]),
    ]



def get_product_color_choices():
    
    colors = [
           {"id": "colorRed",    "name": "color",  "data_color": "red",    "value": "red"},
           {"id": "colorGreen",  "name": "color",  "data_color": "green",  "value": "green"},
           {"id": "colorBlue",   "name": "color",  "data_color": "blue",   "value": "blue"},
           {"id": "colorYellow", "name": "color",  "data_color": "yellow", "value": "yellow"},
           {"id": "colorBlack",  "name": "color",  "data_color": "black",  "value": "black"},
           {"id": "colorWhite",  "name": "color",  "data_color": "white",  "value": "white"},
           {"id": "colorPurple", "name": "color",  "data_color": "purple", "value": "purple"},
           {"id": "colorOrange", "name": "color",  "data_color": "orange", "value": "orange"},
           {"id": "colorPink",   "name": "color",  "data_color": "pink",   "value": "pink"},
           {"id": "colorBrown",  "name": "color",  "data_color": "brown",  "value": "brown"},
           {"id": "colorGray",   "name": "color",  "data_color": "gray",   "value": "gray"},
           {"id": "colorCyan",   "name": "color",  "data_color": "cyan",   "value": "cyan"},
           {"id": "colorMagenta", "name": "color", "data_color": "magenta", "value": "magenta"},
           {"id": "colorLime",   "name": "color",  "data_color": "lime",   "value": "lime"},
           {"id": "colorTeal",   "name": "color",  "data_color": "teal",   "value": "teal"},
           {"id": "colorIndigo", "name": "color",  "data_color": "indigo", "value": "indigo"}
       ]
    
    return colors



def get_product_size_chocies():
    sizes = [
        {"id" :"small",  "name": "size", "value" : "small",  "data_size": "small",  "class": "item-small"},
        {"id" :"medium", "name": "size", "value" : "medium", "data_size": "medium", "class": "item-medium"},
        {"id" :"large",  "name": "size", "value" : "large",  "data_size": "large",  "class": "item-large"}
    ]
    return sizes


def get_shipping_options():
    """
    Returns a list of shipping options for a form, including details for each shipping method.
    
    Each option contains:
    - A label for display
    - Input details (name, value, data attributes, aria attributes)
    - Screen reader accessible elements providing descriptions
    
    Returns:
        list: A list of dictionaries where each dictionary represents a shipping option.
    """
    return [
        {
            "label": "Standard Shipping (3-5 business days) - £3.99",
            "input": {
                "name": "shipping",
                "value": "standard",
                "data": {
                    "shipping_type": "standard",
                    "cost": "3.99",
                    "delivery_time": "3-5 business days"
                },
                "aria": {
                    "describedby": "standard-desc"
                },
                "id": "standard"
            },
            "screen_reader_elems": {
                "id": "standard-desc",
                "text": "Standard shipping with delivery in 3 to 5 business days"
            }
        },
        {
            "label": "Express Shipping (1-2 business days) - £5.99",
            "input": {
                "name": "shipping",
                "value": "express",
                "data": {
                    "shipping_type": "express",
                    "cost": "5.99",
                    "delivery_time": "1-2 business days"
                },
                "aria": {
                    "describedby": "express-desc"
                },
                "id": "express"
            },
            "screen_reader_elems": {
                "id": "express-desc",
                "text": "Express shipping with delivery in 1 to 2 business days"
            }
        },
        {
            "label": "Next-Day Delivery - £9.99",
            "input": {
                "name": "shipping",
                "value": "next-day",
                "data": {
                    "shipping_type": "next-day",
                    "cost": "9.99",
                    "delivery_time": "Next-Day Delivery"
                },
                "aria": {
                    "describedby": "next-day-desc"
                },
                "id": "next-day"
            },
            "screen_reader_elems": {
                "id": "next-day-desc",
                "text": "Next-day delivery option"
            }
        },
        {
            "label": "Same-Day Delivery (order by 2 PM) - £14.99",
            "input": {
                "name": "shipping",
                "value": "same-day",
                "data": {
                    "shipping_type": "same-day",
                    "cost": "14.99",
                    "delivery_time": "Same-Day Delivery (order by 2 PM)"
                },
                "aria": {
                    "describedby": "same-day-desc"
                },
                "id": "same-day"
            },
            "screen_reader_elems": {
                "id": "same-day-desc",
                "text": "Same-day delivery option, order by 2 PM"
            }
        },
        {
            "label": "Click and Collect (1-2 days) - Free",
            "input": {
                "name": "shipping",
                "value": "click-collect",
                "data": {
                    "shipping_type": "click-collect",
                    "cost": "0.00",
                    "delivery_time": "1-2 days"
                },
                "aria": {
                    "describedby": "click-collect-desc"
                },
                "id": "click-collect"
            },
            "screen_reader_elems": {
                "id": "click-collect-desc",
                "text": "Click and Collect option with delivery in 1 to 2 days"
            }
        },
        {
            "label": "Weekend Delivery - £7.99",
            "input": {
                "name": "shipping",
                "value": "weekend",
                "data": {
                    "shipping_type": "weekend",
                    "cost": "7.99",
                    "delivery_time": "Weekend Delivery"
                },
                "aria": {
                    "describedby": "weekend-desc"
                },
                "id": "weekend"
            },
            "screen_reader_elems": {
                "id": "weekend-desc",
                "text": "Weekend delivery option"
            }
        },
        {
            "label": "Free Shipping (orders over £50) - Free",
            "input": {
                "name": "shipping",
                "value": "free",
                "data": {
                    "shipping_type": "free",
                    "cost": "0.00",
                    "delivery_time": "Free Shipping (orders over £50)"
                },
                "aria": {
                    "describedby": "free-desc"
                },
                "id": "free"
            },
            "screen_reader_elems": {
                "id": "free-desc",
                "text": "Free shipping for orders over £50"
            }
        }
    ]
