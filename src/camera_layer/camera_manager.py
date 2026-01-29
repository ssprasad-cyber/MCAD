class CameraManager:
    def __init__(self, cameras):
        self.cameras = cameras

    def read_all(self):
        packets = []
        for cam in self.cameras:
            pkt = cam.read()
            if pkt is not None:
                packets.append(pkt)
        return packets

    def release_all(self):
        for cam in self.cameras:
            cam.release()
