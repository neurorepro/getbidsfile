import os
import sys
import argparse
import textwrap
from bids import BIDSLayout
import warnings

warnings.filterwarnings("ignore", ".*currently excludes the leading dot.*")

########################################################################################
### Argument parsing
###
def main():
    ##### PARSER
    def type_isfile(f):
        if not os.path.isfile(f):
            raise argparse.ArgumentTypeError("%s does not exist" % f)
        return f
    def type_isdir(d):
        if not os.path.isdir(d):
            raise argparse.ArgumentTypeError("Directory %s does not exist" % d)
        return d
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Query single BIDS file for a given subject and BIDS dataset'''),
        epilog=textwrap.dedent('''\
            Example: bidsget --bidsdir /my/bids --subject 0001 --suffix T1w'''))
    parser.add_argument("--bidsdir", required=True, help="path to the BIDS directory", type=type_isdir)
    parser.add_argument("--subject", required=True, help="name of subject (e.g. '0001')")
    parser.add_argument("--suffix", required=False, help="suffix present in filename (e.g. 'T1w')")
    parser.add_argument("--extension", required=False, help="extension of queried file (e.g. 'nii.gz' or '[.nii, .nii.gz]')")
    parser.add_argument("--scope", required=False, help="scope (e.g. 'raw', 'derivatives')", default="all")
    args = parser.parse_args()
    ### Get arguments
    bidsdir = os.path.abspath(args.bidsdir)
    scope = args.scope
    # Set dictonary filter for BIDS layout
    nonfilter_args = ["bidsdir", "scope"]
    all_args = vars(args)
    filters = {k: v for k, v in all_args.items() if k not in nonfilter_args and v is not None}

    ####  Extract files
    layout = BIDSLayout(bidsdir)
    layout_files = layout.get(scope=scope, return_type="file", **filters)

    if len(layout_files) == 0:
        sys.exit("No file found matching the provided arguments.")
    elif len(layout_files) == 1:
        print(layout_files[0])
    else:
        sys.exit(textwrap.dedent(f"""\
                  More than one file found matching the provided arguments: {layout_files}.
                  You can use the "extension" option to select files according to file extension. 
                  """))

if __name__ == "__main__":
    main()


