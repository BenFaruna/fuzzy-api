import os
import dotenv

import requests
import unittest

dotenv.load_dotenv()


class TestAPIEndpoints(unittest.TestCase):
    """This class contain testcases for thr crud enpoint of the API"""

    base_url = os.getenv("API_URL", "http://localhost:8080/api/")

    def setUp(self):
        self.name = "Neo"
        self.update_name = "Nemo"

    def test_create_endpoint(self):
        """Test the create endpoint"""
        res = requests.post(self.base_url, json={"name": self.name})
        # print(requests.delete(self.base_url + self.user))
        self.assertEqual(self.name, res.json().get("user").get("name"))
        self.assertIn("Success", res.json())
        self.assertIn("user", res.json())

    def test_create_endpoint_without_data(self):
        """test the create endpoint response without data"""
        res = requests.post(self.base_url, json={})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), {"Error": "body data not supplied or name key not found"})

    def test_read_endpoint(self):
        """Test the read enpoint for correct response"""
        res = requests.get(self.base_url + self.name)
        user_data = res.json()
        self.assertEqual(list(user_data.keys()), ["id", "name"])
        self.assertEqual(user_data.get("name"), self.name)

    def test_read_endpoint_with_wrong_user(self):
        """Test read endpoint using data not in the database"""
        user = "exampleUser"
        res = requests.get(self.base_url + user)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json(), {"Error": f"{user} not found"})
        # print(requests.delete(self.base_url + self.user))

    def test_update_endpoint(self):
        """test the update endpoint to ensure user detail is updated"""
        res = requests.put(self.base_url + self.name, json={"new_name": self.update_name})
        self.assertEqual(self.update_name, res.json().get("user").get("name"))
        self.assertIn("Success", res.json())
        self.assertIn("user", res.json())

        new_res = requests.get(self.base_url + self.update_name)
        new_res2 = requests.get(self.base_url + self.name)

        self.assertEqual(new_res.status_code, 200)
        self.assertEqual(new_res2.status_code, 404)


    def test_update_endpoint_without_new_name_data(self):
        """test the response of the API when querying the update endpoint without the new_name parameter"""
        res = requests.put(self.base_url + self.update_name, json={})
        self.assertEqual(res.json(), {"Error": "new_name data not supplied"})
        self.assertEqual(res.status_code, 400)

        requests.delete(self.base_url + self.update_name)

    def test_delete_endpopint(self):
        """testing the delete endpoint"""
        user = "deleteUser"
        requests.post(self.base_url, json={"name": user})
        res = requests.delete(self.base_url + user)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(), {"Success": f"{user} deleted"})

        new_res = requests.get(self.base_url + user)
        self.assertEqual(new_res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
