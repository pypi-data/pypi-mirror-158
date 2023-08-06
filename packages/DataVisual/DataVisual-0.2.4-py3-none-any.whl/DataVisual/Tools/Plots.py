import matplotlib.pyplot as plt
import numpy    as np
from numpy      import pi, cos, sin, abs
from mayavi     import mlab
from tvtk.tools import visual
from tvtk.api   import tvtk
from pyface.api import GUI

from DataVisual.Tools.utils       import Sp2Cart, ToList, FormatStr, FormatString
from DataVisual.Tools.Config      import *
from DataVisual.Tools.PlotsUtils  import *


def Unstructured(**kwargs):
    if kwargs['Mode'] == 'Absolute':
        kwargs.pop('Mode')
        return UnstructuredAbs(**kwargs)

    if kwargs['Mode'] == 'Amplitude':
        kwargs.pop('Mode')
        return UnstructuredAmplitude(**kwargs)



def Structured(**kwargs):
    if kwargs['Mode'] == 'Absolute':
        kwargs.pop('Mode')
        return StructuredAbs(**kwargs)

    if kwargs['Mode'] == 'Amplitude':
        kwargs.pop('Mode')
        return StructuredAmplitude(**kwargs)



def UnstructuredAbs(Mesh, Scalar = None, Name = '', Figure  = None):

    Figure = mlab.figure(figure=None, size=(600,300))
    visual.set_viewer(Figure)

    if Scalar is None: Scalar = Mesh.Phi.Radian*0+1

    x, y, z = Sp2Cart(Scalar.flatten(),
                      Mesh.Phi.Radian.flatten(),
                      Mesh.Theta.Radian.flatten())

    AddUnitAxes(Figure=Figure, Scale=1., Origin=(0,0,-1.5))

    AddUnitSphere(Num=50, Radius=1, Origin=(0,0,0), Figure=Figure)

    im0 = mlab.points3d(x,
                        y,
                        z,
                        abs(Scalar),
                        mode       = 'sphere',
                        scale_mode = 'none',
                        colormap   = CMAP)

    mlab.colorbar(object           = im0,
                  label_fmt        = "%.0e",
                  nb_labels        = 5,
                  title            = 'Real part',
                  orientation      = 'horizontal' )




def UnstructuredAmplitude(Mesh, Scalar = None, Name = ''):
    Figure = mlab.figure(figure=None, size=(600,300))

    visual.set_viewer(Figure)

    if Scalar is None: Scalar = Mesh.Phi.Radian.flatten()*0+1

    x, y, z = Sp2Cart(Scalar,
                      Mesh.Phi.Radian.flatten(),
                      Mesh.Theta.Radian.flatten())

    dic = {'Real'     : (-3, np.real, 'horizontal'),
           'Imaginary': (+3, np.imag, 'vertical')}

    for keys, (val, func, ax) in dic.items():
        Origin = (val, 0, 0)

        AddUnitAxes(Figure=Figure, Scale=2., Origin=Origin)

        mlab.text3d(val,
                    Origin[1],
                    3,
                    keys,
                    scale = 0.5)

        AddUnitSphere(Num               = 50,
                      Radius            = 1.,
                      Origin            = Origin,
                      Figure            = Figure)

        im0 = mlab.points3d(Mesh.CartCoord[0]+Origin[0],
                            Mesh.CartCoord[1]+Origin[1],
                            Mesh.CartCoord[2]+Origin[2],
                            func(Scalar),
                            mode        = 'sphere',
                            scale_mode  = 'none',
                            colormap    = CMAP)

        mlab.colorbar(object            = im0,
                      label_fmt         = "%.0e",
                      nb_labels         = 5,
                      title             = f'{keys} part',
                      orientation       = ax )


        WavenumberArrow(Figure, Origin=(val,0,-3), Scale=1)

    return Figure




