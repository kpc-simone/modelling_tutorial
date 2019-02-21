import nengo
import numpy as np
import scipy as sp
import sys
from scipy import signal
import matplotlib.pyplot as plt

#nengo GUI simulator
###################################
model = nengo.Network()
with model:
###################################
    
    #########################
    #ENVIRONMENTAL STIMULI
    #########################

    exp_rate = 0.5 #vary from 0.1 to 0.9
    def square(t):
        return exp_rate * ( sp.signal.square (2*np.pi*0.1*(t-1), duty = 0.5) + 1 ) / 2
    
    stim = nengo.Node(square)
    stim.label='expansion rate'
    
    sc = nengo.Ensemble(n_neurons=400,
                            radius=1,
                            dimensions=1,
                            )
    
    thal = nengo.Ensemble(n_neurons=600,
                            radius=1,
                            dimensions=1,
                            )    
                            
    la = nengo.Ensemble(n_neurons=400,
                            radius=1,
                            dimensions=1)
                            
    bma = nengo.Ensemble(n_neurons=400,
                            radius=1,
                            dimensions=1)                        
    
    bnst = nengo.Ensemble(n_neurons=200,
                            radius=2,
                            dimensions=1)
                            
    cea = nengo.Ensemble(n_neurons=200,
                            radius=1,
                            dimensions=1)
                            
    peri_pvn = nengo.Ensemble(n_neurons=200,
                                radius=1,
                                dimensions=1)
    
    ahn = nengo.Ensemble(n_neurons=600,
                            radius=5,
                            dimensions=1, 
                            encoders=nengo.dists.Choice([[1]]),
                            intercepts=nengo.dists.Uniform(0,1)
                            )
                            
    vmh = nengo.Ensemble(n_neurons=600,
                            radius=10,
                            dimensions=1)
    
    dmh = nengo.Ensemble(n_neurons=200,
                            radius=1,
                            dimensions=1)  
    
    pvn_neurons=200
    pvn_crh = nengo.Ensemble(n_neurons=pvn_neurons,
                            radius=1,
                            dimensions=1,
                            encoders=nengo.dists.Choice([[1]]),
                            intercepts=nengo.dists.Uniform(0,1)
                            )  
                        
    dpag = nengo.Ensemble(n_neurons=800,
                            radius=5,
                            dimensions=1, 
                            )
    
    vpag_gaba = nengo.Ensemble(n_neurons=200,
                            radius=1,
                            dimensions=1)
                            
    vpag_glu = nengo.Ensemble(n_neurons=200,
                            radius=1,
                            dimensions=1)
    
    medulla = nengo.Ensemble(n_neurons=200,
                            radius=1,
                            dimensions=1)
                            
    pbn = nengo.Ensemble(n_neurons=200,
                            radius=5,
                            dimensions=1)
                            
    lh = nengo.Ensemble(n_neurons=200,
                            radius=1,
                            dimensions=1)
    
    #behaviors 0: other, 1: escape                        
    motor = nengo.Ensemble(n_neurons=600,
                            radius=5,
                            dimensions=2,
                            #encoders=nengo.dists.Choice([[1,1]]),
                            #intercepts=nengo.dists.Uniform(0,1)
                            )
                       
    #########################
    #VISUAL THREAT DETECTION
    #########################
    
    actual_synapse = 0.15
    b_desired = 1
    a_desired = 0.0001
    
    def input_function(u):
        return u * b_desired * actual_synapse
        
    def recurrent_function(x):
        return ( x * a_desired * actual_synapse) + x 
    
    def multiply(y):
        u,x = y
        return y[0]*y[1]
    
    #relay for U to next ens2
    nengo.Connection(sc[0],thal[0]) #U
    nengo.Connection(thal[0],la[0]) #rate
    
    ###########################
    #MOTOR COMMAND PRODUCTION
    ###########################
    array_inh=np.ones((200,1))*(-10)
    array_motor_inh = np.ones((600,1))*(-5000)
    
    #noise that makes it do something else
    other_promote = nengo.Node(1)
    nengo.Connection(other_promote,motor[0])
    
    #glutamatergic projection from vpag promotes freezing via medulla
    #tovote et al 2016
    nengo.Connection(vpag_glu, medulla)
    nengo.Connection(medulla, motor.neurons, transform=array_motor_inh)
    
    #excitatory projection from vpag to medulla is activated via 
    #disinhibitory mechanism with local GABAergic cells
    #characterized by tonic activity in resting state
    #tovote et al 2016
    tonic_gaba = nengo.Node(0.1)
    nengo.Connection(tonic_gaba, vpag_gaba)
    nengo.Connection(vpag_gaba, vpag_glu.neurons, transform=array_inh)
    
    #ASSUMPTION
    #hypothesized competitive, leaky integrators in dpag, vmh, and ahn
    #with distinct time constants and dynamic ranges
    #accounts for data from kunwar 2015 and predator imminence
    tau_dpag = 0.1
    tau_vmh = 0.1
    tau_ahn = 0.01
    
    #canteras 2002: vmh projects to ahn
    nengo.Connection(vmh, ahn, synapse = tau_ahn)

    #ASSUMPTION
    #ahn projects back onto itself
    nengo.Connection(ahn, ahn, synapse = tau_ahn, transform = 0.9)

    nengo.Connection(ahn, vpag_glu)
    
    nengo.Connection(vmh, dpag, synapse = tau_dpag, transform = 0.9)
    nengo.Connection(dpag, vmh, synapse = tau_vmh, transform = 0.9)
    
    #ASSUMPTION 
    #dpag promotes activity bursting
    nengo.Connection(dpag, motor[0]) 
    nengo.Connection(dpag, motor[1])
    
    #dpag inhibits vpag freezing by promoting local GABAergic activity
    #tovote et al 2016
    nengo.Connection(dpag, vpag_gaba, transform = 0.25)
    
    #ASSUMPTION
    #information from vmh, ahn scaled upon projection to 
    #canteras 2002: vmh and ahn both project to dmh
    nengo.Connection(vmh,dmh,transform = 0.2)
    nengo.Connection(ahn,dmh,transform = -0.1)

    #ASSUMPTION
    #canteras 2002: pbn projects to vmh
    nengo.Connection(pbn,vmh)
    
    #canteras 2002 dmh projects to pvn
    nengo.Connection(dmh,pvn_crh)
    
    array_inh_pvn = np.ones((200,1))*(-1)
    nengo.Connection(cea,peri_pvn.neurons,transform=array_inh)
    
    tonic_peripvn = nengo.Node(output=0.1)
    nengo.Connection(tonic_peripvn,peri_pvn)
    nengo.Connection(peri_pvn, pvn_crh.neurons, transform=array_inh_pvn)
    
    #########################
    #SENSORIMOTOR INTEGRATION
    #########################
    
    def compare_to_optimal(x):
        #steep inverted quadratic function of x
        alpha = 0.51
        return 1 - 1 / ( alpha / 2 ) * ( alpha - x ) * ( alpha - x )
    
    nengo.Connection(la[0],bma[0])
    
    nengo.Connection(bma[0], vmh, function=compare_to_optimal) #rate
    nengo.Connection(bma[0], ahn) #rate
    
    #cea promotes freezing via inhibition of vpag GABAergic cells
    #tovote et al 2016
    nengo.Connection(pbn,cea,transform=0.1)
    nengo.Connection(cea,vpag_gaba.neurons, transform=array_inh*0.1)
    nengo.Connection(bma[0], cea) #rate
    
    nengo.Connection(bma[0], bnst) #rate
    nengo.Connection(bnst,pvn_crh.neurons,transform=array_inh_pvn*1.3)
    
    nengo.Connection(pvn_crh,lh)
    nengo.Connection(lh,dpag)

    #########################
    #ASSUMPTIONS
    #########################
    nengo.Connection(stim,pvn_crh,transform=1.0)
    
    #########################
    #EXPERIMENTS
    #########################
    nengo.Connection(stim,sc[0],synapse=actual_synapse)
   
    noci_stim = nengo.Node(0) 
    opto_stim = nengo.Node(0)
    #nengo.Connection(noci_stim,pbn)
    
    #deng 2018
    #dpag stimulation induces (near instantaneous) 
    #flight upon 2-second photostimulation
    
    #freezing accounts for 75% of 1-minute 
    #inter-trial period (approx. 45 s)
    #nengo.Connection(opto_stim, dpag)
    
    #kunwar 2015
    #vmh stimulation causes freezing-> activity burst transition
    #nengo.Connection(opto_stim, vmh, synapse = tau_vmh)