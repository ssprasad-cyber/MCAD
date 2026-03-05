from queue import Full
from utils.pipeline_queue import frame_queue
from edge_processing.frame_capture.frame_packet import FramePacket


def camera_worker(manager):

    while True:

        packets = manager.read_all()

        for pkt in packets:

            if isinstance(pkt, FramePacket):
                frame_packet = pkt
            else:
                frame_packet = FramePacket(
                    camera_id=pkt["camera_id"],
                    frame=pkt["frame"],
                    timestamp=pkt["timestamp"]
                )

            try:
                frame_queue.put_nowait(frame_packet)
            except Full:
                try:
                    frame_queue.get_nowait()
                except Exception:
                    pass

                try:
                    frame_queue.put_nowait(frame_packet)
                except Exception:
                    pass