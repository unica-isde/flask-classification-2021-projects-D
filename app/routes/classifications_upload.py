import os

import redis
from flask import render_template, request
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import classify_image
from config import Configuration

config = Configuration()


@app.route('/classifications_upload', methods=['GET', 'POST'])
def classificationsUpload():
    """
    API that allows the user to upload an image and classify it.
    The image is saved on the server and on page reload it gets deleted.
    The API checks if the user actually uploaded an image and if so it classifies it,
    otherwise the page is reloaded.
    """

    form = ClassificationForm()
    if request.method == "POST":  # POST
        model_id = form.model.data

        # Saving uploaded image
        file = request.files['file']
        filename = 'uploaded_' + file.filename
        file.save('app/static/imagenet_subset/' + filename)

        image_id = filename

        # Check if the user uploaded the file
        if file.filename != '':
            redis_url = Configuration.REDIS_URL
            redis_conn = redis.from_url(redis_url)
            with Connection(redis_conn):
                q = Queue(name=Configuration.QUEUE)
                job = Job.create(classify_image, kwargs={
                    "model_id": model_id,
                    "img_id": image_id
                })
                task = q.enqueue_job(job)

            # returns the image classification output from the specified model
            # return render_template('classification_output.html', image_id=image_id, results=result_dict)
            return render_template("classification_output_queue.html", image_id=image_id, jobID=task.get_id())

    # otherwise, it is a get request and should return the
    # image and model selector

    # On page loading, all the uploaded images are deleted
    for file in os.listdir("app/static/imagenet_subset"):
        if file.startswith("uploaded"):
            try:
                os.remove("app/static/imagenet_subset/" + file)
            except FileNotFoundError:
                pass

    return render_template('classification_upload.html', form=form)
