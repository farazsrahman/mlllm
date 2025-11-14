#!/usr/bin/env python3
"""
Simple function to send console logs to ChatGPT and get a PNG plot back.
"""
import re
import os
import tempfile
import subprocess
from openai import OpenAI


# ============================================================================
# DEBUG: Hardcode console logs here for testing
# ============================================================================

# Paste your console logs between the triple quotes above for debugging


def extract_python_code(response_text: str) -> str:
    """Extract Python code from ChatGPT response."""
    # Try to find code blocks
    code_block_pattern = r'```(?:python)?\s*\n(.*?)```'
    matches = re.findall(code_block_pattern, response_text, re.DOTALL)
    if matches:
        return max(matches, key=len).strip()
    return ""


def plot_from_logs(
    console_logs: str,
    plotting_request: str,
    name: str = "plot",
    api_key: str = None,
    model: str = "gpt-4o"
) -> str:
    """
    Generate a plot from console logs using ChatGPT.
    
    Args:
        console_logs: Raw console log text
        plotting_request: String describing what plot to create (e.g., "log log scaling law for validation loss with line of best fit")
        name: Name for the output file (without extension, will be saved as gpt_png/{name}.png)
        api_key: OpenAI API key (if None, uses OPENAI_API_KEY env var)
        model: OpenAI model to use (default: gpt-4o)
    
    Returns:
        Path to the saved PNG file (gpt_png/{name}.png)
    """
    # Create gpt_png directory if it doesn't exist
    output_dir = "gpt_png"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create output path
    output_path = os.path.join(output_dir, f"{name}.png")
    
    # Call the main function
    return generate_plot_with_chatgpt(
        console_logs=console_logs,
        output_path=output_path,
        prompt=plotting_request,
        api_key=api_key,
        model=model
    )


