# Trex ML Experiment Assistant - Design Guidelines

## Design Approach
**Utility-Focused Application**: This is a productivity tool for ML researchers. Prioritize efficiency, readability, and quick information scanning over visual flourishes.

## Color Palette (Fixed)
- **Primary Background**: `#00143c` (dark navy)
- **Accent Blue**: `#00b4f0` (bright blue for interactive elements, highlights)
- **Accent Purple**: `#b428ff` (purple for secondary highlights, badges)
- **Text**: White/light gray on dark backgrounds
- **Status Indicators**: Use accent colors for active states, muted grays for inactive

## Layout System

### Homepage Structure
**Two-column grid layout**:
- **Left Panel (40% width)**: Chat interface
- **Right Panel (60% width)**: Runs grid

**Spacing**: Use Tailwind units: `p-4`, `p-6`, `gap-4`, `gap-6` for consistent rhythm

### Component Layouts
- **ChatWindow**: Full height of left panel, scrollable message area
- **ChatInput**: Fixed at bottom of left panel
- **RunsGrid**: Responsive grid (1 column mobile, 2-3 columns desktop)
- **RunCard**: Compact card showing metrics at a glance

## Typography
- **Headings**: Bold, sans-serif (system default or Inter)
- **Body**: Regular weight for chat messages and run details
- **Monospace**: For run IDs, numeric values (lr, epochs, batch_size)
- **Sizes**: `text-sm` for metadata, `text-base` for messages, `text-lg` for headings

## Core Components

### Chat Interface (Left Panel)
- **ChatBubble**: Rounded corners, distinguish user (right-aligned, blue accent) vs system (left-aligned, darker background)
- **ChatInput**: Fixed bottom bar with input field and send button (blue accent)
- **Scrollable Area**: Auto-scroll to latest message

### Runs Grid (Right Panel)
- **RunCard Design**:
  - Run ID badge (top, purple accent)
  - Hyperparameters displayed as key-value pairs
  - Metrics (validation loss, lr) in monospace
  - Status badge (color-coded: running=blue, complete=green, failed=red)
  - "View Plot" button (blue accent, full width at card bottom)

### Plot Viewer Page (`/run/[id]`)
- **Header**: Run metadata (ID, config, status)
- **Main Area**: Plotly.js chart (full width)
- **Dark theme**: Chart background matches `#00143c`, grid lines subtle

## Visual Hierarchy
1. **Primary Actions**: Blue accent buttons (`#00b4f0`)
2. **Status/Badges**: Purple highlights (`#b428ff`)
3. **Content**: White text on dark navy
4. **Secondary Info**: Gray text (60-70% opacity)

## Interaction Patterns
- **Hover States**: Slight brightness increase on cards and buttons
- **Active Runs**: Pulsing indicator on status badge
- **Loading States**: Skeleton screens or spinners in accent blue
- **No animations**: Keep UI snappy and professional, minimal motion

## Images
**No hero images or marketing visuals** - This is a developer tool. Focus on data visualization and content density.

## Accessibility
- Maintain contrast ratios on dark backgrounds
- Keyboard navigation for chat input and run cards
- Screen reader labels for status indicators

## Key Principles
- **Density over whitespace**: ML researchers want information-rich interfaces
- **Dark theme throughout**: Reduce eye strain during long sessions
- **Scannable metrics**: Quick visual parsing of hyperparameters and results
- **Minimal decorative elements**: Function over form