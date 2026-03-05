import numpy as np


class GlobalIdentityManager:

    def __init__(self, threshold=0.75):

        self.database = {}
        self.next_id = 1
        self.threshold = threshold


    def cosine(self, a, b):

        return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))


    def assign(self, embedding):

        best_id = None
        best_score = 0

        for gid, emb in self.database.items():

            score = self.cosine(embedding, emb)

            if score > best_score:
                best_score = score
                best_id = gid

        if best_score > self.threshold:
            return best_id

        gid = self.next_id
        self.database[gid] = embedding
        self.next_id += 1

        return gid