# Trade Data Management App

## Overview
The Trade Data Management app is a Streamlit application designed to help users efficiently manage and analyze their trading data. It provides functionalities to add/edit trades, view summaries, and analyze monthly and yearly performance.

## Features
- **Add/Edit Trades**: Input new trades or modify existing ones.
- **View Trade Summaries**: Get an overview of trading performance, including total profits and open trades.
- **Analyze Monthly Profits**: Visualize profit trends over time with interactive graphs.
- **Track Yearly Performance**: Assess yearly profit performance with bar charts.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have the necessary CSV file for trade data in the specified path.

## Usage
Run the Streamlit app using the following command:


Open your web browser and navigate to `http://localhost:8501` to access the app.

## File Structure
- `pages/1_trades.py`: Main application file for managing trades.
- `trades_data.py`: Contains functions for adding and editing trade data.
- `trade_summaries.py`: Functions for generating trade summaries.
- `monthly_profit_graph.py`: Functions for visualizing monthly profit data.
- `yearly_performance.py`: Functions for visualizing yearly performance data.
- `app.py`: Main entry point for the application.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.