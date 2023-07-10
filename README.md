
# Smart Farm: Livestock Tracking

This project aims to provide a smart farm solution for livestock tracking. It utilizes a three-tier approach involving data collection from sensors installed in the ranch, data processing and packaging in JSON format, and data visualization for live tracking and monitoring of the animals.

## Features

- Real-time tracking and monitoring of livestock in a farm
- Display of individual animal information, including quantity, timestamp, humidity, temperature, and total CO2 emission
- Unique color assignment for each animal for easy identification

## Technologies Used

- Python
- Flask (web framework)
- MQTT (message queuing protocol)
- HTML/CSS/JavaScript (for the frontend visualization)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/taugroup/Smart-Farm-Frontend.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:

   ```bash
   python frontend/app.py & backend/backend.py -vr backend/cow_move.mp4
   ```

4. Access the application in your web browser at `http://localhost:5000`.

## Usage

1. Ensure that the MQTT server is running and receiving data from the sensors.

2. Open the web browser and navigate to `http://localhost:5000`.

3. The animals in the pen will be displayed in the green box.

4. Hover over each animal to view their respective information received from the sensors.

## Customization

- You can customize the MQTT server connection details in the `app.py` file.

- To change the visualization layout or style, modify the HTML/CSS/JavaScript code in the `templates/index.html` file.
