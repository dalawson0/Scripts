# Step 1 : Import the 4D Image
# Step 2: Grab the reference volume from the 3D vector
# 	◦  Use ITK script to do this
# step 3: Extract the 2nd volume and compare against the reference volume
# 	◦ The comparison will the MRI-PET script
#       let i = 2, repeat the extraction and comparison until i == N 
# step 4.capture parameters
# Step 5: plot the parameters

import os # functions & methods for performing OS-related tasks 
import sys # allows for interaction with the Python interpreter & current OS
import SimpleITK
import logging
import tempfile
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
# from FileProcessing import write_parameters
from FileProcessing import ReadnWrite

# Establisher logger object and its settings 
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel( logging.INFO )



## Step 0 - establishing directories
# working_path = '/Users/daniellawson/documents/activedir/bch/projects.nosycn'
working_path = '/home_local/daniellawson/Documents/projects'

##output
output_dir = working_path + '/Registration/outputs'
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
# set up subdirectories within the output directories
tempdir = tempfile.mkdtemp(prefix = "RigidReg-", dir = output_dir)
dataworkdir = tempdir + '/mri4dData'
alignworkdir = tempdir + '/alignment'
figworkdir = tempdir + '/Figures'
new_dir = [dataworkdir, alignworkdir, figworkdir]
for item in new_dir:
    if not os.path.isdir(item):
        os.mkdir(item)


## Step 1. load the image - scan_08-Subject
# input 
def open_file():
    tf = True
    if tf == True:
    # try: # open up GUI if the system supports it
        file_path = filedialog.askopenfilename()
    # except RuntimeError:
        # logger.info('No file has been selected')
    else:
        logger.info('No GUI available. Cannot use filedialog. Please specify a complete file path.')
        # scan = ['fmri', 'scout', 'T1-scan', 'T2-scan', 'fluid-suppressed']
        # subjects = ['34613-030','34613-034', '34613-042', '34613-043']
        # file = '/1_3_12_2_1107_5_2_43_166200_2023040617472437272833536_0_0_0_dwi_acq-CUSP90_dir-AP_20230406172644_14.nii.'
        # input_dir = working_path +'Warfieldatlas/subjects/' + subjects[2] + '/' + scan[0] 
        # file_path = input_dir +file
        file_path = sys.argv[0]
    return file_path 
image = open_file()
# image = "/Users/daniellawson/documents/activedir/bch/projects/warfieldatlas/subjects/34613-042/'Session 08'/diffusion/1_3_12_2_1107_5_2_43_166200_2023040617472437272833536_0_0_0_dwi_acq-CUSP90_dir-AP_20230406172644_14.nii"
input_img = SimpleITK.ReadImage(image)
logger.info('Input MRI is ' + image)

# NOTE :if statement to have the code work for 4D images 
size = list(input_img.GetSize())
if len(size) != 4:
    logger.info('Input image is of the ' + len(size)+ 'th dimesion, this script expects 4D.') 
    sys.exit(1)

# parse the dimensions of 4D image
size_x, size_y, size_z, num_timepoints = size[0], size[1], size[2], size[3]
print(f'> Image dimensions: {size_x} | {size_y} | {size_z} | {num_timepoints}') # the number of slices in x,y,z and the number of timepoints  
remaining_tp = num_timepoints -1


#Step 2. Extract the reference volume 
    # Define function to extract a subvolume 
def Extract(Input_image, subvol_size, start_idx):
    extractor_obj = SimpleITK.ExtractImageFilter()
    extractor_obj.SetSize(subvol_size)
    extractor_obj.SetIndex(start_idx)
    subvolume = extractor_obj.Execute(Input_image)
    extracted_size =  extractor_obj.GetSize()
    extracted_index = extractor_obj.GetIndex()
    print("> Extracted size:", extracted_size)
    print("> Extracted index:", extracted_index)
    return subvolume

# Extract reference volume 
ref_size, ref_idx = [size_x,size_y,size_z,1], [0,0,0,0] # specify the size & starting index the of the reference volume
filename = 'reference-volume.nii'
ref_path = dataworkdir + "/" + filename
reference_vol = Extract(input_img, ref_size, ref_idx)
first = SimpleITK.WriteImage(reference_vol, ref_path)



# Step 3. Extract subsequent volumes and preform Registration 
time = [] # start at time = 0
for cur_iter in range(0, 5): # num_timepoints, range(1, 18) == range(0,17)
    time.append(cur_iter)
    if cur_iter == 0:
        logger.info('Iterating through the subsequent volumes within the 4D image. Beginning regestriation')
    subvol_size = [size_x,size_y,size_z, 1]
    cur_idx = [0,0,0,cur_iter]
    try:
        cur_subvol = Extract(input_img,subvol_size,cur_idx)
    except RuntimeError:
        logger.info(f"It looks like the volume for the timepoint {cur_iter} doesn't exist.")
    except:
        logger.info(f'''It looks like the volume for the timepoint {cur_iter} doesn't exist.
                    Stopping volume extraction.''') 
    else:   
        newfile = f'/volume_{cur_iter}.nii' # expect volumes to start @ 2 and go to num_timepoints
        cur_output_pth =  dataworkdir + newfile
        SimpleITK.WriteImage(cur_subvol, cur_output_pth)  
        logger.info('Successfully created :' + newfile)

# Preform 6 DOF registration:
        #prep inputs
        docker_prefix = 'docker run -v'
        directory_mapping = tempdir + ':/data/'
        fixed_img = '/data/mri4dData/reference-volume.nii'
        moving_img = '/data/mri4dData' + newfile
        cur_trans = f'/data/alignment/transform_{cur_iter}.txt'
        output_file = f'/data/alignment/alignment_{cur_iter}.nii'
        cmd = docker_prefix + " " + directory_mapping + " " + "--name RigidRegistration --rm ccts3.aws.chboston.org:5151/computationalradiology/crkit:latest /opt/crkit/bin/crlRigidRegistration" + " " + fixed_img + " " + moving_img+ " " + output_file + " " + cur_trans 
        #execute command
        os.system(cmd)
        # # delete duplicate reference volume
        if cur_iter == 0:
            os.remove(cur_output_pth)
    finally: 
        logger.info('Moving on...')
     

print(time)
# print directory 
print(alignworkdir)



# step 4.capture parameters
parameters = ReadnWrite(alignworkdir)
# logger.info(parameters)



## step 5. plotting parameters
def plot_parameter(ylabel, measurement,color = 'k'):
    plt.plot(time,measurement, color) # could be a np.arrays or lists
    # Gold, hotpink red blue yellow, hexidecimal (rgb, #667788)
    plt.xlabel("time",fontsize = 12)
    plt.ylabel(ylabel, fontsize = 12)
    plt.title(f'{ylabel} vs. time', loc = 'center')
    plt.grid()
    plt.savefig(f'{figworkdir}/{ylabel}vTime.pdf',dpi=200)
    plt.show() 

x_pos = plot_parameter('x-position', parameters[0],"r")
y_pos = plot_parameter('y-position', parameters[1],'b') 
z_pos = plot_parameter('z-position', parameters[2],'g') 
yaw_pos = plot_parameter('psi', parameters[3])
pitch_pos = plot_parameter('theta', parameters[4],'m')
roll_pos = plot_parameter('phi', parameters[5],'y')

# consider making one plot 


