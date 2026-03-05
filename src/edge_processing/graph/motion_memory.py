class MotionMemory:

    def __init__(self):
        self.prev = {}

    def compute(self, gid, center):

        cx, cy = center

        if gid in self.prev:
            px, py = self.prev[gid]
            vx = cx - px
            vy = cy - py
        else:
            vx, vy = 0, 0

        self.prev[gid] = (cx, cy)

        return vx, vy
    