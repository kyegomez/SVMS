from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
from loguru import logger
from scipy.signal import chirp, find_peaks


class SonarVisionMappingSystem:
    """
    Initialize the SonarVisionMappingSystem.

    Args:
        fs (int): Sampling frequency in Hz.
        duration (float): Duration of the chirp signal in seconds.
        f0 (int): Starting frequency of the chirp signal in Hz.
        f1 (int): Ending frequency of the chirp signal in Hz.
        num_directions (int): Number of horizontal directions to scan.
        elevation_angles (int): Number of vertical angles to scan.
    """
    def __init__(
        self,
        fs: int = 44100,
        duration: float = 0.5,
        f0: int = 20000,
        f1: int = 20000,
        num_directions: int = 36,
        elevation_angles: int = 9,
    ) -> None:
        self.fs = fs
        self.duration = duration
        self.f0 = f0
        self.f1 = f1
        self.num_samples = int(fs * duration)
        self.num_directions = num_directions
        self.elevation_angles = elevation_angles
        self.signal = self.generate_chirp_signal()
        self.responses: List[np.ndarray] = []
        self.distances: List[Tuple[np.ndarray, float, float]] = []
        self.horizontal_angles = np.linspace(
            0, 2 * np.pi, num_directions, endpoint=False
        )
        self.vertical_angles = np.linspace(
            -np.pi / 4, np.pi / 4, elevation_angles
        )

    def generate_chirp_signal(self) -> np.ndarray:
        """
        Generate a chirp signal.

        Returns:
            np.ndarray: The generated chirp signal.
        """
        t = np.linspace(0, self.duration, self.num_samples)
        signal = chirp(
            t,
            f0=self.f0,
            f1=self.f1,
            t1=self.duration,
            method="linear",
        )
        return signal

    def record_response(self) -> np.ndarray:
        """
        Record the response signal.

        Returns:
            np.ndarray: The recorded response signal.
        """
        response = sd.playrec(
            self.signal, self.fs, channels=1, dtype="float64"
        )
        sd.wait()
        return response.flatten()

    def process_signal(self, response: np.ndarray) -> np.ndarray:
        """
        Process the recorded response signal.

        Args:
            response (np.ndarray): The recorded response signal.

        Returns:
            np.ndarray: The calculated distances.
        """
        corr = np.correlate(response, self.signal, mode="full")
        corr = corr[len(corr) // 2 :]

        peaks, _ = find_peaks(corr, height=0.1 * np.max(corr))
        distances = (
            (peaks / self.fs) * 343 / 2
        )  # Calculate distance (343 m/s is the speed of sound)
        return distances

    def collect_data(self) -> None:
        """
        Collect data by scanning different angles and recording responses.
        """
        for v_angle in self.vertical_angles:
            for h_angle in self.horizontal_angles:
                response = self.record_response()
                distances = self.process_signal(response)
                self.responses.append(response)
                self.distances.append((distances, h_angle, v_angle))
                logger.info(f"Collected data for h_angle={h_angle}, v_angle={v_angle}")

    def plot_3d_mapping(self) -> None:
        """
        Plot the 3D sonar mapping.
        """
        if not self.distances:
            raise ValueError(
                "No distances calculated. Please collect data first."
            )

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        xs, ys, zs = [], [], []
        for distances, h_angle, v_angle in self.distances:
            for distance in distances:
                x = distance * np.cos(v_angle) * np.cos(h_angle)
                y = distance * np.cos(v_angle) * np.sin(h_angle)
                z = distance * np.sin(v_angle)
                xs.append(x)
                ys.append(y)
                zs.append(z)

        ax.scatter(xs, ys, zs, c="b", marker="o")
        ax.set_xlabel("X (meters)")
        ax.set_ylabel("Y (meters)")
        ax.set_zlabel("Z (meters)")
        ax.set_title("3D Sonar Mapping")
        plt.show()

    def run(self) -> None:
        """
        Run the SonarVisionMappingSystem.
        """
        logger.info("Starting SonarVisionMappingSystem")
        self.collect_data()
    
        logger.info("Data collection completed")
        logger.info("Plotting 3D mapping")
        self.plot_3d_mapping()
        logger.info("SonarVisionMappingSystem completed")
