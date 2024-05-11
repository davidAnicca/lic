#!/python3/
import io
import numpy as np
import matplotlib.pyplot as plt

def create_lattice_diagram(sequence):
    grid = np.full((100, 100), '', dtype=str)
    
    
    x, y = 30, 30
    
    directions = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}

    coordinates = []
    
    for step in sequence:
        direction, element = step[0], step[1]
        dx, dy = directions[direction]
        x, y = x + dx, y + dy
        grid[x, y] = element
        coordinates.append((x, y))

    print(coordinates)
    
    all_xs, all_ys = zip(*coordinates)
    
    min_x, max_x = min(all_xs) - 0.5, max(all_xs) + 0.5
    min_y, max_y = min(all_ys) - 0.5, max(all_ys) + 0.5
     

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(min_y, max_y)
    ax.set_ylim(min_x, max_x)
    ax.set_xticks(np.arange(min_y, max_y + 1, 1))
    ax.set_yticks(np.arange(min_x, max_x + 1, 1))
    ax.axis('off')
    
    # Set aspect of the plot to be equal, ensuring the plot is always square
    ax.set_aspect('equal', adjustable='box')

    circle_radius = 0.2
    
    for i in range(100):
        for j in range(100):
            if grid[i, j] != '':
                ax.text(j, i, grid[i, j], ha='center', va='center', fontsize=12, color='black')
                color = 'red' if grid[i, j] == 'H' else 'blue'
                circle = plt.Circle((j, i), circle_radius, color=color, fill=True)
                ax.add_artist(circle)
    
    for k in range(0, len(coordinates) - 1):
        x0, y0 = coordinates[k]
        x1, y1 = coordinates[k+1]
        line_length = np.hypot(x1 - x0, y1 - y0)
        if line_length != 0:
            scale = (line_length - circle_radius * 2) / line_length
            x0_adj = x0 + (x1 - x0) * circle_radius / line_length
            y0_adj = y0 + (y1 - y0) * circle_radius / line_length
            x1_adj = x0 + (x1 - x0) * (1 - circle_radius / line_length)
            y1_adj = y0 + (y1 - y0) * (1 - circle_radius / line_length)
            ax.plot([y0_adj, y1_adj], [x0_adj, x1_adj], 'k-')
    
    for k in range(len(coordinates)):
        for l in range(k + 2, len(coordinates)):  
            x0, y0 = coordinates[k]
            x1, y1 = coordinates[l]
            if grid[x0, y0] == 'H' and grid[x1, y1] == 'H' and ((abs(x0 - x1) == 1 and y0 == y1) or (abs(y0 - y1) == 1 and x0 == x1)):
                line_length = np.hypot(x1 - x0, y1 - y0)
                if line_length != 0:
                    scale = (line_length - circle_radius * 2) / line_length
                    x0_adj = x0 + (x1 - x0) * circle_radius / line_length
                    y0_adj = y0 + (y1 - y0) * circle_radius / line_length
                    x1_adj = x0 + (x1 - x0) * (1 - circle_radius / line_length)
                    y1_adj = y0 + (y1 - y0) * (1 - circle_radius / line_length)
                    ax.plot([y0_adj, y1_adj], [x0_adj, x1_adj], 'k--')

    plt.gca().invert_yaxis()
    buf = io.BytesIO()
    plt.savefig(buf, format='png') 
    plt.close(fig) 
    buf.seek(0) 
    return buf

