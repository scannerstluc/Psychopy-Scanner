import os
from abc import ABC, abstractmethod
from datetime import datetime
from psychopy import event

import serial


class Parente(ABC):
    def preprocessing_tsv(self, filename):
        output_dir = 'Fichiers_output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        current_date = datetime.now().strftime("%Y-%m-%d")
        run_number = 1
        filename_prefix = f"{current_date}_{filename.split('.')[0]}"
        existing_files = [f for f in os.listdir(output_dir) if f.startswith(filename_prefix) and 'run' in f]
        if existing_files:
            runs = [int(f.split('run')[-1].split('.')[0]) for f in existing_files if 'run' in f]
            if runs:
                run_number = max(runs) + 1
        filename = os.path.join(output_dir, f"{filename_prefix}_run{run_number}.tsv")
        return filename


    def wait_for_trigger(self, port='COM3', baudrate=9600, trigger_char='s'):
        if port == None:
            event.waitKeys()
        else:
            with serial.Serial(port, baudrate=baudrate) as ser:
                trigger = ser.read().decode('utf-8')
                while trigger != trigger_char:
                    trigger = ser.read().decode('utf-8')
                print("Trigger received")


