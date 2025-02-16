import unittest
from unittest.mock import patch, MagicMock
from backend.tools.hotel import HotelTool

class TestHotelTool(unittest.TestCase):
    def setUp(self):
        self.hotel_tool = HotelTool()
        self.mock_location_response = {
            "places": [{
                "location": {
                    "latitude": 48.8566,
                    "longitude": 2.3522
                }
            }]
        }
        self.mock_hotels_response = {
            "places": [
                {
                    "id": "12345",
                    "displayName": {"text": "Test Hotel 1"},
                    "formattedAddress": "123 Test Street, Paris"
                },
                {
                    "id": "67890",
                    "displayName": {"text": "Test Hotel 2"},
                    "formattedAddress": "456 Test Avenue, Paris"
                }
            ]
        }

    @patch('requests.post')
    def test_successful_hotel_search(self, mock_post):
        # Configure mock responses
        mock_responses = [
            MagicMock(status_code=200),
            MagicMock(status_code=200)
        ]
        mock_responses[0].json.return_value = self.mock_location_response
        mock_responses[1].json.return_value = self.mock_hotels_response
        mock_post.side_effect = mock_responses

        # Execute the tool
        result = self.hotel_tool.execute(location="Paris", nb_results=2)

        # Assertions
        self.assertIn("result", result)
        self.assertIn("hotels", result)
        self.assertEqual(len(result["hotels"]), 2)
        self.assertEqual(result["hotels"][0]["name"], "Test Hotel 1")
        self.assertEqual(result["hotels"][1]["name"], "Test Hotel 2")

    @patch('requests.post')
    def test_location_not_found(self, mock_post):
        # Mock empty location response
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {"places": []}
        mock_post.return_value = mock_response

        # Execute the tool
        result = self.hotel_tool.execute(location="NonexistentPlace", nb_results=2)

        # Assertions
        self.assertIn("error", result)
        self.assertEqual(result["error"], "No places found for this location")

if __name__ == '__main__':
    unittest.main()
