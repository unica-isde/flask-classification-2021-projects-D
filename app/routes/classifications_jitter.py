import redis
from flask import render_template
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.color_jitter_form import ClassificationColorJitterForm
from ml.classification_utils import classify_image, fetch_image #
from config import Configuration
from torchvision import transforms

config = Configuration()


@app.route('/classifications_jitter', methods=['GET', 'POST'])
def classificationsJitter():
    """API for selecting a model and an image and running a
    classification job. Returns the output scores from the
    model."""
    form = ClassificationColorJitterForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        model_id = form.model.data
        color_values = [form.brightness.data, form.contrast.data, form.saturation.data, form.hue.data]

        modify_image(image_id, color_values)

        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)
        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={
                "model_id": model_id,
                "img_id": image_id,
            })
            task = q.enqueue_job(job)

        # returns the image classification output from the specified model
        # return render_template('classification_output.html', image_id=image_id, results=result_dict)
        return render_template("classification_output_queue.html", image_id=image_id, jobID=task.get_id())

    # otherwise, it is a get request and should return the
    # image and model selector
    return render_template('classification_jitter_select.html', form=form)


def modify_image(img_id, color_values):
    img = fetch_image(img_id)
    transform = transforms.ColorJitter(brightness=color_values[0], contrast=color_values[1],
                                       saturation=color_values[2], hue=color_values[3])
    tensor = transform(img)
    print(tensor)
