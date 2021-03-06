# This is a simulation of solvated polymethylene or polyethylene. It's still an on-going thing.
# I need to restrict the angles to real values. All my attempts up until now have failed.
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
close('all')# Depending on your developing environment you may or may not need this.
# I use it because it closes all figures.
params = {'backend': 'ps',
          'axes.labelsize': 20,
          'axes.titlesize': 20,
          'text.fontsize': 20,
          'legend.fontsize': 20,
          'xtick.labelsize': 10,
          'ytick.labelsize': 10,
          'ztick.labelsize': 10,
          'text.usetex': True,
          'font.family': 'serif',
          'mathtext.fontset': 'custom'}
matplotlib.rcParams.update(params)# I also have LaTeX installed, so my graph parameters
# include LaTeX typesetting. If you don't use LaTeX yourself,
# you should, but if you really don't want to, you need to
# take out the setting which gives graphs LaTeX typesetting (last 3 lines).
m = int(input("Number of carbons = "))# Asks an integer (no fractional atoms) input and saves it onto m.
m1 = int(input("Number of repetitions = "))# This is because my friends needed to calculate the mean distance
# between the first and last carbon atoms of a given number of polymers.
dist_ar = np.array([])# This is the distances array with which mean distance and std dev will be calculated.
for counter in np.arange(m1):# This is the for loop which gives the repetitions.
    n = m# Things went to hell if I didn't change variables. I still don't know why.
    r = float()# It's the bond length. I know I don't have to, but I like defining things.
    b = int(0)# This is the C-C-C angle counter. It's there so the bonds have the required angle between them.
# It works well when you take out all randomness, but if you do that then all you get is an upward spiral.
# The perfect example of damned if you do, damned if you don't. In fact, this whole program is.
    x, y, z = float(), float(), float()# These are the x,y,z coordiantes.
    p = np.ndarray((1,3),int)# ndarray because it needs to be able to morph into an nx3 matrix.
    p[:,:] = int(0)# This is the first coordinate, however, it doesn't figure in the plot or generated .txt files.
# The reason for this is that it doesn't preserve the angle it needs to have, but it's required
# for the definition of vectors.
    i = int()# This is the counter for the cycle which builds the polymer.
    v_list = np.array([])# This is the list for all bond lengths, its dimension is n-1 (C-C-C), n = number of points.
    text_file=open('points'+str(counter+1)+'.txt',"w")# Creates a .txt file "points[counter+1]", where counter is the
# repetition number, so points1, points2, etc.
    text_file.write('Number of carbons = '+str(n)+'\n\n')# Gives the number of carbon atoms in the chain.
    text_file.write('x y z\n\n')# Labels each coordinate row.
    for i in np.arange(1,n+1):# Starts from 1 because it needs to index p[0,:], ends at n+1 because that's how python
# works. Eg. np.arange(a,k) = [a,a+1,a+2,...,k-1]
        if np.random.randint(0,2)==1:# Decides whether the angle between carbons will be measured clock or anticlockwise.
# This eliminates any chirality (handedness).
            b = b + 1
        else:
            b = b - 1
        phi = np.random.uniform(0,np.pi)# Growth angle. This can stand in for good or bad solvents. It can also stand in
# for solvation kinetics. The wider the range, the more spherical the polymer
# tends to be. Good solvents stretch the chains, bad solvents only swell them.
# This is the angle between the Z axis and the XY plane.
        r = 0.001*np.random.randn() + 1.59# Bond length, with some randomness thrown in. This is a random normal dis-
# tribution with 0.001 std dev and 1.59 mean.
        if i>1:#This is so the program can define dihedral angles.
            xi = p[i-1,0]# The last x coordinate. It's added to the new calculated x. This makes the polymer grow out.
            yi = p[i-1,1]# The last y coordinate. It's added to the new calculated x. This makes the polymer grow out.
            zi = p[i-1,2]# The last z coordinate. It's added to the new calculated x. This makes the polymer grow out.
            ux = p[i-1,0] - p[i-2,0]# The x component of the bond vector around which the coordinates will rotate.
            uy = p[i-1,1] - p[i-2,1]# The y component of the bond vector around which the coordinates will rotate.
            uz = p[i-1,2] - p[i-2,2]# The z component of the bond vector around which the coordinates will rotate.
            if np.random.randint(0,2)==1:# Decides whether the rotation will be clock or anticlockwise.
                theta = np.random.randn() + np.pi/6
            else:
                theta = np.random.randn() - np.pi/6
            n = np.linalg.norm(np.array([ux,uy,uz]))**2# The bond vector's squared norm. Needed for the rotation
