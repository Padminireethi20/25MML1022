from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


vehicles = [

    {
        "name": "Vehicle A",
        "hours": 5,
        "impact": 10
    },

    {
        "name": "Vehicle B",
        "hours": 4,
        "impact": 7
    },

    {
        "name": "Vehicle C",
        "hours": 2,
        "impact": 4
    }
]

MAX_HOURS = 8


def scheduler(vehicles, max_hours):

    n = len(vehicles)

    my_list = [

        [0 for i in range(max_hours + 1)]

        for j in range(n + 1)
    ]

    for i in range(1, n + 1):

        curr_hrs = (
            vehicles[i - 1]["hours"]
        )

        curr_impact = (
            vehicles[i - 1]["impact"]
        )

        for remaining_hours in range(
            max_hours + 1
        ):

            if curr_hrs <= remaining_hours:

                my_list[i][remaining_hours] = max(

                    curr_impact +

                    my_list[i - 1][
                        remaining_hours -
                        curr_hrs
                    ],

                    my_list[i - 1][remaining_hours]
                )

            else:

                my_list[i][remaining_hours] = (

                    my_list[i - 1][remaining_hours]
                )

    return my_list[n][max_hours]


@app.route("/schedule")
def schedule():

    max_impact = scheduler(
        vehicles,
        MAX_HOURS
    )

    return jsonify({

        "maximumImpact":
        max_impact

    }), 200


if __name__ == "__main__":

    app.run(debug=True)