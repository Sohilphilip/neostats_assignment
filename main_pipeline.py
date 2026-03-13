import subprocess
import sys

def run_script(script_path):
    """Runs a Python script and checks for success."""
    print(f"\n{'='*50}")
    print(f"🚀 TRIGGERING: {script_path}")
    print(f"{'='*50}\n")
    
    # Run the script and capture the output
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    
    # Print the script's normal output
    print(result.stdout)
    
    # If the script failed, print the error and stop the pipeline
    if result.returncode != 0:
        print(f"❌ ERROR IN {script_path}:\n{result.stderr}")
        return False
        
    return True

if __name__ == "__main__":
    print("🌟 STARTING FULL NEOSTATS END-TO-END PIPELINE 🌟")
    
    # Define the order of operations
    pipeline_steps = [
        "src/ingestion.py",
        "src/transformation.py",
        "src/load.py"
    ]
    
    # Run each step in sequence
    for step in pipeline_steps:
        success = run_script(step)
        if not success:
            print(f"\n🛑 PIPELINE HALTED: Failed at {step}")
            sys.exit(1) # Exit with an error code
            
    print("\n✅ PIPELINE COMPLETED SUCCESSFULLY! Data is ready in Azure SQL.")