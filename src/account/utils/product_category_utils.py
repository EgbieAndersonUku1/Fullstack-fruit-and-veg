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
