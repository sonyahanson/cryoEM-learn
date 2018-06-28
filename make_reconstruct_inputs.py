# Run in this in a new directory called 'buildmap' in the same dir as the RELION/SPIDER/binary dirs.
# Then run 
# > relion_reconstruct --i EULER_1_of_20.star --angpix 1.2 --o RECONSTRUCT_1_of_20.mrc

# Note that in this case this is for nClass of 20, whereas the default is 50, so change if needed.

import numpy as np
import mrcfile
import pandas as pd

nPix = 160

for i in range(20):
    n = i+1

    binary_file  =  '../SPIDER/imgsSPIDER_trajectoryName_%s_of_20.dat'%n
    mrc_filename =  'particleIMGS_%s_of_20'%n
   
    align_file   =  '../RELION/align_%02d.dat'%n
    star_file    =  'EULER_%s_of_20.star'%n 


    binary_array = np.fromfile(binary_file,dtype=np.float32)

    # This builds a 3D array of nPix by nPix particles, skipping the headers
    my_particles = []
    # J iterates through particles
    for j in range(len(binary_array)/(nPix*nPix)):
        particle = []
        # i iterates through rows in the nPix x nPix particle
        for i in range(nPix):
            particle.append(binary_array[ (nPix*nPix*j) +(i+6+(3*j)) *nPix: (nPix*nPix*j) +(i+7+(3*j)) *nPix ])
        my_particles.append(particle)

    # We want to trim our number of particles, but before we do that we want to know the right number
    #  of particles from our align file

    df_Euler = pd.read_csv(align_file,sep='\s+') 
    df_Euler.columns=['particle','#columns','psi','theta','phi']

    print('### Frame %s has %s particles. ###' %(n,len(df_Euler)))

    my_particles_trimmed = my_particles[0:len(df_Euler)]

    # Below here is to get the data in a format that the mrcfile package understands.
    # This may be somewhat overkill, but it works.
    df = pd.DataFrame(my_particles_trimmed)
    values = df.values
    list_values = []
    for value in values:
        list_values.append(value.tolist())
    list_values_array = np.asarray(list_values)

    # Then we save that to our mrc file!
    mrc = mrcfile.new('%s.mrcs'%mrc_filename,overwrite=True)

    # The -1 here inverts the image so the particles are white.
    mrc.set_data(list_values_array*-1)
    mrc.set_image_stack()
    mrc.close()

    # Now we write out our star file
    with open(star_file,'w') as text_file:   
        text_file.write('\ndata_ \n \nloop_ \n \n_rlnImageName #1 \n_rlnAnglePsi #2 \n_rlnAngleTilt #3 \n_rlnAngleRot #4 \n')
        for i in range(len(df_Euler)):
            text_file.write('%s@%s.mrcs %s %s %s\n' %(df_Euler.particle[i],mrc_filename,df_Euler.psi[i],df_Euler.theta[i],df_Euler.phi[i]))
