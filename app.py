# from dash_plots import get_plots
from dash_plots_daterng import get_plots


app = get_plots()
# app = daterng()

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)