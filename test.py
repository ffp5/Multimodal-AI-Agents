import googlemaps
from datetime import datetime

gmaps=googlemaps.Client(key='AIzaSyD6r9ETEBygVtqEEAlcXu7WLMj4fkbhnig')

distance_matrix = gmaps.distance_matrix('New York City', 'Los Angeles', mode='driving')
print(distance_matrix)