# matrix, which involves vector projections. Linear algebra rules.
            N = np.linalg.norm(np.array([ux,uy,uz]))# The bond vector's norm. Also needed for the rotation matrix.
            r_vec = np.array([ux,uy,uz])/N# Unitary bond vector around which the rotation will be performed.
# Doesn't figure explicitly, but is required in the construction of the
# rotation matrix.
            C = np.cos(theta)# One of the terms in the rotation matrix.
            S = np.sin(theta)# One of the terms in the rotation matrix.
            t = 1 - np.cos(theta)# One of the terms in the rotation matrix.
            R = np.array([
            [t*ux**2/n+C,t*ux*uy/n-S*uz/N,t*ux*uz/n+S*uy/N],
            [t*ux*uy/n+S*uz/N,t*uy**2/n+C,t*uy*uz/n-S*ux/N],
            [t*ux*uz/n-S*uy/N,t*uy*uz/n+S*ux/N,t*uz**2/n+C]
                          ])# Normalised rotation matrix about an arbitrary vector at the origin.
            x=r*np.sin(phi)*np.cos((b*109.5)/180*np.pi)# Generating the x coordinate of the new point.
# r is centered at the origin, otherwise this shit won't work.
            y=r*np.sin(phi)*np.sin((b*109.5)/180*np.pi)# Generating the y coordinate of the new point.
# r is centered at the origin, otherwise this shit won't work.
            z=r*np.cos(phi)# Generating the y coordinate of the new point. r is centered at the origin,
# otherwise this shit won't work.
            v = np.array([x,y,z])# Places all coordinates on a vector.
            v = np.dot(R,v)# Matrix multiplication which rotates the vector.
            p1=np.array([v[0]+xi,v[1]+yi,v[2]+zi])# Adds the last point's coordinates to the new coordinates.
            p=np.vstack((p,p1))# Adds the new coordinates to the last line of the coordinate matrix.
            text_file.write(str('{0}'.format(' '.join(str(i) for i in p[i,:])+'\n')))
# Writes each coordinate, separated by a space, onto the text file. This allows the user to plot the
# coordinates in the software of their choice.
            v_list = np.append(v_list,np.linalg.norm(v))# Adds the bond vector norm to a list.
        else:
            x=r*np.sin(phi)*np.cos((b*109.5)/180*np.pi)# Creates the first point on x.
            y=r*np.sin(phi)*np.sin((b*109.5)/180*np.pi)# Creates the first point on y.
            z=r*np.cos(phi)# Creates the first point on z.
            p1=np.array([x,y,z])# Makes a vector from these coordinates.
            p=np.vstack((p,p1))# Adds this vector as a row at the bottom of the coordinate matrix.
            text_file.write(str('{0}'.format(' '.join(str(i) for i in p[i,:])+'\n')))
# Writes each coordinate, separated by a space, onto the text file. This allows the user to plot the
# coordinates in the software of their choice.
    text_file.write('\nMean bond length = '+str(v_list.mean())+' Angströms\n\n')
    text_file.write('Bond length standard deviation = '+str(v_list.std())+' Angströms\n\n')
    gyr_rad = np.linalg.norm(np.array([p[n-4,0]-p[1,0],p[n-4,1]-p[1,1],p[n-4,2]+p[1,2]]))# Gyroscopic radius.
# Distance between the first and last carbon carbon atoms in a polymer.
# I have no idea why the last carbon atom corresponds to the n-4 index.
    text_file.write('Gyroscopic radius = '+str(gyr_rad))
    dist_ar = np.append(dist_ar,gyr_rad)
# This adds the distance between the first and last carbons in each repetion to an array
    text_file.close()# Closes the text file with the coordinates.
    fig = plt.figure(figsize=(15,15))# Creates a figure that is 15in x 15in in size.
    ax = fig.add_subplot(1, 1, 1, projection='3d')# Creates a 3d subplot.
    ax.plot(p[1:,0],p[1:,1],p[1:,2], '-', label=r'Polymer')# Plots every point.
    ax.legend(loc=0)# Dynamically decides the best place for a label.
    ax.set_xlabel(r'X')# x-axis name.
    ax.set_ylabel(r'Y')# y-axis name.
    ax.set_zlabel(r'Z')# z-axis name.
    ax.set_aspect(1)# Plot aspect ratio.
print(dist_ar.mean())# Prints the mean distance between first and last points among repetitions.
print(dist_ar.std())# Prints the std dev of the distances between first and last points among repetitions.
