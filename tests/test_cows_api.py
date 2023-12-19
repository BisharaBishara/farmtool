from starlette import status

cow = {
        "name": "Bob",
        "sex": "male",
        "birthdate": "2023-12-09T16:46:52.682000+00:00",
        "condition": "string",
        "weight": {
            "mass_kg": 0,
            "last_measured": "2023-12-09T16:46:52.682000+00:00"
        },
        "feeding": {
            "amount_kg": 0,
            "cron_schedule": "* * * * *",
            "last_measured": "2023-12-09T16:46:52.682000+00:00"
        },
        "milk_production": {
            "last_milk": "2023-12-09T16:46:52.682000+00:00",
            "cron_schedule": "* * * * *",
            "amount_l": 0
        },
        "has_calves": True
    }

def test_create_cow(client):
    response = client.post("/cows", json=cow)

    assert response.status_code == status.HTTP_201_CREATED
    response = response.json()
    response = {k:v for k,v in response.items() if k != "_id"}
    assert response == cow

def test_get_cows(client):
    response = client.get("/cows")

    assert response.status_code == status.HTTP_200_OK
    response = response.json()[0]
    response = {k:v for k,v in response.items() if k != "_id"}
    assert response == cow

def test_get_filtered_cows(client):
    response = client.get("/cows?sex=female")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_cow_by_id(client):
    cow_id = client.get("/cows").json()[0]["_id"]

    response = client.get(f"/cows/{cow_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "_id": cow_id,
        **cow
    }

def test_update_cow(client):
    cow_id = client.get("/cows").json()[0]["_id"]
    
    response = client.put(f"/cows/{cow_id}", json={"condition": "healthy"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "_id": cow_id,
        "name": "Bob",
        "sex": "male",
        "birthdate": "2023-12-09T16:46:52.682000+00:00",
        "condition": "healthy",
        "weight": {
            "mass_kg": 0,
            "last_measured": "2023-12-09T16:46:52.682000+00:00"
        },
        "feeding": {
            "amount_kg": 0,
            "cron_schedule": "* * * * *",
            "last_measured": "2023-12-09T16:46:52.682000+00:00"
        },
        "milk_production": {
            "last_milk": "2023-12-09T16:46:52.682000+00:00",
            "cron_schedule": "* * * * *",
            "amount_l": 0
        },
        "has_calves": True
    }

def test_delete_cow(client):
    cow_id = client.get("/cows").json()[0]["_id"]

    response = client.delete(f"/cows/{cow_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
