[![Multi-Modality](agorabanner.png)](https://discord.com/servers/agora-999382051935506503)

# Sonar Vision Mapping System

This project aims to recreate the vision mapping system inspired by Batman in "The Dark Knight." The system uses high-frequency sound pulses to create a real-time, three-dimensional map of an environment. It is designed for applications in security, surveillance, and search-and-rescue operations.

## Features

- Emit ultrasonic chirp signals
- Record echoes and process the response
- Calculate distances to objects based on echo timings
- Construct and visualize a 3D point cloud of the environment

## Requirements

- Python 3.6+
- `numpy`
- `sounddevice`
- `scipy`
- `matplotlib`

# Install
```bash
$ pip install svms
```

## Usage
```python

from svms.main import SonarVisionMappingSystem

# Example usage
sonar_system = SonarVisionMappingSystem()
sonar_system.run()

```



This script will emit ultrasonic pulses, record the echoes, and visualize the 3D point cloud of the environment.

## Code Overview

### `SonarVisionMappingSystem` Class

The main functionality is encapsulated in the `SonarVisionMappingSystem` class. Here's a breakdown of the key methods:

- `__init__(self, fs=44100, duration=0.5, f0=20000, f1=20000, num_directions=36, elevation_angles=9)`: Initializes the system with sampling frequency, duration, and frequency range for the chirp signal, along with the number of directions and elevation angles for mapping.

- `generate_chirp_signal(self)`: Generates a chirp signal.

- `record_response(self)`: Emits the chirp signal and records the response.

- `process_signal(self, response)`: Processes the recorded response to find echoes and calculate distances.

- `collect_data(self)`: Collects responses and distances for multiple directions and elevation angles.

- `plot_3d_mapping(self)`: Plots the 3D point cloud of the environment.

- `run(self)`: Runs the complete process of data collection and 3D mapping.

### Example Usage

```python
sonar_system = SonarVisionMappingSystem()
sonar_system.run()
```

## Safety Considerations

The system uses ultrasonic frequencies (20 kHz), which are generally considered safe. However, ensure that the intensity of the emitted pulses is within safe limits, and avoid prolonged exposure to ultrasonic waves.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.