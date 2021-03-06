import numpy as np

intensity = lambda x: np.dot(x, [0.299, 0.587, 0.114])

def img_norm_diff(images):
    '''
    Returns normalized image difference for visualization
    
    Keyword arguments:
        images -- list-like structure containing two images
    '''
    diff = np.abs(intensity(images[0]) - intensity(images[1]))
    diff_max = np.max(diff)
    if diff_max != 0:
        diff /= diff_max
    return diff
    
def flow_norm_diff(flows):
    '''
    Normalized length of flow vector difference for visualization
    Returns angle in 3D between (u0, v0, 1) and (u1, v1, 1)
    
    Keyword arguments:
        flows -- list-like structure containing two optical flows
    '''
    diff = flows[1] - flows[0]
    diff_mod = np.sqrt(diff[:, :, 0] ** 2 + diff[:, :, 1] ** 2)
    max_mod = np.max(diff_mod)
    if max_mod != 0:
        diff_mod /= max_mod
    return diff_mod

def ang_error(flows):
    '''
    Angular error
    Returns angle in 3D between (u0, v0, 1) and (u1, v1, 1)
    where (u0, v0) and (u1, v1) are original optical flow vectors
    
    Keyword arguments:
        flows -- list-like structure containing two optical flows
    '''
    norm_flows = []
    for i in xrange(2):
        # add elems containing ones along last axis and get a flow with 3d vectors
        flow3d = np.append(flows[i], np.ones(flows[i].shape[:-1] + (1,)), axis = 2)
        
        norm = np.linalg.norm(flow3d, axis = 2)
        # broadcasting doesn't work with np.divide so repeat the array
        # norm = np.stack([norm] * 3, axis = 2) # obsolete
        norm = np.repeat(norm[:, :, np.newaxis], repeats = 3, axis = -1)
        # normalize flow with 3d vectors
        # np.divide instead of "/" to check for zeros on-the-fly
        norm_flow = np.divide(flow3d, norm, out = np.zeros_like(flow3d), where = (norm != 0))
        norm_flows.append(norm_flow)
    dot = np.sum(np.multiply(norm_flows[0], norm_flows[1]), axis = 2) # dot product
    dot /= np.max(np.abs(dot)) # normalize dot product
    ang = np.arccos(dot)
    return np.mean(ang)

def epe_error(flows):
    '''
    End-point error
    Returns mean length of flow vector difference
    
    Keyword arguments:
        flows -- list-like structure containing two optical flows
    '''
    diff = flows[1] - flows[0]
    diff_mod = np.sqrt(diff[:, :, 0] ** 2 + diff[:, :, 1] ** 2)
    return np.mean(diff_mod)

def ssd_error(images):
    '''
    Returns sum of squared differences between 2 images
    
    Keyword arguments:
        images -- list-like structure containing 2 images
    '''
#    return np.sum((intensity(images[0].astype(np.float) / 255) -
#                  intensity(images[1].astype(np.float) / 255)) ** 2)
    channels = imgs[0].shape[2]
    res = np.sum((images[0].astype(np.float) / 255 - images[1].astype(np.float) / 255) ** 2) / channels
    return res

def rms_error(images):
    '''
    Returns root mean square difference between 2 images
    
    Keyword arguments:
        images -- list-like structure containing 2 images
    '''
#    return np.sqrt(np.mean((intensity(images[0].astype(np.float) / 255) -
#                   intensity(images[1].astype(np.float) / 255)) ** 2))
    res = np.sqrt(np.mean((images[0].astype(np.float) / 255 - images[1].astype(np.float) / 255) ** 2))
    return res