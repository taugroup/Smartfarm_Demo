from os import strerror
from ultralytics import YOLO
from jinja2 import Template
import json
import numpy as np


template = Template("""
{
  "DateType": "MultipleElements",
  "Quantity": {{ quantity }},
  "TimeStamp": {
    "counter": {{ counter }}
  },
  "Grid": {
    "scale": "{{ scale }}",
    "type": "{{ type }}"
  },
  "Data": {
    "humidity": {{ humidity }},
    "temperature": {{ temperature }},
    "co2" : {{ co2 }}
  },
  "Elements": {
    {% for element in elements %}
      "{{ loop.index }}": {
        "location": "{{ element.location }}",
        "data": {
          "co2": {{ element.co2 }}
        }
      }{% if not loop.last %},{% endif %}
    {% endfor %}
    }
}
""")


def write_json(results, frameNum, frameShape):
    elements = []
    for result in results:
        for box in result.boxes:
            elements.append({"location": np.squeeze(
                box.xyxyn.cpu().numpy()).tolist(), "co2": 0})

    data = {
        "quantity": len(results[0].boxes),
        # "counter": datetime.now(),
        "counter": frameNum,
        "scale": f"({frameShape[0]},{frameShape[1]})",
        "type": "topLeft",
        "humidity": 0,
        "temperature": 0,
        "co2": 0,
        "elements": elements
    }
    json_str = template.render(data)
    json_data = json.loads(json_str)
    return json_data


def track_frame(model, frame, frameNum):
    results = model.track(frame, show=False, show_labels=False, show_conf=False,
                          tracker="bytetrack.yaml", conf=0.1, persist=True, device='cpu')

    ## TO-DO: Implement custom tracking code, currently reviewing literature about methods to calculate ##

    return results
