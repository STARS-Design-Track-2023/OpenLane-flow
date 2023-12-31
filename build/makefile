###########################################################################################
# STARS 2023 General Makefile
# 
# Set tab spacing to 2 spaces per tab for best viewing results
###########################################################################################

##############################################################################
# VARIABLES
##############################################################################

# Source


# Flags to run make gds
KLAYOUT_FLAGS := $(SAK)/klayout/tech/sky130A/sky130A.krc -nn $(SAK)/klayout/tech/sky130A/sky130A.lyt -l $(SAK)/klayout/tech/sky130A/sky130A-eft.lyp


# Specify the name of the top level file (do not include the source folder in the name)
# NOTE: YOU WILL NEED TO SET THIS VARIABLE'S VALUE WHEN WORKING WITH HEIRARCHICAL DESIGNS
TOP_FILE         := 

# List internal component/block files here (separate the filenames with spaces)
# NOTE: YOU WILL NEED TO SET THIS VARIABLE'S VALUE WHEN WORKING WITH HEIRARCHICAL DESIGNS
COMPONENT_FILES  := 

# Specify the filepath of the test bench you want to use (ie. tb_top_level.sv)
# (do not include the source folder in the name)
TB               :=

# Get the top level design and test_bench module names
TB_MODULE		 := $(notdir $(basename $(TB)))
TOP_MODULE	     := $(notdir $(basename $(TOP_FILE)))

# Simulation
WF               ?= 0

# Directries where the source and mapped code is located
SRC              := src
MAP              := mapped
INC              := $(PWD)/includes_gl_sdf

# Location of executables
BUILD            := sim_build

# Simulation Targets
SIM_SOURCE       := sim_source

DUMP             := dump

# Compiler
VC               := iverilog
# Flags currently described specify the 2012 IEEE verilog standard, require compiler
# to look into the specify blocks in a cell lib, choose the max timings form the 
# parameters and print out the compiler verbose.
CFLAGS           := -g2012 -v

# Cell libraries
PDK_ROOT         := $(HOME)/pdk
PDK              := sky130A

##############################################################################
# RULES
##############################################################################


##############################################################################
# Administrative Targets
##############################################################################

###########################################################################################
# Make the default target (the one called when no specific one is invoked) to
# output the proper usage of this makefile
###########################################################################################
help:
	@echo "----------------------------------------------------------------"
	@echo "|                       Makefile Targets                       |"
	@echo "----------------------------------------------------------------"
	@echo "Administrative targets:"
	@echo "  all           - compiles the source version of a full"
	@echo "                  design including its top level test bench"
	@echo "  dir           - Creates required directories."
	@echo "  help          - makefile targets explanation"
	@echo "  clean         - removes the temporary files"
	@echo "  print_vars    - prints the contents of the variables"
	@echo
	@echo "Compilation targets:"
	@echo "  source       - compiles the source version of a full"
	@echo "                 design including its top level test bench"
	@echo
	@echo "Simulation targets:"
	@echo "  sim_source   - compiles and simulates the source version"
	@echo "                 of a full design including its top level"
	@echo "                 test bench"
	@echo "  sim_time     - simulates a time for netlist of a full"
	@echo "                 design with top level test_bench"
	@echo 
	@echo "Miscellaneous targets:"
	@echo "  lint         - checks syntax for source files with the"
	@echo "                 Verilator linter"
	@echo "  verify       - view traces with gtkwave. If you have a wave"
	@echo "                 foramt file saved run 'make verify WF=filename'"
	@echo "                 do not give the file extension .gtkw. Wave"
	@echo "                 format file must be saved in same directory as"
	@echo "                 the makefile."
	@echo "  view         - view the gate level circuit schematic"
	@echo "  view_gds     - view the gds file with KLayout"
	@echo "----------------------------------------------------------------"

all: $(SIM_SOURCE)

# A target that sets up the working directory structure
setup:
	@mkdir -p docs
	@mkdir -p $(MAP)
	@mkdir -p $(BUILD)
	@mkdir -p $(SRC)


# moves the GDS file to working directory and open it w/ klayout flags
view_gds:
	@./get_gds.py $(TOP_MODULE)
	@klayout -c $(KLAYOUT_FLAGS) $(TOP_MODULE).gds


