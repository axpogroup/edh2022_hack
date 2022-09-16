import ezdxf
import matplotlib.pyplot as plt

from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

if __name__ == '__main__':
    dxfFilename = '..'
    doc = ezdxf.readfile('data/SWISSBUILDINGS3D_2_0_CHLV95LN02_1070-42.dxf')

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    Frontend(ctx, out).draw_layout(doc.modelspace(), finalize=True)

    fig.show()
    fig.savefig('your.png', dpi=300)
