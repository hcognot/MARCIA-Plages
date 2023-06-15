
from maskSigma import Mask
import concatenexlsx
import matplotlib.pyplot as plt


def tout(atome):
    cm = Mask('examples/Data/lead_ore_','.bmp','examples/Data/Mask.xlsx')

    cm.load_table()
    cm.datacube_creation()

    cm.get_hist(atome)
    print('---------  '+atome+'  ---------')
    reponse = cm.create_hist(atome)
    concatenexlsx.createAtomFile(reponse, 'examples/Data', atome)
    concatenexlsx.createSynthesisFile('examples/Data')

# tout('Al')
# tout('As')
# tout('Ca')
# tout('Cl')
# tout('Cu')
# tout('Fe')
# tout('K')
# tout('Mg')
# tout('Mn')
# tout('Na')
# tout('Pb')
# tout('S')
# tout('Si')
tout('Ti')

plt.show()

