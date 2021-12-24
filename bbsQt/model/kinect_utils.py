import numpy as np

ORG_KNT_TYPEs = ["PELVIS", "SPINE_NAVAL", "SPINE_CHEST", "NECK", "CLAVICLE_LEFT", "SHOULDER_LEFT", "ELBOW_LEFT",
                    "WRIST_LEFT", "HAND_LEFT", "HANDTIP_LEFT", "THUMB_LEFT", "CLAVICLE_RIGHT", "SHOULDER_RIGHT", "ELBOW_RIGHT",
                    "WRIST_RIGHT", "HAND_RIFHT", "HANDTIP_RIGHT", "THUMB_LEFT", "HIP_LEFT", "KNEE_LEFT", "ANKLE_LEFT", "ROOT_LEFT",
                    "HIP_RIGHT", "KNEE_RIGHT", "ANKLE_RIGHT", "FOOT_RIGHT", "HEAD", "NOSE", "EYE_LEFT", "EAR_LEFT","EYE_RIGHT", "EAR_RIGHT"]

K2M = {"SHOULDER_LEFT":"l_shoulder",
       "SHOULDER_RIGHT":"r_shoulder",
       "ELBOW_LEFT":"l_elbow", 
       "ELBOW_RIGHT":"r_elbow", 
       "WRIST_LEFT":"l_hand", 
       "WRIST_RIGHT":"r_hand",
       "HIP_LEFT":"l_hip", 
       "HIP_RIGHT":"r_hip", 
       "KNEE_LEFT":"l_knee", 
       "KNEE_RIGHT":"r_knee",
       "ANKLE_LEFT":"l_foot", 
       "ANKLE_RIGHT":"r_foot",
       "NOSE":"head"}

def get_a_skel(tdict, this_person):
    for this_joint in this_person:
        tdict["x"+this_joint[0]] = this_joint[1]
        tdict["y"+this_joint[0]] = this_joint[2]
        
import BBS_pp_utils as bbpp
def kinect2mobile_direct(klist):
    """fills mobile_skeleton array with KINECT_BBS skeleton 
       directly from kinect application
       
       Kinect application passes 
       per-frame list 
           of per-person list 
               of per-skeleton list
       
       KINECT_BBS names are different from 
    """
    
    K2M = {"SHOULDER_LEFT":"l_shoulder",
           "SHOULDER_RIGHT":"r_shoulder",
           "ELBOW_LEFT":"l_elbow", 
           "ELBOW_RIGHT":"r_elbow", 
           "WRIST_LEFT":"l_hand", 
           "WRIST_RIGHT":"r_hand",
           "HIP_LEFT":"l_hip", 
           "HIP_RIGHT":"r_hip", 
           "KNEE_LEFT":"l_knee", 
           "KNEE_RIGHT":"r_knee",
           "ANKLE_LEFT":"l_foot", 
           "ANKLE_RIGHT":"r_foot",
           "NOSE":"head"} # Assume Kinect nose == common head

    mdtype = bbpp.get_dtypes(skeleton="COMMON")
    marr = np.zeros(len(klist), dtype=mdtype)
    
    # Initialize temporary dict
    tdict = dict([(prx+name, 0) for name in ORG_KNT_TYPEs for prx in ["x", "y"]])

    for iframe, this_frame in enumerate(klist):
        for this_person in this_frame:
            get_a_skel(tdict, this_person)
            
            # Assume neck is the mid point of shoulders
            marr[iframe]['xneck'] = (tdict['xSHOULDER_LEFT'] + tdict['xSHOULDER_RIGHT'])/2
            marr[iframe]['yneck'] = (tdict['ySHOULDER_LEFT'] + tdict['ySHOULDER_RIGHT'])/2

            marr[iframe]['xpelvis'] = (tdict['xHIP_LEFT'] + tdict['xHIP_RIGHT'])/2
            marr[iframe]['ypelvis'] = (tdict['yHIP_LEFT'] + tdict['yHIP_RIGHT'])/2

            for common_field in K2M:
                for prefix in ['x','y']:
                    marr[prefix+K2M[common_field]] = tdict[prefix+common_field]

        marr[iframe]['frame'] = iframe +1
    
    return marr
