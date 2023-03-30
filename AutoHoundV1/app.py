from flask import Flask, request, render_template
from autotrader_scraper import get_carlinks, autotrader_data, get_all_cardata, csv_to_car_data

app = Flask(__name__)

# Configures the app to serve static files
app.static_folder = 'static'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        autotrader_url = request.form['autotrader_url']
        #page_links = get_all_cardata(autotrader_url)
        car_data_list = []
        car_data_list = csv_to_car_data("scorpio.csv")

        # Correct code for scraping
        # for link in page_links:
        #     try:
        #         car_data = autotrader_data(link)
        #         car_data_list.append(car_data)
        #         print(car_data_list)
        #     except Exception as e:
        #         print(f"Error scraping data for link: {link}. Error message: {str(e)}")


        return render_template('result.html', car_data_list=car_data_list)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

# NB NB NB uncomment the code which works for the scraper and remove line 12 car_data_list = csv_to_car_data("hiluxD4D.csv") as this is dud data