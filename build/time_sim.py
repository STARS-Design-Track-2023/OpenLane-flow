#!/usr/bin/env python3

import os, glob, sys, subprocess


# ---------------------------------------------------------------------- #
# This function gets the name of the latest folder generated by the      #
# efabless flow                                                          #
# ---------------------------------------------------------------------- #
def get_latest ():
    list_of_folders = glob.glob("runs/*") 
    latest_folder = max(list_of_folders, key=os.path.getctime)
    return latest_folder

# ---------------------------------------------------------------------- #
# Moves the synthesis and sdf files generated by the efabless flow into  #
# mapped directory                                                       #
# ---------------------------------------------------------------------- #
def move (sdf_path, gl_path):
    subprocess.call ("cp "+sdf_path+" mapped/synth.sdf", shell=True)
    subprocess.call ("cp "+gl_path+" mapped/synth.v", shell=True)
    return

# ---------------------------------------------------------------------- #
# Generates a includes file for cvc to use when running timing           #
# simulations                                                            #
# ---------------------------------------------------------------------- #
def gen_includes (cwd, tb_path, gl_path, primitives_path, syk130_path, fname):

    # Creates am inludes file if it doesn't exist
    subprocess.call ("touch -a "+fname, shell=True)

    # Includes file paths
    tb_path_in         = cwd + "/" + tb_path + "\n"
    gl_path_in         = cwd + "/" + gl_path + "\n"
    primitives_path_in = cwd + "/" + primitives_path + "\n"
    syk130_path_in     = cwd + "/" + syk130_path + "\n"

    # Open the file
    f = open (fname, "w")

    # Write to the file
    f.write (tb_path_in)
    f.write (gl_path_in)
    f.write (primitives_path_in)
    f.write (syk130_path_in)

    # Close the file
    f.close()

    return

# ----------------------------- Main Function -------------------------- #
def main ():

    # get the current working directory
    cwd = os.getcwd()

    # Module name and the location of latest run
    module_name = sys.argv[1]
    latest_folder = get_latest()

    # Path variables
    sdf_path         = latest_folder+"/results/final/sdf/multicorner/nom/"+module_name+".Typical.sdf"
    gl_path          = latest_folder+"/results/final/verilog/gl/"+module_name+".v"
    primitives_path  = "cvc_pdk/primitives_hd.v"
    syk130_path      = "cvc_pdk/sky130_fd_sc_hd.v"
    tb_path          = "src/tb_"+module_name+".v"

    # Includes the
    fname = "includes_gl_sdf"
    
    # Move the files
    move (sdf_path=sdf_path, gl_path=gl_path)

    # Generate includes file for cvc
    gen_includes (cwd=cwd, tb_path=tb_path, gl_path=gl_path, primitives_path=primitives_path, syk130_path=syk130_path, fname=fname)

    return


if __name__ == "__main__":
    main ()