# Removes all non essential files that were made during the building process.
clean:
	@echo "Removing temporary files, build files and log files"
	@rm -rf $(BUILD)/* 
	@rm -rf $(MAP)/*
	@rm -f *.log
	@rm -f *.vcd
	@rm -f xt
	@rm -f includes_gl_sdf
	@echo "Done\n\n"

print_vars:
	@echo "Component Files: \n $(foreach file, $(COMPONENT_FILES), $(file)\n)"
	@echo "Top level File: $(TOP_FILE)"
	@echo "Testbench: $(TB)"
	@echo "Top level module: $(TOP_MODULE)"
	@echo "Testbench module: $(TB_MODULE)"
	@echo "Gate Library: '$(PDK)'"
	@echo "Source work library: '$(SRC)'"
	@echo "Mapped work library: '$(MAP)'"


##############################################################################
# Compilation Targets
##############################################################################

# Define a pattern rule to automatically compile updated source files for a design
$(SRC): $(addprefix $(SRC)/, $(TOP_FILE) $(COMPONENT_FILES) $(TB))
	@echo "----------------------------------------------------------------"
	@echo "Creating executable for source compilation ....."
	@echo "----------------------------------------------------------------\n\n"
	@mkdir -p ./$(BUILD)
	@$(VC) $(CFLAGS) -o $(BUILD)/$(SIM_SOURCE).vvp $^
	@echo "\n\n"
	@echo "Compilation complete\n\n"

# Define a pattern rule to automatically compile mapped design files for a full mapped design
$(MAP): $(addprefix $(SRC)/, $(TOP_FILE) $(COMPONENT_FILES) $(TB))
	@echo "----------------------------------------------------------------"
	@echo "Compiling with sky130_fd_sc_hd process ....."
	@echo "----------------------------------------------------------------\n\n"
	@$(VC) $(CFLAGS) -o $(SIM_MAPPED).vvp -DFUNCTIONAL -DUNIT_DELAY=#1 -v $(PDK_ROOT)/$(PDK)/libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v -v $(PDK_ROOT)/$(PDK)/libs.ref/sky130_fd_sc_hd/verilog/primitives.v $(GL_PATH) $(SRC)/$(TB) 
	@echo "\n\n"
	@echo "Compilation complete\n\n"


##############################################################################
# Simulation Targets
##############################################################################

# This rule defines how to simulate the source form of the full design
$(SIM_SOURCE): $(SRC)
	@echo "----------------------------------------------------------------"
	@echo "Simulating source ....."
	@echo "----------------------------------------------------------------\n\n"
	@vvp -lxt -s $(BUILD)/$@.vvp
	@echo "\n\n"

# This rule defines how to simulate the mapped form of the full design
$(SIM_MAPPED): $(MAP)
	@echo "----------------------------------------------------------------"
	@echo "Simulating mapped ....."
	@echo "----------------------------------------------------------------\n\n"
	@vvp -lxt -s sim_mapped.vvp
	@echo "\n\n"

sim_time:
	@echo "----------------------------------------------------------------"
	@echo "Simulating mapped ....."
	@echo "----------------------------------------------------------------\n\n"
	@./time_sim.py $(TOP_MODULE)
	@cvc64 +interp \
		+define+SIM +define+FUNCTIONAL +define+GL +define+USE_POWER_PINS +define+UNIT_DELAY \
		+define+ENABLE_SDF +change_port_type +dump2fst +fst+parallel2=on  +nointeractive \
		-f $(INC) > time.log

##############################################################################
# Miscellaneous Targets
##############################################################################

# Define a pattern rule to lint source code with verilator
lint: $(addprefix $(SRC)/, $(TOP_FILE) $(COMPONENT_FILES) $(TB))
	@echo "----------------------------------------------------------------"
	@echo "Checking Syntax ....."
	@echo "----------------------------------------------------------------\n\n"
	@verilator --lint-only --timing -Wno-MULTITOP -Wno-TIMESCALEMOD $^
	@echo "\n\n"
	@echo "Done linting"

# Rule to look at the waveforms with gtkwave
verify: $(DUMP).vcd
ifeq ($(WF), 0)
	@gtkwave $^
else
	@gtkwave $^ -a $(WF).gtkw
endif

# Rule to look at the gate level schematic of the circuit
view: $(addprefix $(SRC)/, $(TOP_FILE) $(COMPONENT_FILES))
	@echo "----------------------------------------------------------------"
	@echo "Making Gate Level Schematic ....."
	@echo "----------------------------------------------------------------\n\n"
	@$(DC) -d -p 'read_verilog -sv $^; hierarchy -check -top $(TOP_MODULE); \
		proc; opt; fsm; opt; memory; opt; techmap; opt; show' > log_mapping.log
	@echo "Done creating Schematic"	

###########################################################################################
# Designate targets that do not correspond directly to files so that they are
# run every time they are called
###########################################################################################
.PHONY: all help clean print_vars
.PHONY: $(SRC) $(MAP)
.PHONY: $(SIM_SOURCE) $(SIM_MAPPED)
.PHONY: lint verify view
###########################################################################################
# Designate targerts that whose runtime warnings/errors may be ignored
###########################################################################################
.IGNORE: lint
