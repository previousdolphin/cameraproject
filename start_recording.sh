#!/bin/bash

duration=$1
python /home/pi/project/capture_images.py $duration
```

4. Shell Script on Raspberry Pi 1 (stop_recording.sh):
```bash
#!/bin/bash

python /home/pi/project/capture_images.py
```

5. Modified 3D Model Creation Script on Raspberry Pi 2 (create_3d_model.py):
```python
import time

def create_model():
    # Create 3D model from depth maps
    # ...

    # Save the generated 3D model
    # ...

# Main program
while True:
    if depth_maps_available():
        create_model()
    time.sleep(1)
