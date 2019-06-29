import ine_python as ine
from matplotlib import pyplot as plt

# plt.ion()
api = ine.INE()
ipc = api.get_ipc()
ipc.plot()
plt.show()

