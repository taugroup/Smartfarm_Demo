# Smart Farm: Livestock Tracking

This project aims to provide a smart farm solution for livestock tracking. It utilizes a three-tier approach involving data collection from sensors installed in the ranch, data processing and packaging in JSON format, and data visualization for live tracking and monitoring of the animals.

## Features

- Real-time tracking and monitoring of livestock on a farm
- Display of individual animal information, including other sensors deployed.
- Unique color assignment for each animal for easy identification

## Technologies Used

- Python: The main programming language used for developing the smart farm system.

- Flask (web framework): Flask is used to build the web application for visualizing the tracked livestock.

- MQTT (message queuing protocol): MQTT is used as the communication protocol for transmitting data between the sensors and the visualization system.

- HTML/CSS/JavaScript (for the frontend visualization): These web technologies are used to create an interactive and user-friendly interface for visualizing livestock data.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/taugroup/Smartfarm_Demo.git
   ```

2. Create a Python eirtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate
   
3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run both the backend and frontend applications:

   ```bash
   python frontend/app.py & backend/backend.py -vr backend/cow_move.mp4
   ```

5. Access the application in your web browser at `http://localhost:5000`.

## Usage

1. Ensure that the MQTT server is running and receiving data from the sensors.

2. Open the web browser and navigate to `http://localhost:5000`.

3. The animals in the pen will be displayed in the green box.

4. Hover over each animal to view the respective information received from the sensors.

## Customization

- You can customize the MQTT server connection details in the `app.py` file.

- To change the visualization layout or style, modify the HTML/CSS/JavaScript code in the `templates/index.html` file.
