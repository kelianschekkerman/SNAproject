# import os
# import pytz
# import json

# charlie = 'charliehebdo'
# german_airplane = 'germanwings-crash'
# putin = 'putinmissing'

# # Pick a folder
# # FOLDER = charlie
# FOLDERS = {
#     'charliehebdo',
#     'germanwings-crash',
#     'putinmissing',
# }

# current_directory = os.getcwd()

# timezones = []
# Walk through the directory
# for FOLDER in FOLDERS:
#     for root, dirs, files in os.walk(current_directory):
#         if FOLDER in root:
#             if "source-tweet" in root or "reactions" in root:
#                 for file in files:
#                     file_path = os.path.join(root, file)
#                     with open(file_path, 'r') as file:
#                         data = json.load(file)
#                         id = data["id_str"]
                        
#                         created_at = data["created_at"]
#                         user_data = data.get('user', {})  # Get 'user' data, or an empty dict if it doesn't exist
#                         time_zone = user_data.get('time_zone', 'NaN')
#                         # print(f"{id} : {created_at}, {time_zone}\n")
#                         if time_zone not in timezones and time_zone is not None:
#                             timezones.append(time_zone)

timezone_map = {
        "Pacific Time (US & Canada)": "US/Pacific",
        "Athens": "Europe/Athens",
        "Greenland": "America/Godthab",
        "Brussels": "Europe/Brussels",
        "London": "Europe/London",
        "Warsaw": "Europe/Warsaw",
        "Vienna": "Europe/Vienna",
        "Bern": "Europe/Zurich",
        "Arizona": "America/Phoenix",
        "Moscow": "Europe/Moscow",
        "Baghdad": "Asia/Baghdad",
        "Volgograd": "Europe/Volgograd",
        "Central Time (US & Canada)": "US/Central",
        "Eastern Time (US & Canada)": "US/Eastern",
        "New Caledonia": "Pacific/Noumea",
        "Quito": "America/Guayaquil",
        "Atlantic Time (Canada)": "America/Halifax",
        "Hawaii": "Pacific/Honolulu",
        "Nairobi": "Africa/Nairobi",
        "Kyiv": "Europe/Kyiv",
        "Mountain Time (US & Canada)": "US/Mountain",
        "Abu Dhabi": "Asia/Dubai",
        "Amsterdam": "Europe/Amsterdam",
        "Auckland": "Pacific/Auckland",
        "Beijing": "Asia/Shanghai",
        "Belgrade": "Europe/Belgrade",
        "Berlin": "Europe/Berlin",
        "Brisbane": "Australia/Brisbane",
        "Budapest": "Europe/Budapest",
        "Caracas": "America/Caracas",
        "Casablanca": "Africa/Casablanca",
        "Chennai": "Asia/Kolkata",
        "Copenhagen": "Europe/Copenhagen",
        "Darwin": "Australia/Darwin",
        "Dublin": "Europe/Dublin",
        "Edinburgh": "Europe/London",
        "Harare": "Africa/Harare",
        "Hawaii": "Pacific/Honolulu",
        "Hong Kong": "Asia/Hong_Kong",
        "Indiana (East)": "America/New_York",
        "Irkutsk": "Asia/Irkutsk",
        "Islamabad": "Asia/Karachi",
        "Istanbul": "Europe/Istanbul",
        "Jakarta": "Asia/Jakarta",
        "Jerusalem": "Asia/Jerusalem",
        "Kabul": "Asia/Kabul",
        "Karachi": "Asia/Karachi",
        "Kathmandu": "Asia/Kathmandu",
        "Krasnoyarsk": "Asia/Krasnoyarsk",
        "Kuala Lumpur": "Asia/Kuala_Lumpur",
        "La Paz": "America/La_Paz",
        "Lima": "America/Lima",
        "Lisbon": "Europe/Lisbon",
        "Ljubljana": "Europe/Ljubljana",
        "Madrid": "Europe/Madrid",
        "Mazatlan": "America/Mazatlan",
        "Melbourne": "Australia/Melbourne",
        "Minsk": "Europe/Minsk",
        "Mumbai": "Asia/Kolkata",
        "Nairobi": "Africa/Nairobi",
        "New Delhi": "Asia/Kolkata",
        "Novosibirsk": "Asia/Novosibirsk",
        "Nuku'alofa": "Pacific/Tongatapu",
        "Paris": "Europe/Paris",
        "Perth": "Australia/Perth",
        "Prague": "Europe/Prague",
        "Pretoria": "Africa/Johannesburg",
        "Riyadh": "Asia/Riyadh",
        "Rome": "Europe/Rome",
        "Santiago": "America/Santiago",
        "Saskatchewan": "America/Regina",
        "Singapore": "Asia/Singapore",
        "Stockholm": "Europe/Stockholm",
        "Sydney": "Australia/Sydney",
        "Tehran": "Asia/Tehran",
        "Tijuana": "America/Tijuana",
        "Tokyo": "Asia/Tokyo",
        "Ulaan Bataar": "Asia/Ulaanbaatar",
        "Vienna": "Europe/Vienna",
        "Volgograd": "Europe/Volgograd",
        "Wellington": "Pacific/Auckland",
        "West Central Africa": "Africa/Lagos",
        "Yakutsk": "Asia/Yakutsk",
        "Bangkok": "Asia/Bangkok",
        "Bogota": "America/Bogota",
        "Brasilia": "America/Sao_Paulo",
        "Buenos Aires": "America/Argentina/Buenos_Aires",
        "Cairo": "Africa/Cairo",
        "Canberra": "Australia/Canberra",
        "Dublin": "Europe/Dublin",
        "International Date Line West": "Pacific/Midway",
        "Europe/London": "Europe/London",
        "Asia/Kolkata": "Asia/Kolkata",
        "Alaska": "America/Anchorage",
        "Africa/Nairobi": "Africa/Nairobi",
        "Bucharest": "Europe/Bucharest",
        "Adelaide": "Australia/Adelaide",
        "Mid-Atlantic": "America/New_York",
        "America/New_York": "America/New_York",
        "Australia/Adelaide": "Australia/Adelaide"   
    }
