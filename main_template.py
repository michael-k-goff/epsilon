# This script generates data for the template for the main page.

def generate_template():
    return [
        {
            "type":"numeric",
            "default":"5",
            "field_name":"x",
            "text_name":"Rows"
        },
        {
            "type":"numeric",
            "default":"5",
            "field_name":"y",
            "text_name":"Columns"
        },
        {
            "type":"box",
            "field_name":"room_size",
            "text_name":"Room Size",
            "default":"2",
            "choices":["1","2","3","4"],
            "choice_names":["1","2","3","4"]
        },
        {
            "type":"box_text",
            "field_name":"dungeon_shape",
            "text_name":"Dungeon Shape",
            "default":"box",
            "choices":["box","taper","round"],
            "choice_names":["Box","Tapered Tower","Round Tower"]
        },
        {
            "type":"numeric",
            "default":"3",
            "field_name":"z",
            "text_name":"Number of Floors"
        },
        {
            "type":"box_text",
            "field_name":"corridor_preference",
            "text_name":"Corridors",
            "default":"none",
            "choices":["none","long","short","few_stairs"],
            "choice_names":["No Preference","Prefer Long","Prefer Short","Prefer Few Stairs"]
        },
        {
            "type":"button",
            "name":"Generate Map",
            "action":"generate_map(0)"
        },
        {
            "type":"button",
            "name":"Save Map",
            "action":"generate_map(1)"
        }
    ] # Should eventually return a list of data encoding forms