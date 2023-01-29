import datetime
import time
from colorama import Fore
import requests
import random

ratelimit = 1

def check_token():
    check_token = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": f"{TOKEN}"})
    if check_token.status_code == 200:
        print(Fore.GREEN + "Token is valid")
    else:
        print(Fore.RED + "Token is invalid")
        exit()

def nonce():
        date = datetime.datetime.now()
        unixts = time.mktime(date.timetuple())
        return str((int(unixts)*1000-1420070400000)*4194304)


ascii = "██████╗░░█████╗░████████╗  ███╗░░██╗██╗░░░██╗██╗░░██╗███████╗██████╗░\n██╔══██╗██╔══██╗╚══██╔══╝  ████╗░██║██║░░░██║██║░██╔╝██╔════╝██╔══██╗\n██████╦╝██║░░██║░░░██║░░░  ██╔██╗██║██║░░░██║█████═╝░█████╗░░██████╔╝\n██╔══██╗██║░░██║░░░██║░░░  ██║╚████║██║░░░██║██╔═██╗░██╔══╝░░██╔══██╗\n██████╦╝╚█████╔╝░░░██║░░░  ██║░╚███║╚██████╔╝██║░╚██╗███████╗██║░░██║\n╚═════╝░░╚════╝░░░░╚═╝░░░  ╚═╝░░╚══╝░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝"
print(Fore.LIGHTGREEN_EX + ascii)
TOKEN = input(Fore.LIGHTGREEN_EX + "Enter your token: ")
check_token()

def send_message_to_all():
    message = input(Fore.LIGHTGREEN_EX + "Enter your message: ")

    people_to_dm = []

    dms_response = requests.get("https://discord.com/api/v9/users/@me/channels", headers={"Authorization": f"{TOKEN}"})


    dms_data = dms_response.json()
    i = 0
    for channel in dms_data:
        for recipient in dms_data[i]["recipients"]:
            people_to_dm.append(recipient["id"])
        i += 1


    friends_response = requests.get("https://discord.com/api/v9/users/@me/relationships", headers={"Authorization": f"{TOKEN}"})
    friends_data = friends_response.json()
    for friend in friends_data:
        if not friend['id'] in people_to_dm:
            people_to_dm.append(friend['id'])


    for person_to_dm in people_to_dm:

        open_channel = requests.post("https://discord.com/api/v9/users/@me/channels", json={"recipients": [person_to_dm]}, headers={"Authorization": f"{TOKEN}", "Content-Type": "application/json"})
        channel_id = open_channel.json()["id"]
        username = open_channel.json()["recipients"][0]["username"]
        discriminator = open_channel.json()["recipients"][0]["discriminator"]

        send_dm = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers={"Authorization": f"{TOKEN}", "Content-Type": "application/json"}, json={"content": f"{message}", "tts": False, "nonce": nonce()})

        if send_dm.status_code == 200:
            print(Fore.GREEN + f"Successfully sent dm to {username}#{discriminator}")
        else:
            print(Fore.RED + f"Failed to dm {username}#{discriminator}")
        time.sleep(ratelimit)

def remove_all_friends():
    friends = []

    friends_response = requests.get("https://discord.com/api/v9/users/@me/relationships", headers={"Authorization": f"{TOKEN}"})
    friends_data = friends_response.json()
    for friend in friends_data:
        friends.append(friend['id'])

    for friend in friends:
        remove_friend = requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{friend}", headers={"Authorization": f"{TOKEN}"})
        print(remove_friend.text)
        if remove_friend.status_code == 204:
            print(Fore.GREEN + f"Successfully removed friend with id {friend}")
        else:
            print(Fore.RED + f"Failed to remove friend with id {friend}")
        time.sleep(ratelimit)

def close_all_dms():
    open_dms = []
    dms_response = requests.get("https://discord.com/api/v9/users/@me/channels", headers={"Authorization": f"{TOKEN}"})

    dms_data = dms_response.json()
    i = 0
    for channel in dms_data:
        for recipient in dms_data[i]["recipients"]:
            open_dms.append(recipient["id"])
        i += 1

    for dm in open_dms:
        open_channel = requests.post("https://discord.com/api/v9/users/@me/channels", json={"recipients": [dm]}, headers={"Authorization": f"{TOKEN}", "Content-Type": "application/json"})
        channel_id = open_channel.json()["id"]
        username = open_channel.json()["recipients"][0]["username"]
        discriminator = open_channel.json()["recipients"][0]["discriminator"]
        close_dm = requests.delete(f"https://discord.com/api/v9/channels/{channel_id}?silent=false", headers={"Authorization": f"{TOKEN}"})
        if close_dm.status_code == 200:
            print(Fore.GREEN + f"Successfully closed dm with id {username}#{discriminator}")
        else:
            print(Fore.RED + f"Failed to close dm with id {username}#{discriminator}")
        time.sleep(ratelimit)

