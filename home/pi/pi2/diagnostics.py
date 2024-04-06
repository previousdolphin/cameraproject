import logging
import time
from flask import jsonify

class DiagnosticsLogger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.logger = logging.getLogger('diagnostics')
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.frame_processing_times = []

    def start_logging(self):
        self.logger.info("Diagnostics logging started.")

    def stop_logging(self):
        self.logger.info("Diagnostics logging stopped.")

    def log_frame_processing_time(self):
        current_time = time.time()
        self.frame_processing_times.append(current_time)

    def get_logs(self):
        logs = []
        with open(self.log_file, 'r') as file:
            for line in file:
                logs.append(line.strip())
        return jsonify(logs=logs, frame_processing_times=self.frame_processing_times)
