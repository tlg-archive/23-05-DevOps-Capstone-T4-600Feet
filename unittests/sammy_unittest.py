import sys
import unittest
from unittest.mock import Mock, patch

sys.path.append('..')

from main import handle_item_interaction 

mock_widget = Mock()

# mock classes
class MockSubmarine:
    def __init__(self):
        self.rooms = {1: {"content": [{"name": "advil", "properties": {"heal": 5}}]}}

    def is_item_in_room(self, item_name, room):
        room_content = self.rooms[room]['content']
        for content in room_content:
            if content["name"] == item_name:
                return True
        return False

    def rem_room_content(self, item_name, room):
        room_content = self.rooms[room]['content']
        for content in room_content:
            if content["name"] == item_name:
                room_content.remove(content)
                break

    def place_item(self, item_name, room):
        if item_name == "advil":
            self.rooms[room]['content'].append({"name": "advil", "properties": {"heal": 5}})
        elif item_name == "key":
            self.rooms[room]['content'].append({"name": "a key", "properties": {"unlock": "True"}})

class MockPlayer:
    def __init__(self):
        self.current_room = 1
        self.inventory = []

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        self.inventory.remove(item)

# calss for testing
@patch('main.update_output', return_value=None)
class TestHandleItemInteraction(unittest.TestCase):

    def setUp(self):
        # Set up the test environment
        self.submarine = MockSubmarine()
        self.player = MockPlayer()

    def test_handle_item_take(self, mock_update_output):
        handle_item_interaction(self.player, "advil", "t", self.submarine)
    
        room_content = [item["name"] for item in self.submarine.rooms[1]["content"]]
        self.assertNotIn("advil", room_content)
        self.assertIn("advil", self.player.inventory)


    def test_handle_item_drop(self, mock_update_output):
        # Test drop
        self.player.add_to_inventory("advil")
        handle_item_interaction(self.player, "advil", "d", self.submarine)
        self.assertNotIn("advil", self.player.inventory)
        room_content = [item["name"] for item in self.submarine.rooms[1]["content"]]
        self.assertIn("advil", room_content)


if __name__ == '__main__':
    unittest.main()