def StructuredAbs(Scalar,
                  Phi,
                  Theta,
                  Name         = '',
                  Polarization = None):

    Figure = mlab.figure(figure=None, size=(600,300))
    visual.set_viewer(Figure)

    O = (0,0,0)
    O1 = (0,0,-2)

    x, y, z = Sp2Cart(Scalar/np.max(Scalar)*4, Phi, Theta)

    AddUnitAxes(Figure=Figure, Scale=5, Origin=O, ScaleTube=0.7)

    im = mlab.mesh(x, y, z-np.min(z), colormap='viridis', figure=Figure)

    mlab.mesh(x, y, z-np.min(z), representation='wireframe', color=(0, 0, 0), line_width=0.1, figure=Figure, opacity=0.05)

    mlab.colorbar(object      = im,
                  label_fmt   = "%.0e",
                  nb_labels   = 5,
                  title       = 'Normalized scale',
                  orientation = 'horizontal' )

    if Polarization is not None:
        AddSource(Figure, O1, Polarization, Scale=1)

    return Figure





def StructuredAmplitude(ETheta,
                         EPhi,
                         Phi,
                         Theta,
                         Name         = '',
                         Polarization = None,
                         Source       = None):

    Figure = mlab.figure(figure=None, size=(600,300))
    visual.set_viewer(Figure)

    O = (0,0,0)
    O1 = (-2,0,+2)
    O2 = (+2,0,+2)

    Abs = np.sqrt( ETheta.__abs__()**2 + EPhi.__abs__()**2 )
    Abs /= np.max(Abs)

    x, y, z = Sp2Cart(np.abs(Abs)*3, Phi, Theta)

    AddUnitAxes(Figure=Figure, Scale=2, Origin=(-2,0,0), ScaleTube=0.7)

    AddUnitAxes(Figure=Figure, Scale=2, Origin=(+2,0,0), ScaleTube=0.7)

    im0 = mlab.mesh(x-2, y, z, scalars=np.real(ETheta), colormap='RdBu', figure=Figure)
    im1 = mlab.mesh(x+2, y, z, scalars=np.real(EPhi), colormap='RdBu', figure=Figure)

    mlab.mesh(x-2, y, z, representation='wireframe', color=(0, 0, 0), line_width=0.1, figure=Figure, opacity=0.05)
    mlab.mesh(x+2, y, z, representation='wireframe', color=(0, 0, 0), line_width=0.1, figure=Figure, opacity=0.05)



    mlab.colorbar(object      = im1,
                  label_fmt   = "%.0e",
                  nb_labels   = 5,
                  title       = 'Electric field',
                  orientation = 'vertical' )

    if Polarization is not None:
        AddSource(Figure, (-2,0,-2), Polarization, Scale=1)
        AddSource(Figure, (+2,0,-2), Polarization, Scale=1)


    return Figure



def _StructuredAmplitude(Scalar,
                        Phi,
                        Theta,
                        Name         = '',
                        Polarization = None,
                        Source       = None):

    Figure = mlab.figure(figure=None, size=(600,300))
    visual.set_viewer(Figure)

    x, y, z = Sp2Cart(Phi*0+1, Phi, Theta)

    dic = {'Real'     : (-3, np.real, 'horizontal'),
           'Imaginary': (+3, np.imag, 'vertical')}

    for keys, (val, func, ax) in dic.items():
        Origin = (val, 0, 0)

        AddUnitAxes(Figure=Figure, Origin=Origin, Scale=2)

        mlab.text3d(Origin[0], Origin[1], 5, keys, scale=0.5)

        AddSource(Figure, (val,0,-3), Polarization, Scale=1.1)

        im0 = mlab.points3d(x+val,
                            y,
                            z,
                            func(Scalar),
                            mode       = 'sphere',
                            scale_mode = 'none',
                            colormap   = CMAP,
                            opacity    = 1)


        mlab.colorbar(object           = im0,
                      label_fmt        = "%.0e",
                      nb_labels        = 5,
                      title            = f'{keys} part',
                      orientation      = ax )

    return Figure


