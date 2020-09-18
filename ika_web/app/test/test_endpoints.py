# import os
# import requests

# def test_credentials_test(api_v1_host):
#     endpoint = os.path.join(api_v1_host, 'credentials', 'test')
#     response = requests.get(endpoint)
#     assert response.status_code == 200
#     json = response.json()
#     assert 'msg' in json
#     assert json['msg'] == "I'm the test endpoint from credentials."

# def test_blueprint_y_test(api_v1_host):
#     endpoint = os.path.join(api_v1_host, 'path_for_blueprint_y', 'test')
#     response = requests.get(endpoint)
#     assert response.status_code == 200
#     json = response.json()
#     assert 'msg' in json
#     assert json['msg'] == "I'm the test endpoint from blueprint_y."

# def test_blueprint_x_plus(api_v1_host):
#     endpoint = os.path.join(api_v1_host, 'path_for_blueprint_x', 'plus')
#     payload = {'number': 5}
#     response = requests.post(endpoint, json=payload)
#     assert response.status_code == 200
#     json = response.json()
#     assert 'msg' in json
#     assert json['msg'] == "Your result is: '10'"

# def test_blueprint_x_minus(api_v1_host):
#     endpoint = os.path.join(api_v1_host, 'path_for_blueprint_y', 'minus')
#     payload = {'number': 1000}
#     response = requests.post(endpoint, json=payload)
#     assert response.status_code == 200
#     json = response.json()
#     assert 'msg' in json
#     assert json['msg'] == "Your result is: '0'"