def generate_plot_with_chatgpt(
    console_logs: str,
    output_path: str = "scaling_law_plot.png",
    prompt: str = "Given this data can you plot me a log log scaling law for validation loss with line of best fit",
    api_key: str = None,
    model: str = "gpt-4o"
) -> str:
    """
    Send console logs to ChatGPT, get plotting code, execute it, and save PNG.
    
    Args:
        console_logs: Raw console log text
        output_path: Path to save the PNG file
        prompt: Custom prompt for ChatGPT
        api_key: OpenAI API key (if None, uses OPENAI_API_KEY env var)
        model: OpenAI model to use (default: gpt-4o)
    
    Returns:
        Path to the saved PNG file
    """
    # Initialize OpenAI client
    if api_key:
        client = OpenAI(api_key=api_key)
    else:
        client = OpenAI()  # Uses OPENAI_API_KEY from environment
    
    print(f"Sending console logs to ChatGPT ({model})...")
    
    # Send raw console logs to ChatGPT
    full_prompt = f"""{prompt}

Here are the console logs:
{console_logs}

Please generate Python code using matplotlib to create the plot. The code should:
1. Use matplotlib and numpy
2. Parse the data from the console logs
3. Create a log-log plot of validation loss vs dataset size with a line of best fit
4. Save the figure to '{output_path}'

Return ONLY the Python code, wrapped in ```python code blocks."""
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates Python code for data visualization. Always return code wrapped in ```python code blocks."
            },
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        temperature=0.3,
    )
    
    response_text = response.choices[0].message.content
    print("Received response from ChatGPT")
    
    # Extract Python code
    code = extract_python_code(response_text)
    
    if not code:
        raise ValueError("Could not extract Python code from ChatGPT response.")
    
    print("Extracted Python code, executing...")
    
    # Ensure matplotlib uses non-interactive backend
    if 'import matplotlib' not in code:
        code = 'import matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\nimport numpy as np\n' + code
    elif 'matplotlib.use' not in code:
        code = code.replace('import matplotlib.pyplot', 'import matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot')
        code = code.replace('from matplotlib', 'import matplotlib\nmatplotlib.use("Agg")\nfrom matplotlib')
    
    # Fix output path in savefig calls
    savefig_pattern = r"plt\.savefig\([^)]+\)"
    def replace_savefig(match):
        savefig_call = match.group(0)
        params_match = re.search(r'plt\.savefig\([^,)]+,\s*(.+)\)', savefig_call)
        if params_match:
            extra_params = params_match.group(1)
            return f'plt.savefig("{output_path}", {extra_params}'
        else:
            return f'plt.savefig("{output_path}")'
    
    code = re.sub(savefig_pattern, replace_savefig, code)
    
    # Execute the code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_script = f.name
    
    try:
        result = subprocess.run(
            ['python3', temp_script],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Error executing code:\n{result.stderr}")
        
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Plot file was not created at {output_path}")
        
        print(f"✓ Plot saved to {output_path}")
        return output_path
        
    finally:
        if os.path.exists(temp_script):
            os.unlink(temp_script)


def main():
    """Example usage: read from stdin or a file."""
    import sys
    
    # Use hardcoded logs with specific plotting request
    logs = HARDCODED_LOGS
    plotting_request = "please make a plot of scaling laws from the above training console logs please make sure to keep everything on a log log scale and to fit a line of best fit. the line of best fit should match the color of the points"
    name = sys.argv[1] if len(sys.argv) > 1 else "scaling_law_plot"
    
    try:
        result_path = plot_from_logs(logs, plotting_request, name)
        print(f"\nSuccess! Plot saved to: {result_path}")
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)

HARDCODED_LOGS = """
[1/6] Dataset size: 100
  Trial 1/10... Final Validation Loss: 0.5072
  Trial 2/10... Final Validation Loss: 0.5323
  Trial 3/10... Final Validation Loss: 0.5191
  Trial 4/10... Final Validation Loss: 0.5080
  Trial 5/10... Final Validation Loss: 0.4897
  Trial 6/10... Final Validation Loss: 0.5809
  Trial 7/10... Final Validation Loss: 0.5133
  Trial 8/10... Final Validation Loss: 0.5398
  Trial 9/10... Final Validation Loss: 0.5370
  Trial 10/10... Final Validation Loss: 0.5126

[2/6] Dataset size: 200
  Trial 1/10... Final Validation Loss: 0.3333
  Trial 2/10... Final Validation Loss: 0.3284
  Trial 3/10... Final Validation Loss: 0.3304
  Trial 4/10... Final Validation Loss: 0.3030
  Trial 5/10... Final Validation Loss: 0.2651
  Trial 6/10... Final Validation Loss: 0.3212
  Trial 7/10... Final Validation Loss: 0.2761
  Trial 8/10... Final Validation Loss: 0.3653
  Trial 9/10... Final Validation Loss: 0.3060
  Trial 10/10... Final Validation Loss: 0.3196

[3/6] Dataset size: 500
  Trial 1/10... Final Validation Loss: 0.0447
  Trial 2/10... Final Validation Loss: 0.0316
  Trial 3/10... Final Validation Loss: 0.0338
  Trial 4/10... Final Validation Loss: 0.0381
  Trial 5/10... Final Validation Loss: 0.0459
  Trial 6/10... Final Validation Loss: 0.0578
  Trial 7/10... Final Validation Loss: 0.0409
  Trial 8/10... Final Validation Loss: 0.0366
  Trial 9/10... Final Validation Loss: 0.0318
  Trial 10/10... Final Validation Loss: 0.0441

[4/6] Dataset size: 1000
  Trial 1/10... Final Validation Loss: 0.0057
  Trial 2/10... Final Validation Loss: 0.0075
  Trial 3/10... Final Validation Loss: 0.0088
  Trial 4/10... Final Validation Loss: 0.0085
  Trial 5/10... Final Validation Loss: 0.0071
  Trial 6/10... Final Validation Loss: 0.0059
  Trial 7/10... Final Validation Loss: 0.0080
  Trial 8/10... Final Validation Loss: 0.0089
  Trial 9/10... Final Validation Loss: 0.0089
  Trial 10/10... Final Validation Loss: 0.0114

[5/6] Dataset size: 2000
  Trial 1/10... Final Validation Loss: 0.0024
  Trial 2/10... Final Validation Loss: 0.0028
  Trial 3/10... Final Validation Loss: 0.0035
  Trial 4/10... Final Validation Loss: 0.0031
  Trial 5/10... Final Validation Loss: 0.0024
  Trial 6/10... Final Validation Loss: 0.0026
  Trial 7/10... Final Validation Loss: 0.0025
  Trial 8/10... Final Validation Loss: 0.0030
  Trial 9/10... Final Validation Loss: 0.0026
  Trial 10/10... Final Validation Loss: 0.0023

[6/6] Dataset size: 5000
  Trial 1/10... Final Validation Loss: 0.0023
  Trial 2/10... Final Validation Loss: 0.0015
  Trial 3/10... Final Validation Loss: 0.0010
  Trial 4/10... Final Validation Loss: 0.0012
  Trial 5/10... Final Validation Loss: 0.0015
  Trial 6/10... Final Validation Loss: 0.0012
  Trial 7/10... Final Validation Loss: 0.0037
  Trial 8/10... Final Validation Loss: 0.0012
  Trial 9/10... Final Validation Loss: 0.0010
  Trial 10/10... Final Validation Loss: 0.0019
"""

if __name__ == "__main__":
    main()