def PlotConfiguration(Detector, Scatterer):
    """Still experimental"""
    from tvtk.tools import visual
    from tvtk.api import tvtk
    from numpy import sqrt

    Figure = mlab.figure(figure = 'Optical configuration', size=(600,300))
    visual.set_viewer(Figure)

    Origin = [0,0,0]

    AddUnitSphere(Num=50, Radius=0.1, Origin=(0,0,0), Figure=Figure)

    AddUnitAxes(Scale=3, Origin=(0,0,0), Figure=Figure)

    AddUnitAxes(Scale=0.8, Origin=(0,0,-2), Figure=Figure, Label=False, ScaleTube=0.5)

    ElectricFieldArrow(Figure=Figure, Origin=(0,0,-2), Pol=0, Scale=1)

    Ydir = np.sin(Detector.PhiOffset)
    Xdir = np.sin(Detector.GammaOffset)

    Direction = np.array([Xdir,Ydir,-1])

    dist = sqrt(Direction[0]**2 + Direction[1]**2 + Direction[2]**2)

    Height = 2.0

    Origin = Origin - Direction/dist*Height/2.5


    SPF = Scatterer.SPF(100)
    SPF['SPF'] = SPF['SPF']/np.max(SPF['SPF'])*2

    x, y, z = Sp2Cart(SPF['SPF'], SPF['Phi'], SPF['Theta'] )

    im = mlab.mesh(x, y, z, colormap='viridis', figure=Figure)

    PlotCone(Origin     = Origin,
             Radius     = Detector.NA*Height,
             Height     = Height,
             Resolution = 100,
             Figure     = fig,
             Direction  = Direction)

    mlab.view(azimuth=0, elevation=180, distance=None)



def StokesPlot(I,
               Q,
               U,
               V,
               Phi,
               Theta,
               Name         = '',
               Polarization = None,
               Figure       = None):

    Figure = mlab.figure(figure=Name, size=(600,300))
    visual.set_viewer(Figure)

    dic = {'I': (I, -6),
           'Q': (Q, -2),
           'U': (U, +2),
           'V': (V, +6)}

    for keys, (stokes, val) in dic.items():
        Origin = (val, 0, -3)

        x, y, z = Sp2Cart(Phi*0+1, Phi, Theta)
        im = mlab.points3d(x.flatten() + Origin[0],
                           y.flatten(),
                           z.flatten(),
                           stokes.flatten()/np.max(I),
                           colormap     = CMAP,
                           figure       = Figure,
                           mode         = 'sphere',
                           scale_mode   = 'none')

        mlab.text3d(Origin[0], Origin[1], 3, keys, scale = 0.5)

        lut_manager = mlab.colorbar(object      = im,
                                    label_fmt   = "%.0e",
                                    nb_labels   = 5,
                                    title       = 'Normalized scale',
                                    orientation = 'horizontal' )

        lut_manager.data_range = (0, 1)

        if Polarization is not None:
            AddSource(Figure, Origin, Polarization, Scale=1)






def ExperimentPlot(func):

    def wrapper(self, y, x, Polar=False, yLog=False, xLog=False, rLog=False, Normalize=False):

        figure = plt.figure(figsize=(10,5))
        if Polar:
            ax = figure.add_subplot(111, projection='polar')
            if rLog: ax.set_rscale('symlog')
        else:
            ax = figure.add_subplot(111)
            if xLog: ax.set_xscale('log')
            if yLog: ax.set_yscale('log')
            ax.grid()

        func(self, x=x, y=y, Polar=Polar, Normalize=Normalize, figure=figure, ax=ax)

        ax.legend(loc='upper left', prop={'family': 'monospace', 'size':7})

        plt.show()
        return figure

    return wrapper






# -
