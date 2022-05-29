from components.force import Force
from components.support import FixedSupport, PinnedSupport, RollerSupport
from components.moment import Moment

import numpy as np
import matplotlib.pyplot as plt

def calculate_support_reactions(components):
    """Calculate support reactions"""
    times = []
    fy = 0
    distcount = 0
    
    for distload in components["distloads"]:
        ang = 90 if distload.direction == "up" else 270
        components["forces"].append(Force(distload.eq_loc, distload.eq_force,ang, 1))
        distcount += 1
    
    
    for force in components["forces"]:
        fy +=force.fy
    
    totalmom = 0
    for moment in components["moments"]:
        totalmom += moment.mag
    
    rows = []
    row1 = []
    for support in components["supports"]:
        row1.append(1)
    
    rows.append(row1)
    rrow = []
    rrow.append(-fy)
    
    for support in components["supports"]:
        newrow = []
        fmom = 0
        for force in components["forces"]:
            fmom += force.fy * (force.x-support.x)
        for othersup in components["supports"]:
            newrow.append(othersup.x-support.x)
        rows.append(newrow)
        rrow.append(-fmom-totalmom) 
    
    delete = True
    fixedcount = 0
    for support in components["supports"]:
        if isinstance(support, FixedSupport):
            delete = False
            fixedcount +=1
            for row in rows:
                row.append(1)
            rows[0][-1] = 0

    
    if delete:
        del rows[-1]
        del rrow[-1]

    nmat = np.array(rows)
    cons = np.array(rrow)
    
    components["forces"] = components["forces"][:-distcount or None]
    
    try:
        ans = np.linalg.solve(nmat,cons)
    except np.linalg.LinAlgError:
        return False
        
    
    for ind, support in enumerate(components["supports"]):
        support.reaction_force = ans[ind]
    
    for support in components["supports"]:
        if isinstance(support, FixedSupport):
            support.reaction_moment = ans[-fixedcount]
            fixedcount -= 1
    
    return True

def plot_diagrams(components, beam_length):
    """
    Calculate support reactions incrementing with inc,
    Use a dummy fixed support at the right side to save the moments and shears,
    and plot the moment and shear diagrams
    """
    inc = 0.005
    shears = []
    moments = []

    # Linear space
    x = np.arange(0, beam_length, inc)

    # Copying the list to not change the original
    copied_components = {key:[val.duplicate(beam_length) for val in lst] for key, lst in components.items()}

    # Converting supports to forces and moments
    for support in copied_components["supports"]:
        ang = 90 if support.reaction_force >= 0 else 270
        copied_components["forces"].append(Force(support.x,support.reaction_force,ang, beam_length))
        if isinstance(support, FixedSupport):
            copied_components["moments"].append(Moment(support.x,support.reaction_moment, beam_length))
    
    # Deleting the converted supports
    copied_components["supports"] = []
    
    for i in range(len(x)):
        components_in_range = {key:[val.duplicate(beam_length) for val in lst] for key, lst in copied_components.items()}
        
        # Converting distributed loads to equivalent forces
        
        for distload in components_in_range["distloads"]:
            if distload.startx < x[i]:
                if distload.endx > x[i]:
                    distload.endx = x[i]
                    distload.calculate_equivalent_quantities()
            ang = 90 if distload.direction == "up" else 270
            components_in_range["forces"].append(Force(distload.eq_loc,distload.eq_force,ang, beam_length))
        
        # Deleting the converted distributed loads

        components_in_range["distloads"] = []
        
        for subclass in components_in_range:
            for component in components_in_range[subclass]:
                if component.x > x[i]:
                    components_in_range[subclass].remove(component)
        
        # Creating a mock fixed support to calculate reactions
        components_in_range["supports"].append(FixedSupport("right", x[i]))
        
        calculate_support_reactions(components_in_range)
        
        fixed_support = components_in_range["supports"][0]
        
        shears.append(-fixed_support.reaction_force)
        moments.append(fixed_support.reaction_moment)
        

        
    
    x = np.insert(x,0,0)
    x = np.append(x,beam_length)
    shears.insert(0,0)
    moments.insert(0,0)
    shears.append(0)
    moments.append(0)

    fig, subplot = plt.subplots(2,sharex=True)
    subplot[0].plot(x,shears)
    subplot[0].set_title("Shear Diagram")
    subplot[0].fill(x, shears, facecolor='blue', alpha=0.1)
    subplot[0].axhline(y=0, color='r', linestyle='--')
    plt.xlim([0,beam_length])
    subplot[1].plot(x,moments)
    subplot[1].set_title("Moment Diagram")
    subplot[1].fill(x, moments, facecolor='blue', alpha=0.1)
    subplot[1].axhline(y=0, color='r', linestyle='--')
    plt.xlim([0,beam_length])
    plt.show()

def check_indeterminate(components, beam_length):
    unknowns = 0
    sup_xs = []
    for comp in components:
        if isinstance(comp, (PinnedSupport, RollerSupport)):
            unknowns += 1
            sup_xs.append(comp.x)
        elif isinstance(comp, FixedSupport):
            unknowns += 2
            sup_xs.append(comp.x)

    segments = len(set(sup_xs + [0, beam_length])) - 1

    return unknowns <= 2 * segments