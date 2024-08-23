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
        {"id": "colorRed",    "name": "color",  "value": "Red"},
        {"id": "colorGreen",  "name": "color",  "value": "Green"},
        {"id": "colorBlue",   "name": "color",  "value": "Blue"},
        {"id": "colorYellow", "name": "color",  "value": "Yellow"},
        {"id": "colorBlack",  "name": "color",  "value": "Black"},
        {"id": "colorWhite",  "name": "color",  "value": "White"},
        {"id": "colorPurple", "name": "color",  "value": "Purple"},
        {"id": "colorOrange", "name": "color",  "value": "Orange"},
        {"id": "colorPink",   "name": "color",  "value": "Pink"},
        {"id": "colorBrown",  "name": "color",  "value": "Brown"},
        {"id": "colorGray",   "name": "color",  "value": "Gray"},
        {"id": "colorCyan",   "name": "color",  "value": "Cyan"},
        {"id": "colorMagenta", "name": "color", "value": "Magenta"},
        {"id": "colorLime",   "name": "color",  "value": "Lime"},
        {"id": "colorTeal",   "name": "color",  "value": "Teal"},
        {"id": "colorIndigo", "name": "color",  "value": "Indigo"}
    ]

    
    return colors



def get_product_size_choices():
    sizes = [
        {"id" :"small",  "name": "size", "value" : "Small",  "data_size": "small",  "class": "item-small"},
        {"id" :"medium", "name": "size", "value" : "Medium", "data_size": "medium", "class": "item-medium"},
        {"id" :"large",  "name": "size", "value" : "Large",  "data_size": "large",  "class": "item-large"}
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
                "value": "Standard",
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
                "value": "Express",
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
                "value": "Next-Day-Delivery",
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
                "value": "Same-Day",
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
                "value": "Click-Collect",
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
                "value": "Weekend",
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
                "value": "Free",
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
