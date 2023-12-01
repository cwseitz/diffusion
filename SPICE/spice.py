import numpy as np
import matplotlib.pyplot as plt
import torch
from BaseSMLM.generators import *
from DeepSMLM.models import Ring_Rad1_K5_SPAD
from SPICE.mcmc import run_langevin_dynamics
from scipy.stats import poisson

class SPICEG:
    def __init__(self):
        pass
        
    def Theta0(self,bstar,M):
        """Rejection sampling for P(theta0|B,M)"""
        rows,cols = bstar.shape
        U = np.random.uniform(size=(rows,cols))
        Z = np.zeros_like(U)
        Z[U < bstar] = 1
        num_objects = np.sum(Z).astype(int)
        if num_objects > M:
            idx = np.argwhere(Z)
            x = np.arange(0,num_objects,1)
            to_remove = np.random.choice(x,size=num_objects-M,replace=False)
            ridx = idx[to_remove,:]
            Z[ridx[:, 0], ridx[:, 1]] = 0
        theta = np.zeros((2,M))
        z = 0.25*np.argwhere(Z > 0).T
        theta[:2,:] = z
        theta_ = np.ones_like(theta)
        theta_[:,0] *= 0.92; theta[:,1] *= 1000
        theta0 = np.concatenate([theta,theta_],axis=0)
        return theta0
        
    def CNN(self):
        """Models P(B|S)"""
        cnn_config = {'thresh_cnn':20,'radius':4,'pixel_size_lateral':108.3}
        model = Ring_Rad1_K5_SPAD(cnn_config)
        adu = adu[np.newaxis,np.newaxis,:,:]
        spots,bstar = model.forward(adu)
        
    def Langevin(self):
        """Models P(theta|theta0)"""
        adu = np.squeeze(adu)
        lr = torch.tensor(np.array([1e-9,1e-9,0.0,0.0])) #only update x,y
        theta,loglikes = run_langevin_dynamics(adu,initial_params=theta_init,lr=lr,
                                               num_samples=1000,warmup_steps=100,print_every=100)
        print(f'Average log likelihood: {np.mean(loglikes)}')
        
    def Poisson(self,X):
        """Models P(M|X)"""
        print(X.shape)
        return None
        
    def forward(self,X):
        M = self.Poisson(X)
        #B = self.CNN(X)

       
