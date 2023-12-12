from starlette import status


def test_create_cow(client):
    response = client.post("/cows", json={
        "_id": "1fbf288b-85d1-4134-be4f-acb05c578ddb",
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
            "amount_I": 0
        },
        "has_calves": True
    })

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "_id": "1fbf288b-85d1-4134-be4f-acb05c578ddb",
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
            "amount_I": 0
        },
        "has_calves": True
    }

def test_get_cows(client):
    response = client.get("/cows")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "_id": "1fbf288b-85d1-4134-be4f-acb05c578ddb",
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
            "amount_I": 0
        },
        "has_calves": True
    }]

def test_get_filtered_cows(client):
    response = client.get("/cows?sex=female")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_cow_by_id(client):
    response = client.get("/cows/1fbf288b-85d1-4134-be4f-acb05c578ddb")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "_id": "1fbf288b-85d1-4134-be4f-acb05c578ddb",
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
            "amount_I": 0
        },
        "has_calves": True
    }

def test_update_cow(client):
    response = client.put("/cows/1fbf288b-85d1-4134-be4f-acb05c578ddb", json={"condition": "healthy"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "_id": "1fbf288b-85d1-4134-be4f-acb05c578ddb",
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
            "amount_I": 0
        },
        "has_calves": True
    }

def test_delete_cow(client):
    response = client.delete("/cows/1fbf288b-85d1-4134-be4f-acb05c578ddb")

    assert response.status_code == status.HTTP_204_NO_CONTENT
