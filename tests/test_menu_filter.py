"""
Unit tests for menu item filtering functionality.
These tests validate the behavior of the 
find_restaurants_by_food_item function in the database module
"""


from app import database

def test_find_menu_items_by_food_item_base():
    """ Base test cases for find_restaurants_by_food_item function. """
    database.menu_items = [
        {
            "itemId": 1, 
            "restaurantId": 1, 
            "name": "Pizza Margherita", 
            "price": 10.0, 
            "isActive": True},
        {
            "itemId": 2, 
            "restaurantId": 1, 
            "name": "Spaghetti Carbonara", 
            "price": 12.0, 
            "isActive": True},
        {
            "itemId": 3, 
            "restaurantId": 2, 
            "name": "Pizza Pepperoni", 
            "price": 11.0, 
            "isActive": True},
        {
            "itemId": 4, 
            "restaurantId": 2, 
            "name": "Lasagna", 
            "price": 13.0, 
            "isActive": False},
    ]

    results = database.find_restaurants_by_food_item("Pizza")
    assert len(results) == 2
    item_ids = [item["itemId"] for item in results]
    assert 1 in item_ids
    assert 3 in item_ids
    assert 4 not in item_ids

def test_find_menu_items_by_food_item_inactive():
    """ Test case to validate that inactive menu items are not included in results. """
    database.menu_items = [
        {
            "itemId": 1, 
            "restaurantId": 1, 
            "name": "Pizza Margherita", 
            "price": 10.0, 
            "isActive": True},
        {
            "itemId": 2, 
            "restaurantId": 1, 
            "name": "Spaghetti Carbonara", 
            "price": 12.0, 
            "isActive": True},
        {
            "itemId": 3, 
            "restaurantId": 2, 
            "name": "Pizza Pepperoni", 
            "price": 11.0, 
            "isActive": True},
        {
            "itemId": 4, 
            "restaurantId": 2, 
            "name": "Lasagna", 
            "price": 13.0, 
            "isActive": False},
    ]

    results = database.find_restaurants_by_food_item("Pizza")
    assert len(results) == 2
    item_ids = [item["itemId"] for item in results]
    assert 1 in item_ids
    assert 3 in item_ids

def test_find_menu_items_by_food_item_case_insensitive():
    """ Test case to validate that search is case insensitive. """
    database.menu_items = [
        {
            "itemId": 1, 
            "restaurantId": 1,
            "name": "Pizza Margherita",
            "price": 10.0,
            "isActive": True},
        {
            "itemId": 2,
            "restaurantId": 1,
            "name": "Spaghetti Carbonara",
            "price": 12.0,
            "isActive": True},
        {
            "itemId": 3,
            "restaurantId": 2,
            "name": "Pizza Pepperoni",
            "price": 11.0,
            "isActive": True},
        {
            "itemId": 4,
            "restaurantId": 2,
            "name": "Lasagna",
            "price": 13.0,
            "isActive": False},
    ]

    results = database.find_restaurants_by_food_item("pizza")
    assert len(results) == 2
    item_ids = [item["itemId"] for item in results]
    assert 1 in item_ids
    assert 3 in item_ids
def test_find_menu_items_by_food_item_no_match():
    """ Test case to validate that no results are returned when there is no match. """
    database.menu_items = [
        {
            "itemId": 1, 
            "restaurantId": 1, 
            "name": "Pizza Margherita", 
            "price": 10.0, 
            "isActive": True},
        {
            "itemId": 2, 
            "restaurantId": 1, 
            "name": "Spaghetti Carbonara", 
            "price": 12.0, 
            "isActive": True},
        {
            "itemId": 3, 
            "restaurantId": 2, 
            "name": "Pizza Pepperoni", 
            "price": 11.0, 
            "isActive": True},
        {
            "itemId": 4, 
            "restaurantId": 2, 
            "name": "Lasagna", 
            "price": 13.0, 
            "isActive": False},
    ]

    results = database.find_restaurants_by_food_item("Sushi")
    assert len(results) == 0

def test_search_restaurants_by_name():
    """ Test case to validate restaurant search by name. """
    database.users_map = {
        1: {"userId": 1, "name": "Pizza", "role": "restaurant", "email": "a", "password": "b"},
        2: {"userId": 2, "name": "Burger", "role": "restaurant", "email": "a", "password": "b"},
        3: {"userId": 3, "name": "Sushi", "role": "restaurant", "email": "a", "password": "b"},
        4: {"userId": 4, "name": "Admin", "role": "admin", "email": "a", "password": "b"}
    }
    results = database.search_restaurants_by_name("planet")
    assert len(results) == 2
    r_names = [r["name"] for r in results]
    assert "Pizza" in r_names
    assert "Planet of Sushi" in r_names

def test_search_restaurants_by_name_no_match():
    """ Test case to validate restaurant search with no match. """
    database.users_map = {
        1: {"userId": 1, "name": "Pizza", "role": "restaurant", "email": "a", "password": "b"}
    }
    results = database.search_restaurants_by_name("Tacos")
    assert len(results) == 0
