from app import app
from flask import render_template, Response
from .classifications_id import classifications_id
import json


@app.route('/json_results/<string:job_id>', methods=['GET'])
def json_results(job_id):
    """API for downloading the result of the classification
    in JSON format"""
    response = classifications_id(job_id)

    # Convert the response into a dict to render it better with json
    data = _response_list_to_dict(response)

    # Download the json file
    return Response(json.dumps(data, indent=4),
                    mimetype='application/json',
                    headers={"Content-disposition":
                                 "attachment; filename=classification.json"}
                    )


def _response_list_to_dict(response):
    """
    Function that convert the response list (made up by pairs(label, value)) into a dict
    """
    data = dict()
    for pair in response['data']:
        data[pair[0]] = pair[1]

    return data
