import requests
from datetime import datetime, timedelta
import PySimpleGUI as sg
from config import get_api_key

API_KEY = get_api_key()
API_URL = f'https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}'

def get_movies():
    today = datetime.today().date()
    payload = {
        'primary_release_date.gte': today.strftime('%Y-%m-%d'),
        'primary_release_date.lte': (today + timedelta(days=250)).strftime('%Y-%m-%d'),
        'sort_by': 'primary_release_date.asc'
    }
    all_results = []
    page_number = 1
    while len(all_results) < 500:
        payload['page'] = page_number
        response = requests.get(API_URL, params=payload)
        data = response.json()
        results = data.get('results', [])
        if not results:
            break
        all_results.extend(results)
        page_number += 1
    return all_results[:500]

def main():
    sg.theme('DarkGrey13')
    layout = [
        [sg.Text('Najbliższe premiery filmowe', font=('Arial', 20), pad=((10, 10), (10, 10)))],
        [sg.Text('Szukaj: '), sg.InputText(key='search'), sg.Button('Szukaj', key='search_button', size=(20,1))],
        [sg.Table(values=[], headings=['Tytuł', 'Data premiery', 'Dni do premiery'], auto_size_columns=False, col_widths=[40, 20, 15], justification='center', key='output', font=('Arial', 10), num_rows=10, row_height=25, pad=((10, 10), (10, 10)))],
        [sg.Image("tmdb_logo.png")]
    ]

    window = sg.Window('Premiery filmowe i serialowe', layout, resizable=True, size=(800, 600))

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'search_button':
            search_query = values['search']
            movies = get_movies()
            filtered_movies = [movie for movie in movies if search_query.lower() in movie['title'].lower()]
            sorted_movies = sorted(filtered_movies, key=lambda movie: datetime.strptime(movie['release_date'], '%Y-%m-%d'))
            output_data = []
            for movie in sorted_movies:
                days_to_release = (datetime.strptime(movie['release_date'], '%Y-%m-%d').date() - datetime.today().date()).days
                if days_to_release >= 0:
                    output_data.append([movie['title'], movie['release_date'], days_to_release])
            window['output'].update(values=output_data)

    window.close()

if __name__ == '__main__':
    main()
