
from .samples_cache import data_to_samples
from .repitch import change_pitch


class Note:
    def __init__(self, key, on_vel, sample, gens, mods):
        self.sample_data = data_to_samples(sample.data)
        self.key = key
        self.on_vel = on_vel
        self.gens = gens
        self.mods = mods

        print("gens")
        for g in self.gens:
            print(">",g,self.gens[g])

        print("\n\nmods")
        for m in self.mods:
            print(">",m)

    # def
