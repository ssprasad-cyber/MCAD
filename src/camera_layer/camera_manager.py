class CameraManager:
    def __init__(self, cameras):
        self.cameras = cameras

    def read_all(self):
        packets = []
        for cam in self.cameras:
            data = cam.read()
            if data is not None:
                packets.append(data)
        return packets

    def release_all(self):
        for cam in self.cameras:
            cam.release()
