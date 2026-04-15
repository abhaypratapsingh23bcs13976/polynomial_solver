import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

class PlotService:
    @staticmethod
    def generate_plot(coefficients):
        """
        Generates a premium dark-themed plot of the polynomial and returns it as a base64 encoded string.
        """
        coeffs = np.trim_zeros(coefficients, 'f')
        if not coeffs:
            return None
        
        poly = np.poly1d(coeffs)
        roots = np.roots(coeffs)
        
        # Determine x-range based on real roots
        real_roots = roots[np.isreal(roots)].real
        
        if len(real_roots) > 0:
            x_min = min(real_roots) - 2.5
            x_max = max(real_roots) + 2.5
        else:
            x_min = -10
            x_max = 10
            
        # Generate thousands of points for an ultra-smooth curve
        x = np.linspace(x_min, x_max, 2000)
        y = poly(x)
        
        # --- PREMIUM DARK THEME CONFIGURATION ---
        bg_color = '#18181b' # Matches var(--card-bg) closely in dark mode
        grid_color = '#27272a'
        text_color = '#e2e8f0'
        accent_color = '#8b5cf6' # Primary purple from CSS
        root_color = '#10b981'   # Accent green from CSS

        fig, ax = plt.subplots(figsize=(12, 7), facecolor=bg_color)
        ax.set_facecolor(bg_color)

        # Plot the main curve with a glow effect (multiple layers of decreasing width/alpha)
        ax.plot(x, y, color=accent_color, linewidth=5, alpha=0.2)
        ax.plot(x, y, color=accent_color, linewidth=2.5, alpha=0.9, label='Function Curve')
        
        # Fill area under the curve slightly for depth
        ax.fill_between(x, y, 0, where=(y > 0), color=accent_color, alpha=0.05)
        ax.fill_between(x, y, 0, where=(y < 0), color=accent_color, alpha=0.02)
        
        # Plot real roots
        if len(real_roots) > 0:
            # Add glow to roots
            ax.scatter(real_roots, [0]*len(real_roots), color=root_color, s=200, alpha=0.3, zorder=4)
            ax.scatter(real_roots, [0]*len(real_roots), color=root_color, s=80, edgecolor='white', linewidth=1.5, zorder=5, label='Real Roots')
            
            # Annotate roots
            for root in real_roots:
                ax.annotate(f'{root:.2f}', (root, 0), textcoords="offset points", xytext=(0,12), 
                            ha='center', color='white', fontweight='bold', fontsize=10,
                            bbox=dict(boxstyle="round,pad=0.3", fc=bg_color, ec=root_color, lw=1, alpha=0.8))

        # Stylize Axes
        ax.axhline(0, color='#52525b', linewidth=1.5, zorder=1)
        ax.axvline(0, color='#52525b', linewidth=1.5, zorder=1)
        
        # Grid and borders
        ax.grid(True, linestyle='-', color=grid_color, alpha=0.8, zorder=0)
        for spine in ax.spines.values():
            spine.set_color(grid_color)
            spine.set_linewidth(1.5)
            
        # Ticks styling
        ax.tick_params(colors=text_color, labelsize=10, width=1.5, color=grid_color)
        
        # Labels and Legend
        ax.set_title('Tensor Render: f(x)', fontsize=15, pad=20, color='white', fontweight='bold')
        ax.set_xlabel('X Axis', fontsize=12, color=text_color, fontweight='semibold')
        ax.set_ylabel('Y Axis', fontsize=12, color=text_color, fontweight='semibold')
        
        legend = ax.legend(loc='upper right', frameon=True, shadow=False)
        legend.get_frame().set_facecolor(bg_color)
        legend.get_frame().set_edgecolor(grid_color)
        for text in legend.get_texts():
            text.set_color(text_color)
        
        # Save to buffer tightly
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=150, transparent=False)
        plt.close()
        buf.seek(0)
        
        # Encode as base64
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return image_base64
