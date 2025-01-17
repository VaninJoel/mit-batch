from pathlib import Path
import os

# Model inputs to be changed must be in a dictionary format with the same 
# name as the created BatchTest.py file
var_dict = {"PARAMETER_NAME":    [.1, .9],          # 2
            "PARAMETER_NAME2":   [.1, .25, .5],     # 3
            "PARAMETER_NAME3":   [2, 500, 1000]}    # 3

# single_cell = {"side": [4, 6, 8, 10, 12]}

mult_dict = var_dict

# number of replicates
num_rep = 4

# Model output frequency
model_out_freq = 1

# Output frequency of simulation data per simulation replica
out_freq = 250 # VTK frequence in MCS

# Root output directory
sweep_output_folder = r'/N/u/jvanin/Carbonate/Projects/vCornea/Batch_Output'
if not os.path.isdir(sweep_output_folder):
    Path(sweep_output_folder).mkdir(parents=True)

# Input modules 
# from Models.Motion.Simulation import UniCellModelInputs
# from Models.SingleCell.Simulation import CellInputs
from Models.vCornea_4_8.Simulation import BatchTest
input_modules = [BatchTest]

# Automatic inputs
from BatchRun import BatchRunLib
BatchRunLib.register_auto_inputs(input_module_name='Models.vCornea_4_8.Simulation')

# Carbonate configuration
from BatchRun.BatchRunPrototyping import config_template

config_template = config_template()
config_template['jn'] = 'vCornea'       # Job Name
config_template['wh'] = 18              # Hours of Wall time requested
config_template['wm'] = 0               # Minutes of Wall time requested | Total time is (wh:wm)
config_template['ppn'] = 8              # How many jobs in a single node
config_template['vmem'] = 10            # Virtual memory requested in GB

#  Wall time = Maximum time the application can run, for Carbonate is 4 days (96 hours)
#  the more time requested the least priority rate the job gets


# Begin computing work
import os
from nCoVToolkit import nCoVUtils
from BatchRun import BatchRunPrototyping

BatchRunPrototyping.simulation_fname = os.path.join(os.path.dirname(__file__),
                                                    'UniCell_Explicit_Force_2D_with_beta.cc3d')

from BatchRun.BatchRunLib import cc3d_batch_key


def get_num_sets():
    num_sets = 1
    if mult_dict is not None:
        for v in mult_dict.values():
            num_sets *= len(v)
    return num_sets


def get_param_descr():
    if isinstance(mult_dict, dict):
        return {k + "_multiplier": f"Multiplier for {k}" for k in mult_dict.keys()}
    else:
        return None


def sim_input_generator(_set_idx):
    if mult_dict is None:
        return dict()

    sweep_vars = list(mult_dict.keys())
    sweep_idx = {s: 0 for s in sweep_vars}
    len_mults = {s: len(mult_dict[s]) for s in sweep_vars}
    recur_vals = {s: 0 for s in sweep_vars}
    for k in range(len(sweep_vars)):
        sweep_var = sweep_vars[k]
        if k == 0:
            recur_vals[sweep_var] = _set_idx
            sweep_idx[sweep_var] = _set_idx % len_mults[sweep_var]
        elif k == len(sweep_vars) - 1:
            sweep_var_o = sweep_vars[k - 1]
            sweep_idx[sweep_var] = int((recur_vals[sweep_var_o] - sweep_idx[sweep_var_o]) / len_mults[sweep_var_o])
        else:
            sweep_var_o = sweep_vars[k - 1]
            recur_vals[sweep_var] = int((recur_vals[sweep_var_o] - sweep_idx[sweep_var_o]) / len_mults[sweep_var_o])
            sweep_idx[sweep_var] = recur_vals[sweep_var] % len_mults[sweep_var]

    return {sweep_vars[k]: mult_dict[sweep_vars[k]][sweep_idx[sweep_vars[k]]] for k in range(len(sweep_vars))}


def main():
    num_sets = get_num_sets()

    # Add set labels to job names; scheduler adds run labels
    carbonate_config = [config_template.copy() for _ in range(num_sets)]
    set_idx = 0
    for cc in carbonate_config:
        cc['jn'] += f'_{set_idx}'
        set_idx += 1

    sim_input = list()
    from BatchRun.CallableCoV2VTM import cc3d_input_key
    for set_idx in range(num_sets):
        si = sim_input_generator(set_idx)
        si['__param_desc__'] = get_param_descr()
        # Append system configuration inputs
        si[cc3d_batch_key] = {'out_freq': model_out_freq}
        sim_input.append({cc3d_input_key: si})

    from BatchRun.BatchRunPrototyping import CallableCC3DCarbonateScheduler
    sim_run_sch = CallableCC3DCarbonateScheduler(carbonate_config=carbonate_config,
                                                 root_output_folder=sweep_output_folder,
                                                 output_frequency=out_freq,
                                                 screenshot_output_frequency=out_freq,
                                                 num_runs=num_rep,
                                                 sim_input=sim_input)
    sim_run_sch.run()

    # Export model parameters
    if input_modules is not None and isinstance(input_modules, list):
        for set_idx in range(num_sets):
            if sim_run_sch.is_dumping:
                o = sim_run_sch.dump_set_directory(set_idx)
            else:
                o = sim_run_sch.output_set_directory(set_idx)

            for x in input_modules:
                export_file_rel = x.__name__.split('.')[-1] + "Params.csv"
                export_file_abs = os.path.join(o, export_file_rel)
                nCoVUtils.export_parameters(x, export_file_abs)


if __name__ == '__main__':
    main()
