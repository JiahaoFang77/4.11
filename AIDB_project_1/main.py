import User_defined_metadata
import Base_tables
import Vedio_to_image 
import platform
import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


if __name__ == "__main__":
    tlist = []
    for i in range(20):
        T1 = time.process_time()
        Vedio_to_image.vedio_to_image()
        Base_tables.base_table()
        User_defined_metadata.User_defined_metadata()
        T2 = time.process_time()
        tlist.append((T2-T1))

    data = tlist
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(data, bins=10, density=True)
    mu, sigma = stats.norm.fit(data)
    x = np.linspace(min(bins), max(bins), 100)
    y = stats.norm.pdf(x, mu, sigma)
    ax.plot(x, y)
    ax.set_xlabel('Time(s)')
    ax.set_ylabel('Simulation')
    ax.set_title('Simulation vs. time')
    plt.show()