import pandas as pd
import plotly.graph_objects as go

# Define the paths
log_file = "/Users/nishanth/lora/loss_function.txt"
save_path = "/Users/nishanth/lora/loss_plot.html"

# Initialize lists to store data
train_iterations = []
train_losses = []

# Read data from log file
with open(log_file, 'r') as file:
    for line in file:
        if "Train loss" in line:
            iteration = int(line.split(':')[0].split(' ')[1])
            train_loss = float(line.split('Train loss ')[1].split(',')[0])
            train_iterations.append(iteration)
            train_losses.append(train_loss)

# Create DataFrame
train_data = {'Iteration': train_iterations, 'Train Loss': train_losses}
train_df = pd.DataFrame(train_data)

# Create figure
fig = go.Figure()

# Add trace for training loss
fig.add_trace(go.Scatter(x=train_df['Iteration'], y=train_df['Train Loss'], mode='lines', name='Train Loss'))

# Update layout
fig.update_layout(title='Training Loss over Iterations',
                  xaxis_title='Iteration',
                  yaxis_title='Loss',
                  hovermode='closest')

# Save the plot as an interactive HTML file
fig.write_html(save_path)

# Show message
print("Plot saved as", save_path)
