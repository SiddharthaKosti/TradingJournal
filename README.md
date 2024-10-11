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
- `app.py`: Main entry point for the application.
- `pages/1_trades.py`: Main application file for managing trades.
- `src/trades_analysis/trade_data.py`: Contains functions for adding and editing trade data.
- `src/trades_analysis/trade_summaries.py`: Functions for generating trade summaries.
- `src/trades_analysis/monthly_profit_graph.py`: Functions for visualizing monthly profit data.
- `src/trades_analysis/yearly_performance.py`: Functions for visualizing yearly performance data.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.

## Roadmap for Upcoming Features
- **Real-time Market Data Integration**: Integrate real-time market data to provide users with up-to-date market insights.

## Feedback and Contributions
If you have any feedback or would like to contribute to the project, please don't hesitate to reach out. You can open an issue or submit a pull request on the project's GitHub page. Your input is invaluable in helping me improve the Trade Data Management app.