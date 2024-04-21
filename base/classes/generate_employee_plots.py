import uuid

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Zdefiniuj własną paletę ciemnoniebieskich kolorów
dark_blue_palette = [
    '#f1dac4',  # Beige
    '#a69cac',  # Lilac
    '#474973',  # Dark Slate Blue
    '#161b33',  # Dark Blue
    '#0d0c1d',  # Even Darker Blue
    '#005073',  # Metallic Blue
]


class GenerateEmployeePlots:
    def __init__(self, employee_id, file_path):
        self.employee_id = employee_id
        self.file_path = file_path
        self.data = None
        self.filtered_data = None

    def load_data(self):
        # Loading data from a CSV file
        self.data = pd.read_csv(self.file_path)
        # Filtering data based on the employee ID
        self.filtered_data = self.data[self.data['id'] == self.employee_id]

    def create_combined_plot(self):

        if self.filtered_data is None:
            print("Data not loaded. Call load_data() first.")
            return

        # Transform data for the bar plot
        melted_data = pd.melt(self.filtered_data, id_vars=['id'], value_vars=[
            'Missing abstract method implementations',
            'Diamond inheritance problem',
            'Not using the super() function',
            'Problem with the polymorphism',
            'Static variable issue',
            'Complex inheritance hierarchy'
        ], var_name='Category', value_name='Value')

        # Prepare data for the scatter plot
        cols = [
            'Diamond inheritance problem',
            'Not using the super() function',
            'Problem with the polymorphism',
            'Static variable issue',
            'Complex inheritance hierarchy'
        ]
        x_values = self.filtered_data[cols].values[0]
        max_value = self.filtered_data[cols].max(axis=1).values[0]
        mean_value = self.filtered_data[cols].mean(axis=1).values[0]
        y_values = (x_values * max_value - 0.5 * mean_value) / self.filtered_data['file_counter'].values[0]
        scatter_data = pd.DataFrame({
            'Category': cols,
            'x': x_values,
            'y': y_values
        })

        # Calculate regression line parameters
        A = np.vstack([scatter_data['x'], np.ones(len(scatter_data['x']))]).T
        m, c = np.linalg.lstsq(A, scatter_data['y'], rcond=None)[0]

        # Create subplot layout
        fig = make_subplots(rows=1, cols=2, subplot_titles=('Bar Plot', 'Scatter Plot'))

        # Add bar plot
        for idx, category in enumerate(melted_data['Category']):
            fig.add_trace(
                go.Bar(x=[category], y=[melted_data['Value'].iloc[idx]],
                       name=category,
                       marker=dict(color=dark_blue_palette[idx])),
                row=1, col=1
            )

        # Add scatter plot without text labels
        for idx, category in enumerate(scatter_data['Category']):
            fig.add_trace(
                go.Scatter(x=[scatter_data['x'].iloc[idx]], y=[scatter_data['y'].iloc[idx]], mode='markers',
                           name=category,
                           marker=dict(color=dark_blue_palette[idx]),
                           showlegend=False),
                row=1, col=2
            )

        # Add a line of best fit for scatter plot with a very thin line
        fig.add_trace(
            go.Scatter(
                x=scatter_data['x'],
                y=m * scatter_data['x'] + c,
                mode='lines',
                name='Regression Line',
                line=dict(color='black', width=1),  # Make the regression line very thin
            ),
            row=1, col=2
        )

        # Update x-axis for bar plot to not show tick labels
        fig.update_xaxes(showticklabels=False, row=1, col=1)

        # Update layout
        fig.update_layout(
            height=500,
            width=1000,
            title_text=f'Combined Plots for Employee ID: {self.employee_id}',
            barmode='group',
            legend_title_text='Category',
            paper_bgcolor='rgb(233,233,233)',  # setting background color to light grey
            plot_bgcolor='rgb(233,233,233)'  # setting plot background color to light grey
        )

        fig.show()


def get_mac_address():
    # Pobiera unikalny adres MAC urządzenia
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i + 2] for i in range(0, 12, 2))


# Usage of the class
file_path = '../../data/user_analysis.csv'
# employee_id = 1.0  # Example employee ID
plot_generator = GenerateEmployeePlots(get_mac_address(), file_path)
plot_generator.load_data()
plot_generator.create_combined_plot()
