from runset_train import parameters
from argparse import Namespace

# get list of params, check validity (type and poss)
# return list of [name, [val1, val2, ...]]
def get_parameters_of_runs(params_dict):
    # First create cart prod runsets.
    vals_list = []
    cart_prod_runsets = []
    for info in params_dict.param_infos:
        cart_prod_runsets, vals_list = info.get_input_and_update_runsets(cart_prod_runsets, vals_list, params_dict)
    # Then create args list.
    args_list = []
    indRunNo = 1
    for run in cart_prod_runsets:
        kwargs = {}
        for no, name in enumerate([info.name for info in params_dict.param_infos]): kwargs[name] = run[no]
        kwargs['indRunNo'] = indRunNo # add individual run no
        kwargs['totalInds'] = len(cart_prod_runsets)
        curr_args = Namespace(**kwargs)
        args_list.append(curr_args)
        indRunNo += 1
    return args_list
        
# return a "\n" separated list
def create_opts_strs(args_list, params_dict):
    opts_strs = ""
    names_list = [info.name for info in params_dict.param_infos]
    for args in args_list:
        # First check validity of args
        parameters.check_args(args, params_dict)
        opts = ""
        for no,name in enumerate(names_list):
            if eval("args."+name) is not None:
                opts += " --"+name + " " + str(eval("args."+name))
        opts_strs += opts + "\n"#":"
    return opts_strs[:-1]

    
def main(dict_file):
    params_dict = parameters.decode_arguments_dictionary(dict_file)
    args_list = get_parameters_of_runs(params_dict)
    opts_strs = create_opts_strs(args_list, params_dict)
    return opts_strs, params_dict
if __name__ == "__main__":
    main()