def leave_all_servers():
    servers_response = requests.get("https://discord.com/api/v9/users/@me/guilds", headers={"Authorization": f"{TOKEN}"})
    servers_data = servers_response.json()
    for server in servers_data:
        delete_server = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{server['id']}", headers={"Authorization": f"{TOKEN}"})
        if delete_server.status_code == 204:
            print(Fore.GREEN + f"Successfully left server {server['name']}")
        else:
            print(Fore.RED + f"Failed to leave server {server['name']}")
        time.sleep(ratelimit)

def spam_create_servers():
    server_name = input(Fore.LIGHTGREEN_EX + "Enter the name of the server you want to spam: ")
    server_count = int(input(Fore.LIGHTGREEN_EX + "Enter the amount of servers you want to spam: "))
    i = 0
    for i in range(server_count):
        i+=1
        create_server = requests.post("https://discord.com/api/v9/guilds", headers={"Authorization": f"{TOKEN}"}, json={"name": f"{server_name}", "region": "europe", "icon": None, "channels": None})
        if create_server.status_code == 201:
            print(Fore.GREEN + f"Successfully created server {server_name} ({i})")
        else:
            print(Fore.RED + f"Failed to create server {server_name} ({i})")
            print(create_server.json())
            print(create_server.status_code)
        time.sleep(ratelimit)

def spam_light_dark_mode():
    for i in range(100):
        print(Fore.LIGHTGREEN_EX + "Warning: High Ratelimit (12 seconds)")
        light_mode = requests.patch("https://discord.com/api/v9/users/@me/settings-proto/1", headers={"Authorization": f"{TOKEN}"}, json={"settings": "agQIAhAB"})
        if light_mode.status_code == 200:
            print(Fore.GREEN + "Successfully changed to light mode")
        else:
            print(Fore.RED + "Failed to change to light mode")
        time.sleep(12)
        dark_mode = requests.patch("https://discord.com/api/v9/users/@me/settings-proto/1", headers={"Authorization": f"{TOKEN}"}, json={"settings": "agQIARAB"})
        if dark_mode.status_code == 200:
            print(Fore.GREEN + "Successfully changed to dark mode")
        else:
            print(Fore.RED + "Failed to change to dark mode")
        time.sleep(12)

def spam_change_language():
    languages = ["YhMKBAoCZGESCwjE//////////8B", "YhMKBAoCZGUSCwjE//////////8B", "YhYKBwoFZW4tR0ISCwjE//////////8B", "YhYKBwoFZW4tVVMSCwjE//////////8B", "YhYKBwoFZXMtRVMSCwjE//////////8B", "YhMKBAoCZnISCwjE//////////8B", "YhMKBAoCbmwSCwjE//////////8B", "YhMKBAoCbm8SCwjE//////////8B", "YhMKBAoCY3MSCwjE//////////8B", "YhMKBAoCZWwSCwjE//////////8B", "YhMKBAoCdGgSCwjE//////////8B", "YhYKBwoFemgtQ04SCwjE//////////8B", "YhMKBAoCa28SCwjE//////////8B"]
    for i in range(100):
        change_lang = requests.patch("https://discord.com/api/v9/users/@me/settings-proto/1", headers={"Authorization": f"{TOKEN}"}, json={"settings": f"{random.choice(languages)}"})
        if change_lang.status_code == 200:
            print(Fore.GREEN + "Successfully changed language")
        else:
            print(Fore.RED + "Failed to change language")
        time.sleep(12)
        i+=1

