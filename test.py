import requests

url_login = "http://127.0.0.1:8000/api/v1/auth/token/login"
response = requests.post(url_login, data={
    "password": "admin",
    "email": "admin@admin.ru",
})
token = response.json()['auth_token']

base_headers = {
    "Authorization": f"Token {token}"
}

url_courses = "http://127.0.0.1:8000/api/v1/courses/1"
response = requests.get(url_courses, headers=base_headers)
print()

url_courses = "http://127.0.0.1:8000/api/v1/courses/available"
response = requests.get(url_courses, headers=base_headers)

json_ = response.json()

new_course = json_['Courses'][0]

url_courses = f"http://127.0.0.1:8000/api/v1/courses/{new_course['id']}/pay/"
response = requests.post(url_courses, headers=base_headers, json={

})


url = "http://127.0.0.1:8000/api/v1/users/"
