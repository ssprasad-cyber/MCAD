from .frame_buffer import FrameBuffer

class FrameDispatcher:
    def __init__(self, camera_ids, buffer_size=30):
        self.buffers = {
            cam_id: FrameBuffer(buffer_size)
            for cam_id in camera_ids
        }

    def push(self, packet):
        self.buffers[packet.camera_id].push(packet)

    def pull_latest(self):
        output = {}
        for cam_id, buffer in self.buffers.items():
            pkt = buffer.latest()
            if pkt:
                output[cam_id] = pkt
        return output
