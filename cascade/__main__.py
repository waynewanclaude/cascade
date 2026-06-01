import sys
import os
import shutil
import importlib.util

CLI_USAGE_GUIDE = """Cascade - Zero-dependency Python-to-Web Visual Audit Dashboard
Usage:
  python -m cascade <study_config.py>       Launch designated study dashboard
  python -m cascade --init, -i              Copy starter study config templates to current directory
"""

def print_usage():
    print(CLI_USAGE_GUIDE)

def copy_templates():
    package_dir = os.path.dirname(os.path.abspath(__file__))
    templates_src = os.path.join(package_dir, "templates")
    current_dir = os.getcwd()
    
    if not os.path.exists(templates_src):
        print("Error: Packaged templates directory not found.")
        return
        
    copied = []
    for filename in os.listdir(templates_src):
        if filename.endswith(".py"):
            src_file = os.path.join(templates_src, filename)
            dest_file = os.path.join(current_dir, filename)
            shutil.copy2(src_file, dest_file)
            print(f"  Generated template: {filename}")
            copied.append(filename)
            
    if copied:
        print(f"\nSuccessfully initialized {len(copied)} templates in your active workspace:")
        print("To start, run one of the following:")
        for name in copied:
            print(f"  python -m cascade {name}")
    else:
        print("No templates found to copy.")

def run_study(config_path):
    if not os.path.exists(config_path):
        print(f"Error: Study configuration file '{config_path}' not found.")
        sys.exit(1)
        
    abs_config_path = os.path.abspath(config_path)
    config_dir = os.path.dirname(abs_config_path)
    
    # Inject config parent folder into sys.path to enable relative local imports within studies
    if config_dir not in sys.path:
        sys.path.insert(0, config_dir)
        
    # Dynamically import and compile config module
    module_name = "cascade_active_study"
    try:
        spec = importlib.util.spec_from_file_location(module_name, abs_config_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load specifications for {config_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"Compilation Error inside study configuration '{config_path}':")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    from cascade.core import Cascade
    app = None
    
    # Attempt 1: Fetch active instance from class-level variable
    if hasattr(Cascade, "active_instance") and Cascade.active_instance is not None:
        app = Cascade.active_instance
    else:
        # Attempt 2: Introspect module attributes for Cascade object instances
        for attr_name in dir(module):
            attr_val = getattr(module, attr_name)
            if isinstance(attr_val, Cascade):
                app = attr_val
                break
                
    if app is None:
        print(f"Error: No Cascade application instance was instantiated inside '{config_path}'.")
        print("Ensure you create a Cascade instance (e.g. app = Cascade(title='My Study'))")
        sys.exit(1)
        
    app.run(config_dir)

def main():
    args = sys.argv[1:]
    
    if not args:
        print_usage()
        sys.exit(0)
        
    primary_arg = args[0]
    
    if primary_arg in ("--init", "-i"):
        copy_templates()
    elif primary_arg.startswith("-"):
        print(f"Error: Unknown argument flag '{primary_arg}'")
        print_usage()
        sys.exit(1)
    else:
        run_study(primary_arg)

if __name__ == "__main__":
    main()
