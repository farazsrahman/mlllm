"""
plotting.py — Plotly chart generation (placeholder)

This module should handle:
- Generating Plotly JSON from training metrics
- Creating training/validation loss curves
- Building learning rate schedules
- Comparing multiple runs on same chart
- Customizing dark theme for Trex UI

Backend Implementation Steps:
1. Parse metrics from storage or log files
2. Build Plotly data structures (traces)
3. Configure layout with proper styling
4. Support multiple chart types (line, scatter, bar)
5. Apply dark theme colors matching frontend (#00143c, #00b4f0, #b428ff)
6. Return JSON-serializable Plotly figure

Example Interface:
    plotter = Plotter()
    plot_json = plotter.create_training_plot(run_id)
    # Returns: {"data": [...], "layout": {...}}
    
    multi_plot = plotter.compare_runs([run1, run2, run3])

This file is intentionally left incomplete for backend teammates to implement.
"""

# TODO: Implement Plotter class
# TODO: Add Plotly figure generation
# TODO: Create training curve builders
# TODO: Apply Trex color scheme
# TODO: Add comparison plot functionality
# TODO: Ensure JSON serialization works correctly
