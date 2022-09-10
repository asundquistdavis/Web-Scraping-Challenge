from datetime import datetime as dt

def scrape_mars():
    mars_data = {}
    hemispheres_dict = [{'title': 'Cerberus Hemisphere', 'url': 'https://marshemispheres.com/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg'}, {'title': 'Schiaparelli Hemisphere', 'url': 'https://marshemispheres.com/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg'}, {'title': 'Syrtis Major Hemisphere', 'url': 'https://marshemispheres.com/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg'}, {'title': 'Valles Marineris Hemisphere', 'url': 'https://marshemispheres.com/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg'}]
    mars_data['news'] = {'title': 'Title', 'body': 'Body'}
    mars_data['image'] = 'url'
    mars_data['facts'] = {'mars': [], 'earth': []}
    mars_data['hemispheres'] = hemispheres_dict
    mars_data['time'] = dt.now()
    return mars_data