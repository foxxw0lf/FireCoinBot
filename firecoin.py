import requests
import json
import time
from datetime import datetime
from colorama import init, Fore, Style

# Define the URLs
load_state_url = 'https://app2.firecoin.app/api/loadState'
click_url = 'https://app2.firecoin.app/api/click'

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def login_with_retry(headers):
    retry_count = 0
    max_retries = 5
    delay_seconds = 5
    data = {}

    
    hijau = Fore.GREEN
    putih = Fore.WHITE
    biru = Fore.BLUE
    merah = Fore.RED
    while retry_count < max_retries:
        try:
            load_state_response = requests.post(load_state_url, headers=headers, json=data)
            if load_state_response.status_code == 200:
                response_json = load_state_response.json()
                user_id = response_json.get('user_id')
                wood = response_json.get('wood', {})
                wood_energy = wood.get('count', 0)
                max_value_wood_energy = wood.get('max_value', 0)
                regen_rate = wood.get('regen', 0)
                bot_multiplier = wood.get('bot', 0)
                tap_multiplier = wood.get('tapmul', 0)
                clicks = response_json.get('clicks', 0)
                clicker_Bonus = response_json.get('clickerBonus', {})
                energy_level = wood.get('max',{})

                print(f'{biru}[{get_timestamp()}{biru}] {putih}=================================================={putih}')
                print(f'{biru}[{get_timestamp()}{biru}] {hijau}+            AUTO TAP-TAP FIRECOIN               +{hijau}')
                print(f'{biru}[{get_timestamp()}{biru}] {putih}=================================================={putih}')
                print(f'{biru}[{get_timestamp()}{biru}] {hijau}+            User ID: {user_id}                  +{hijau}')
                print(f'{biru}[{get_timestamp()}{biru}] {putih}=================================================={putih}')
                print(f'{biru}[{get_timestamp()}{biru}] {hijau}Wood Energy: {wood_energy}/{max_value_wood_energy}{hijau}')
                print(f'{biru}[{get_timestamp()}{biru}] {hijau}Wood Energy Max: {max_value_wood_energy}{hijau}')
                print(f'{biru}[{get_timestamp()}{biru}] {hijau}Bot Level: {bot_multiplier}{hijau}')
                print(f'{biru}[{get_timestamp()}{biru}] {hijau}Tap Level: {tap_multiplier}{hijau}')
                print(f'{biru}[{get_timestamp()}{biru}] {hijau}Recharge Speed Level: {regen_rate}{hijau}')
                print(f'{biru}[{get_timestamp()}{biru}] {hijau}Energy Level: {energy_level}{hijau}')

                print(f'{biru}[{get_timestamp()}{biru}] {putih}=================================================={putih}')
                print(f'{biru}[{get_timestamp()}{biru}] {hijau}FireBot Bonus: {clicker_Bonus}{hijau}')
                print(f'{biru}[{get_timestamp()}{biru}] {hijau}Balance FireCoin: {clicks}{hijau}')


                return {'user_id': user_id, 'wood': wood, 'wood_energy': wood_energy, 'max_value_wood': max_value_wood_energy, 'regen_rate': regen_rate, 'bot_multiplier': bot_multiplier, 'tap_multiplier': tap_multiplier, 'total_clicks_bonus': clicker_Bonus, 'total_clicks': clicks}
            else:
                print(f'{biru}[{get_timestamp()}{biru}]{ merah}=================================================={merah}')
                print(f'{biru}[{get_timestamp()}{biru}] {merah}Failed to load state. Retrying...{merah}')
                retry_count += 1
                print(f'{biru}[{get_timestamp()}{biru}] {merah}Retry attempt {retry_count} in {delay_seconds} seconds...{merah}')
                time.sleep(delay_seconds)
                delay_seconds *= 2
        except requests.RequestException as e:
            print(f'{biru}[{get_timestamp()}{biru}] {merah}=================================================={merah}')
            print(f'{biru}[{get_timestamp()}{biru}] {merah}RequestException occurred during login: {str(e)}{merah}')
            retry_count += 1
            print(f'{biru}[{get_timestamp()}{biru}] {merah}Retry attempt {retry_count} in {delay_seconds} seconds...{merah}')
            time.sleep(delay_seconds)
            delay_seconds *= 2
        except Exception as e:
            print(f'{biru}[{get_timestamp()}{biru}] {merah}=================================================={merah}')
            print(f'{biru}[{get_timestamp()}{biru}] {merah}Exception occurred during login: {str(e)}{merah}')
            retry_count += 1
            print(f'{biru}[{get_timestamp()}{biru}] {merah}Retry attempt {retry_count} in {delay_seconds} seconds...{merah}')
            time.sleep(delay_seconds)
            delay_seconds *= 2
            break
    print(f'{biru}[{get_timestamp()}{biru}] {merah}Maximum retries reached. Aborting.{merah}')

