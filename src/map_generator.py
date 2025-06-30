import folium
import json

def create_interactive_map_with_pins(processed_articles: list) -> None:
    """
    Generates an interactive Folium map with custom markers that display
    expandable "dropdown" information when clicked.

    The map is saved as an HTML file which can be opened in any web browser.
    """

    # Define Map Center and Initial Zoom
    initial_location = [50.0, 10.0]
    initial_zoom = 5
    m = folium.Map(location=initial_location, zoom_start=initial_zoom, tiles="CartoDB Positron")

    # Add Pins to the Map
    for article_data in processed_articles:
        article_data = json.loads(article_data)
        title = article_data["title"]
        coords = article_data["coords"]
        info = article_data["info"]

        # Create the HTML content for the popup.
        # We use the <details> and <summary> tags to create an expandable section.
        # The 'style' attribute is added for basic visual appeal within the popup.
        popup_html = f"""
        <div style="width: 250px; font-family: 'Inter', sans-serif; padding: 5px;">
            <h4 style="margin-top: 0; margin-bottom: 8px; color: #333; font-weight: bold;">{title}</h4>
            <details style="border: 1px solid #ccc; border-radius: 5px; padding: 8px; background-color: #f9f9f9;">
                <summary style="font-weight: bold; cursor: pointer; color: #007bff;">Click for Details</summary>
                <ul style="list-style-type: none; padding: 0; margin-top: 10px;">
        """
        for key, value in info.items():
            popup_html += f"""
                    <li style="margin-bottom: 5px;">
                        <strong style="color: #555;">{key}:</strong> {value}
                    </li>
            """
        popup_html += """
                </ul>
            </details>
        </div>
        """

        # Create a Folium Popup object with the HTML content
        # The 'max_width' ensures the popup doesn't get too wide.
        popup = folium.Popup(popup_html, max_width=300)

        # Create a Folium Marker and add it to the map
        # 'tooltip' shows text when hovering over the marker
        folium.Marker(
            location=coords,
            popup=popup,
            tooltip=title,
            icon=folium.Icon(color="red", icon="info-sign") # Custom icon for the pin
        ).add_to(m)

    # --- 4. Save the Map to an HTML File ---
    output_filename = "interactive_map.html"
    m.save(output_filename)
    print(f"Map saved to {output_filename}")

# --- Execute the function to create the map ---
if __name__ == "__main__":
    create_interactive_map_with_pins()