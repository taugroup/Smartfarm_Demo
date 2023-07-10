from jinja2 import Template
import random
import json

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

def data_generator(id=0, num_object=5):
    size_x = 100
    size_y = 100
    elements = []
    for _ in range(num_object):  # generate 5 elements
        x = random.randint(0, size_x)
        y = random.randint(0, size_y)
        co2 = random.randint(1, 3)  # random co2 value between 1 and 3
        elements.append({"location": f"({x},{y})", "co2": co2})

    data = {
        "quantity": len(elements),
        "counter": id,
        "scale": f"({size_x}x{size_y})",
        "type": "topLeft",
        "humidity": random.randint(0, 100),
        "temperature": random.randint(0, 100),
        "co2": random.randint(0, 100),
        "elements": elements
    }
    json_str = template.render(data)
    json_data = json.loads(json_str)
    return json_data

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    json_data = []
    for i in range(100):
        json_data.append(data_generator(id=i, num_object=5))

    with open('output.json', 'w') as f:
        json.dump(json_data, f, indent=4)