def get_account_info():
    print(Fore.LIGHTGREEN_EX + "Getting account information...")
    user_info = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": f"{TOKEN}"})
    user_info_data = user_info.json()
    print(Fore.LIGHTGREEN_EX + "Account Information: ")
    print(Fore.LIGHTGREEN_EX + f"Username: {user_info_data['username']}#{user_info_data['discriminator']}")
    print(Fore.LIGHTGREEN_EX + f"ID: {user_info_data['id']}")
    print(Fore.LIGHTGREEN_EX + f"Email: {user_info_data['email']}")
    print(Fore.LIGHTGREEN_EX + f"Phone: {user_info_data['phone']}")
    print(Fore.LIGHTGREEN_EX + f"2FA: {user_info_data['mfa_enabled']}")
    print(Fore.LIGHTGREEN_EX + f"Verified: {user_info_data['verified']}")
    print(Fore.LIGHTGREEN_EX + f"Locale: {user_info_data['locale']}")
    print(Fore.LIGHTGREEN_EX + f"Flags: {user_info_data['flags']}")
    print(Fore.LIGHTGREEN_EX + f"Premium Type (Nitro): {user_info_data['premium_type']}")
    print(Fore.LIGHTGREEN_EX + f"Public Flags: {user_info_data['public_flags']}")
    print(Fore.LIGHTGREEN_EX + f"Banner: {user_info_data['banner']}")
    print(Fore.LIGHTGREEN_EX + f"Banner Color: {user_info_data['banner_color']}")
    print(Fore.LIGHTGREEN_EX + f"Accent Color: {user_info_data['accent_color']}")
    print(Fore.LIGHTGREEN_EX + f"Bio: {user_info_data['bio']}")
    print(Fore.LIGHTGREEN_EX + f"NSFW Allowed: {user_info_data['nsfw_allowed']}")
    print(Fore.LIGHTGREEN_EX + f"Avatar: {user_info_data['avatar']}")
    print(Fore.LIGHTGREEN_EX + f"Avatar decoration: {user_info_data['avatar_decoration']}")


def delete_own_servers():
    user_info = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": f"{TOKEN}"})
    user_info_data = user_info.json()
    if user_info_data['mfa_enabled']:
        print(Fore.LIGHTGREEN_EX + "2FA is enabled on your account, please disable it to use this feature")
    else:
        servers_response = requests.get("https://discord.com/api/v9/users/@me/guilds", headers={"Authorization": f"{TOKEN}"})
        servers_data = servers_response.json()
        ids_with_owner_true = [item["id"] for item in servers_data if item["owner"]]
        for i in ids_with_owner_true:
            delete_server = requests.post(f"https://discord.com/api/v9/guilds/{i}/delete", headers={"Authorization": f"{TOKEN}"})
            if delete_server.status_code == 204:
                print(Fore.GREEN + f"Successfully deleted server with id {i}")
            else:
                print(Fore.RED + f"Failed to delete server with id {i}")
                print(delete_server.json())


def choose_option():
    print(Fore.LIGHTGREEN_EX + "Choose an option: ")
    print(Fore.LIGHTGREEN_EX + "1. Send a message to all your friends and dms")
    print(Fore.LIGHTGREEN_EX + "2. Remove all your friends")
    print(Fore.LIGHTGREEN_EX + "3. Close all your dms")
    print(Fore.LIGHTGREEN_EX + "4. Leave all your servers")
    print(Fore.LIGHTGREEN_EX + "5. Spam create servers")
    print(Fore.LIGHTGREEN_EX + "6. Spam light/dark mode")
    print(Fore.LIGHTGREEN_EX + "7. Spam change language")
    print(Fore.LIGHTGREEN_EX + "8. Get Information about your account")
    print(Fore.LIGHTGREEN_EX + "9. Delete own servers")
    print(Fore.LIGHTGREEN_EX + "10. Everything")
    option = input(Fore.LIGHTGREEN_EX + "Enter your option: ")
    match option:
        case "1":
            send_message_to_all()
        case "2":
            remove_all_friends()
        case "3":
            close_all_dms()
        case "4":
            leave_all_servers()
        case "5":
            spam_create_servers()
        case "6":
            spam_light_dark_mode()
        case "7":
            spam_change_language()
        case "8":
            get_account_info()
        case "9":
            delete_own_servers()
        case "10":
            get_account_info()
            send_message_to_all()
            remove_all_friends()
            close_all_dms()
            leave_all_servers()
            delete_own_servers()
            spam_create_servers()
            spam_change_language()
            spam_light_dark_mode()
        case _:
            print(Fore.RED + "Invalid option")
choose_option()