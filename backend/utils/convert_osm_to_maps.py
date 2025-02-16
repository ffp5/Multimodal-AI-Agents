def convert_osm_to_maps(osm_url):
    """
    Convertit un lien OpenStreetMap en lien Google Maps fonctionnel.
    
    Args:
        osm_url (str): URL OpenStreetMap (format: https://www.openstreetmap.org/#map=zoom/lat/lon)
    
    Returns:
        str: URL Google Maps
    """
    try:
        # Extraire les coordonnées du lien OSM
        parts = osm_url.split('/')
        if '#map=' in osm_url:
            lat = parts[-2]
            lon = parts[-1]
            
            # Créer le lien Google Maps avec le format correct
            # On utilise le format "?q=lat,lon" qui est plus fiable
            gmaps_url = f"https://www.google.com/maps?q={lat},{lon}"
            return gmaps_url
        else:
            raise ValueError("Format d'URL OpenStreetMap invalide")
            
    except Exception as e:
        return f"Erreur lors de la conversion : {str(e)}"

if __name__ == "__main__":
    # Exemple d'utilisation
    osm_link = "https://www.openstreetmap.org/#map=15/48.8584/2.2945"
    gmaps_link = convert_osm_to_maps(osm_link)
    print(gmaps_link)