def send_click(headers, tap_multiplier, clicks, wood_energy, max_value_wood_energy, regen_rate):
    hijau = Fore.GREEN
    putih = Fore.WHITE
    biru = Fore.BLUE
    merah = Fore.RED
    try:
        time.sleep(3)
        if wood_energy == 0:
            print(f'{biru}[{get_timestamp()}{biru}] {merah}Wood Energy is 0. Waiting for regeneration...{merah}')
            wait_for_energy_regeneration(wood_energy, max_value_wood_energy, regen_rate)
            return

        total_clicks = clicks + tap_multiplier + wood_energy 
        payload = {'clicks': total_clicks}
        
             
        response = requests.post(click_url, json=payload, headers=headers)
        response.raise_for_status()
        
        response_data = response.json()
        next_user = response_data.get('nextUser')

        print(f'{biru}[{get_timestamp()}{biru}] {putih}=================================================={putih}')
        print(f'{biru}[{get_timestamp()}{biru}] {putih}Tap Success{putih}')
        print(f'{biru}[{get_timestamp()}{biru}] {putih}User: {next_user}{putih}')
        print_updated_data(headers, regen_rate)

        # Introduce a delay between consecutive clicks
        time.sleep(2)  # Adjust the delay time as needed

        return response_data

    except requests.RequestException as e:
        print(f'{biru}[{get_timestamp()}{biru}] {putih}=================================================={putih}')
        print(f'{biru}[{get_timestamp()}{biru}] {merah}RequestException occurred during click: {str(e)}{merah}')
        if e.response is not None:
            print(f'{biru}[{get_timestamp()}{biru}] {merah}Response content: {e.response.content}{merah}')
        # Implement retry logic or handle rate limiting here
        time.sleep(10)  # Example of retry delay, adjust as per server's rate limit
    except Exception as e:
        print(f'[{get_timestamp()}] {putih}=================================================={putih}')
        print(f'[{get_timestamp()}] {merah}Exception occurred during click: {str(e)}{merah}')
        # Implement error handling as per your application's requirements
    print(f'{biru}[{get_timestamp()}{biru}] {merah}Tap Failed.{merah}')

def print_updated_data(headers, regen_rate):
    hijau = Fore.GREEN
    putih = Fore.WHITE
    biru = Fore.BLUE
    merah = Fore.RED
    try:
        load_state_response = requests.post(load_state_url, headers=headers, json={})
        load_state_response.raise_for_status()
        response_json = load_state_response.json()
        
        wood = response_json.get('wood', {})
        wood_energy = wood.get('count', 0)
        max_value_wood_energy = wood.get('max_value', 0)
        clicks = response_json.get('clicks', {})
        clicker_Bonus = response_json.get('clickerBonus', {})

        print(f'{biru}[{get_timestamp()}{biru}] {hijau}Wood Energy Updated: {wood_energy}/{max_value_wood_energy}{hijau}')
        print(f'{biru}[{get_timestamp()}{biru}] {hijau}Balance FireCoin Updated: {clicks}{hijau}')
        #print(f'[{get_timestamp()}] Total Clicks Bonus Updated: {clicker_Bonus}')

        if wood_energy < max_value_wood_energy:
            wait_for_energy_regeneration(wood_energy, max_value_wood_energy, regen_rate)
    except requests.RequestException as e:
        print(f'{biru}[{get_timestamp()}{biru}] {merah}RequestException occurred during fetching updated data: {str(e)}{merah}')
    except Exception as e:
        print(f'{biru}[{get_timestamp()}{biru}] {merah}Exception occurred during fetching updated data: {str(e)}{merah}')

def wait_for_energy_regeneration(current_energy, max_energy, regen_rate):
    hijau = Fore.GREEN
    putih = Fore.WHITE
    biru = Fore.BLUE
    merah = Fore.RED
    if current_energy < max_energy:
        required_time = (max_energy - current_energy) / regen_rate
        print(f'{biru}[{get_timestamp()}{biru}] {merah}Wood Energy is below maximum energy. Waiting for it to regenerate...{merah}')
        print(f'{biru}[{get_timestamp()}{biru}] {merah}Waiting for {required_time} seconds...{merah}')
        time.sleep(required_time)

def read_data_from_file(filename):
    hijau = Fore.GREEN
    putih = Fore.WHITE
    biru = Fore.BLUE
    merah = Fore.RED
    data = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    data[key.strip()] = value.strip()
    except Exception as e:
        print(f'{biru}[{get_timestamp()}{biru}] {merah}Error reading file {filename}: {str(e)}{merah}')
    return data

def main():
    hijau = Fore.GREEN
    putih = Fore.WHITE
    biru = Fore.BLUE
    banner = f"""
    {hijau}AUTO TAP-TAP FIRECOIN {biru} https://t.me/firecoin_app_bot/app?startapp=r_394382178
    
    {putih}By : {hijau}t.me/Anggastwn
    {hijau}Github : {putih}@stwn11
    """
    print(banner)

    data_from_file = read_data_from_file('data.txt')
    headers = {
        'accept': '*/*',
        'accept-language': 'en,en-US;q=0.9,id;q=0.8',
        'authorization': data_from_file.get('authorization', ''),
        'baggage': data_from_file.get('baggage', ''),
        'content-type': 'text/plain;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://app2.firecoin.app',
        'priority': 'u=1, i',
        'referer': 'https://app2.firecoin.app/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': data_from_file.get('sentry-trace', ''),
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }

    login_data = login_with_retry(headers)

    if login_data:
        tap_multiplier = login_data.get('tap_multiplier', 0)
        clicks = login_data.get('total_clicks', 0)
        wood_energy = login_data.get('wood_energy', 0)
        max_value_wood_energy = login_data.get('max_value_wood', 0)
        regen_rate = login_data.get('regen_rate', 0)

        while wood_energy > 0:
            send_click(headers, tap_multiplier, clicks, wood_energy, max_value_wood_energy, regen_rate)
            time.sleep(1)
            updated_data = login_with_retry(headers)
            if updated_data:
                wood_energy = updated_data.get('wood_energy', 0)
                clicks = updated_data.get('total_clicks', 0)

if __name__ == "__main__":
    main()
