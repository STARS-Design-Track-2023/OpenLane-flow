#!/usr/bin/env python3

# Import the required libraries
import subprocess as s
import os, sys

def init_design (design):

    # change into the designs directory
    os.chdir ("designs")

    # make the dir for design
    s.call ("mkdir -p "+design, shell=True)

    # copy the dependencies into the design dir
    s.call ("cp ~/build/time_sim.py "+design+"/.", shell=True)
    s.call ("cp ~/build/config.json "+design+"/.", shell=True)
    s.call ("cp ~/build/makefile "+design+"/.", shell=True)
    s.call ("cp -r ~/build/cvc_pdk "+design+"/.", shell=True)
    s.call ("cp ~/build/get_gds.py "+design+"/.", shell=True)
    
    # change to the design dir
    os.chdir(design)

    # make the required directories
    s.call ("mkdir -p src", shell=True)
    s.call ("mkdir -p mapped", shell=True)
    s.call ("mkdir -p docs", shell=True)
    s.call ("mkdir -p sim_build", shell=True)

    return

def main ():
    
    if (len(sys.argv) != 2 or sys.argv[1] == "-help" or sys.argv[1] == "-h"):
        print("""
---------------------------------------------
Syntax : ./init_design <design name>
---------------------------------------------
        """)
    else:
        init_design(sys.argv[1])
    
    return

if __name__ == "__main__":
    main ()
