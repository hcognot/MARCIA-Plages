# from marcia.mask import Mask
import matplotlib.pyplot as plt
from maskSigma import Mask

cm = Mask('examples/Data/lead_ore_','.bmp','examples/Data/Mask.xlsx')
cm.load_table()
cm.datacube_creation()
cm.Elements
# cm.get_hist('Pb')
cm.load_table()
cm.mineralcube_creation()
cm.Minerals
# cm.get_mask('Galene')
cm.plot_mineral_mask()








