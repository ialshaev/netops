from multithreading import Thread


# def send_cmd(device):
#     with IOSXEDriver(
#         host = device["host"],
#         auth_username="cisco",
#         auth_password="cisco",
#         auth_strict_key=False,
#         ssh_config_file=True,
#     ) as conn:
#         response = conn.send_command("show int status")
#         print(response.result)