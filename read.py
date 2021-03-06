from sys import exit
from analysis import averaging, free_energy, draw_phase_diagram


def select_calculation(calc, data, strain_file, Tmin, Tmax, dT, dTmin, points, T, x, kB):
    if calc=='p':
        draw_phase_diagram(data, strain_file, points, dT, Tmin, dTmin, Tmax, kB)
    elif calc=='a':
        averaging(data, strain_file, T, points, x, kB)
    elif calc=='f':
        free_energy(data, strain_file, T, points, kB)







def read_input_file(filename):
    """
    A function to read the file containing properties of microstates (configurations)
    
    :param filename: name of target file
    :type  filename: string
    :return: data
    :rtype: dictionary (data[composition][energy][i_th_prop][property[i_th_prop]]=degeneracy)
    """
    data_file=open(filename,'r')
    lines=data_file.readlines()
    data_file.close()

    Data={}
    num_prop=None

    for line in lines:
        _line=line.split('#')[0]
        if len(_line)<=1: continue

#        comp,*properties=[float(_) for _ in line.split()]  # makes error in python2
        properties=[float(_) for _ in _line.split()]
        comp=properties.pop(0)
        energy=properties[0] #properties[0] : energy

        if num_prop:
            if num_prop != len(properties):
                print("Wrong format of %s" %filename)
                print("The line shown below is of a different format than the previous lines")
                print("%s" %line)
                exit()
        else:
            num_prop=len(properties)

        if not comp in Data:
            Data[comp]={}
        if not energy in Data[comp]: 
            Data[comp][energy]=[]
            for _ in properties:
                Data[comp][energy].append({})

        for i_th_prop in range(len(properties)):
            if not properties[i_th_prop] in Data[comp][energy][i_th_prop]:
                Data[comp][energy][i_th_prop][properties[i_th_prop]]=1
            else:
                Data[comp][energy][i_th_prop][properties[i_th_prop]]+=1

    # Format of data[composition][energy][i_th_prop][property[i_th_prop]]=degeneracy
    # energy : eV/atom or eV/formular unit
    # properties : Unit never changed in the whole process

    N_comp=len(Data) #Number of composition.
    N_atom=N_comp-1 #Number of atom. Number of formular unit in supercell.

    # Checking data existance in all composition and prevent that 0.333333 != 1/3
    data={}
    for i in range(N_comp):
        flag=1
        for j in Data:
            tmp=i/(N_atom*1.0)-j
            if tmp<0.0001 and tmp>-0.0001:
                data[i/(N_atom*1.0)]=Data[j]
                flag=0

        if flag:
            print ("It seems that data for some possible compositions are not included in CompositionEnergyList.log file" )
            print ("Or make sure that same composition is written in same way(0.3333 0.3334 -> 0.3333 0.3333)" )
            exit()
    return data


def read_strain_file(filename):
    """
    A function to read the file containing parameters to fit local strain
    
    :param filename: name of target file
    :type  filename: string

    :return: splitted data in strain_file
    :rtype: list
    """
    File=open(filename,'r')
    line=File.readline().split()
    File.close()
    return line
