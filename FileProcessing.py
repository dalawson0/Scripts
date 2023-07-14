import os
from natsort import natsorted, ns

# file processing 
workingdir = '/Users/daniellawson/documents/activedir/bch/project/registration/outputs/rigidreg-a0d7waox/alignment' # append to tempdir or aligment

def ReadnWrite(workingdir):
    dir_content = os.listdir(workingdir) # goes from the top down (sorted)
  
    x,y,z,yaw,pitch,roll,numbers = [],[],[],[],[],[],[]
    i,j,k,psi,theta,phi = 0,1,2,3,4,5 # indexes

    # ## check the first file for the fixed parameters in x,y,z(likely do this separately)
    # with open(workingdir + '/transform_2.txt', mode = 'r') as fixed_file:
    #     fixed_params = list(enumerate(fixed_file))[4][-1]
    #     print(fixed_params)
    #     spliter = fixed_params.split()
    #     numbers.append(spliter[1::])
    #     x.append(float(numbers[0][i])),y.append(float(numbers[0][j])),z.append(float(numbers[0][k])), yaw.append(float(0)),pitch.append(float(0)),roll.append(float(0))
    #     print(x,y,z,yaw,pitch,roll)
    #     # print('\n', numbers)

    # natural sort the transformation files
    mylist = []  
    for item in dir_content:
        if item[0:9] == "transform":
            mylist += [item]
     
    
    ntsorted_ls = natsorted(mylist, key = lambda y: y.lower())
    print(ntsorted_ls) # confirm everything is organized

    counter = 0 # used to help extract the right parameter value from numbers ls
    for item in ntsorted_ls:
        cur_path = workingdir + '/' + item
        with open(cur_path, mode ='r') as curfile:
            line_params= list(enumerate(curfile))[3][-1] # extract line with parameters, and get rid of the line number
            # print(line_params)
            element = line_params.split() # make a list that split up the 'parmeters' & individual numbers
            numbers.append(element[1::]) # grab only the numbers 
            # print('\n',numbers) 
            x.append(float(numbers[counter][i])),y.append(float(numbers[counter][j])),z.append(float(numbers[counter][k])),yaw.append(float(numbers[counter][psi])),pitch.append(float(numbers[counter][theta])),roll.append(float(numbers[counter][phi]))# append each parameter list
            # print(x,y,z,yaw,pitch,roll)
            counter += 1
        # try:
        #     os.remove(cur_path) # delete the current file 
        # except FileNotFoundError:
        #     print("This file doesn't exist already")
        #     break
        # finally:
        #     print('Successfully removed. Moving on...')
    
 # append the inital file with transformation parameters 
    with open(workingdir + '/All-transformations.txt' , mode ='w+') as file: # after you have gone through the file, and appened params list, delete the file (save space)
        file.write(f'\n\nX:\n{x}\n\nY:\n{y}\n\nZ:\n{z}\n\nYaw:\n{yaw}\n\nPitch:\n{pitch}\n\nRoll:\n{roll}') 
    return x,y,z,yaw,pitch,roll

'''
def write_parameters(workingdir):
    dir_content = os.listdir(workingdir)    # NOTE : files are sorted if operation is done after there creation

    x,y,z,yaw,pitch,roll,numbers = [],[],[],[],[],[],[]
    i,j,k,psi,theta,phi = 0,1,2,3,4,5 # indexes

    for item in dir_content:
        if item[0:9] == "transform":
            print(item)
            with open(workingdir + '/' + item , mode ='r') as file:
                # NOTE: if I have separate files 
                val  = list(enumerate(file))[3][-1] # extract the third line from list
                # counter = len(val)
                element = val.split()
                numbers.append(element[1::])
                x.append(float(numbers[0][i])),y.append(float(numbers[0][j])),z.append(float(numbers[0][k])),yaw.append(float(numbers[0][psi])),pitch.append(float(numbers[0][theta])),roll.append(float(numbers[0][phi]))
            # print(x,y,z,yaw,pitch,roll)
    with open(workingdir + '/Paramters-lsted' , mode ='w+') as cur_file:
        cur_file.write(f'{x}\n\n{y}\n\n{z}\n\n{yaw}\n\n{pitch}\n\n{roll}')
    return x,y,z,yaw,pitch,roll
'''


# # # Test write_parameters
# Test ReadnWrite
# alpha = '/Users/daniellawson/documents/activedir/bch/projects/registration/outputs/rigidreg-WoahTooMuch/alignment' # append to t
# # # esults = append_paramters(alpha)
# # # # print('\n', esults)
# new = ReadnWrite(alpha)
# print('\n', new)


