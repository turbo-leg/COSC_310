from app import database

def test_find_menu_items_by_food_item_base():
    database.menu_items = [
        {"itemId": 1, "restaurantId": 1, "name": "Pizza Margherita", "price": 10.0, "isActive": True},
        {"itemId": 2, "restaurantId": 1, "name": "Spaghetti Carbonara", "price": 12.0, "isActive": True},
        {"itemId": 3, "restaurantId": 2, "name": "Pizza Pepperoni", "price": 11.0, "isActive": True},
        {"itemId": 4, "restaurantId": 2, "name": "Lasagna", "price": 13.0, "isActive": False},
    ]
    
    results = database.find_restaurants_by_food_item("Pizza")
    assert len(results) == 2
    assert 1 in results
    assert 2 in results
    assert len(results[1]) == 1
    assert len(results[2]) == 1
    assert 4 not in results

def test_find_menu_items_by_food_item_inactive():
    database.menu_items = [
        {"itemId": 1, "restaurantId": 1, "name": "Pizza Margherita", "price": 10.0, "isActive": True},
        {"itemId": 2, "restaurantId": 1, "name": "Spaghetti Carbonara", "price": 12.0, "isActive": True},
        {"itemId": 3, "restaurantId": 2, "name": "Pizza Pepperoni", "price": 11.0, "isActive": False},
        {"itemId": 4, "restaurantId": 2, "name": "Lasagna", "price": 13.0, "isActive": False},
    ]
    
    results = database.find_restaurants_by_food_item("Pizza")
    assert len(results) == 1
    assert 1 in results
    assert len(results[1]) == 1
    assert 3 not in results

def test_find_menu_items_by_food_item_case_insensitive():
    database.menu_items = [
        {"itemId": 1, "restaurantId": 1, "name": "Pizza Margherita", "price": 10.0, "isActive": True},
        {"itemId": 2, "restaurantId": 1, "name": "Spaghetti Carbonara", "price": 12.0, "isActive": True},
        {"itemId": 3, "restaurantId": 2, "name": "Pizza Pepperoni", "price": 11.0, "isActive": True},
        {"itemId": 4, "restaurantId": 2, "name": "Lasagna", "price": 13.0, "isActive": False},
    ]
    
    results = database.find_restaurants_by_food_item("pizza")
    assert len(results) == 2
    assert 1 in results
    assert 2 in results
    assert len(results[1]) == 1
    assert len(results[2]) == 1

def test_find_menu_items_by_food_item_no_match():
    database.menu_items = [
        {"itemId": 1, "restaurantId": 1, "name": "Pizza Margherita", "price": 10.0, "isActive": True},
        {"itemId": 2, "restaurantId": 1, "name": "Spaghetti Carbonara", "price": 12.0, "isActive": True},
        {"itemId": 3, "restaurantId": 2, "name": "Pizza Pepperoni", "price": 11.0, "isActive": True},
        {"itemId": 4, "restaurantId": 2, "name": "Lasagna", "price": 13.0, "isActive": False},
    ]
    
    results = database.find_restaurants_by_food_item("Sushi")
    assert len(results) == 0    
