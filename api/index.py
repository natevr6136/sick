import requests
import random
from flask import Flask, jsonify, request
import json
import os
import flask
from flask import Flask, request, jsonify
import requests
import random
from flask import Flask, jsonify, request

class GameInfo:
    def __init__(self):
        titleider: str = ""
        secretkey: str = ""

    def GetAuthHeaders(self) -> dict:
        return {
            "content-type": "application/json",
            "X-SecretKey": secretkey
        }

    def GetTitle(self) -> str:
        return titleider

settings: GameInfo = GameInfo()
app: Flask = Flask(__name__)
playfabCache: dict = {}
muteCache: dict = {}

titleider = ""
secretkey = ""

def ReturnFunctionJson(data, funcname, funcparam={}):
    rjson = data["FunctionParameter"]
    userId: str = rjson.get("CallerEntityProfile").get("Lineage").get("TitlePlayerAccountId")

    req = requests.post(
        url=f"https://{titleider}.playfabapi.com/Server/ExecuteCloudScript",
        json={
            "PlayFabId": userId,
            "FunctionName": funcname,
            "FunctionParameter": funcparam
        },
        headers=settings.GetAuthHeaders()
    )

    if req.status_code == 200:
        return jsonify(req.json().get("data").get("FunctionResult")), req.status_code
    else:
        return jsonify({}), req.status_code


@app.route("/", methods=["POST", "GET"])
def main():
    return """
        <html>
            <head>
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
            </head>
            <body style="font-family: 'Inter', sans-serif;">
                <h1 style="color: red; font-size: 10px;">
                   luckily none of this will work for YOU skidder
                </h1>
            </body>
        </html>
    """

    
@app.route("/api/GetAcceptedAgreements", methods=['POST'])
def GetAcceptedAgreements():
    received_data = request.get_json()
    
    return jsonify({"PrivacyPolicy": "2024.09.20", "TOS": "2024.09.20"})

@app.route("/api/SubmitAcceptedAgreements", methods=['POST'])
def SubmitAcceptedAgreements():
    received_data = request.get_json()

    return jsonify({"PrivacyPolicy": "2024.09.20", "TOS": "2024.09.20"})


@app.route("/api/photon", methods=["POST"])
def photonauth():
    print(f"Received {request.method} request at /api/photon")
    getjson = request.get_json()
    Ticket = getjson.get("Ticket")
    Nonce = getjson.get("Nonce")
    Platform = getjson.get("Platform")
    UserId = getjson.get("UserId")
    nickName = getjson.get("username")
    if request.method.upper() == "GET":
        rjson = request.get_json()
        print(f"{request.method} : {rjson}")

        userId = Ticket.split('-')[0] if Ticket else None
        print(f"Extracted userId: {UserId}")

        if userId is None or len(userId) != 16:
            print("Invalid userId")
            return jsonify({
                'resultCode': 2,
                'message': 'Invalid token',
                'userId': None,
                'nickname': None
            })

        if Platform != 'Quest':
            return jsonify({'Error': 'Bad request', 'Message': 'Invalid platform!'}),403

        if Nonce is None:
            return jsonify({'Error': 'Bad request', 'Message': 'Not Authenticated!'}),304

        req = requests.post(
            url=f"https://{titleider}.playfabapi.com/Server/GetUserAccountInfo",
            json={"PlayFabId": userId},
            headers={
                "content-type": "application/json",
                "X-SecretKey": secretkey
            })

        print(f"Request to PlayFab returned status code: {req.status_code}")

        if req.status_code == 200:
            nickName = req.json().get("UserInfo",
                                      {}).get("UserAccountInfo",
                                              {}).get("Username")
            if not nickName:
                nickName = None

            print(
                f"Authenticated user {userId.lower()} with nickname: {nickName}"
            )

            return jsonify({
                'resultCode': 1,
                'message':
                f'Authenticated user {userId.lower()} title {titleider.lower()}',
                'userId': f'{userId.upper()}',
                'nickname': nickName
            })
        else:
            print("Failed to get user account info from PlayFab")
            return jsonify({
                'resultCode': 0,
                'message': "Something went wrong",
                'userId': None,
                'nickname': None
            })

    elif request.method.upper() == "POST":
        rjson = request.get_json()
        print(f"{request.method} : {rjson}")

        ticket = rjson.get("Ticket")
        userId = ticket.split('-')[0] if ticket else None
        print(f"Extracted userId: {userId}")

        if userId is None or len(userId) != 16:
            print("Invalid userId")
            return jsonify({
                'resultCode': 2,
                'message': 'Invalid token',
                'userId': None,
                'nickname': None
            })

        req = requests.post(
             url=f"https://{titleider}.playfabapi.com/Server/GetUserAccountInfo",
             json={"PlayFabId": userId},
             headers={
                 "content-type": "application/json",
                 "X-SecretKey": secretkey
             })

        print(f"Authenticated user {userId.lower()}")
        print(f"Request to PlayFab returned status code: {req.status_code}")

        if req.status_code == 200:
             nickName = req.json().get("UserInfo",
                                       {}).get("UserAccountInfo",
                                               {}).get("Username")
             if not nickName:
                 nickName = None
             return jsonify({
                 'resultCode': 1,
                 'message':
                 f'Authenticated user {userId.lower()} title {titleider.lower()}',
                 'userId': f'{userId.upper()}',
                 'nickname': nickName
             })
        else:
             print("Failed to get user account info from PlayFab")
             successJson = {
                 'resultCode': 0,
                 'message': "Something went wrong",
                 'userId': None,
                 'nickname': None
             }
             authPostData = {}
             for key, value in authPostData.items():
                 successJson[key] = value
             print(f"Returning successJson: {successJson}")
             return jsonify(successJson)
    else:
         print(f"Invalid method: {request.method.upper()}")
         return jsonify({
             "Message":
             "Use a POST or GET Method instead of " + request.method.upper()
         })


def ReturnFunctionJson(data, funcname, funcparam={}):
    print(f"Calling function: {funcname} with parameters: {funcparam}")
    rjson = data.get("FunctionParameter", {})
    userId = rjson.get("CallerEntityProfile",
                       {}).get("Lineage", {}).get("TitlePlayerAccountId")

    print(f"UserId: {userId}")

    req = requests.post(
        url=f"https://{titleider}.playfabapi.com/Server/ExecuteCloudScript",
        json={
            "PlayFabId": userId,
            "FunctionName": funcname,
            "FunctionParameter": funcparam
        },
        headers={
            "content-type": "application/json",
            "X-SecretKey": secretkey
        })

    if req.status_code == 200:
        result = req.json().get("data", {}).get("FunctionResult", {})
        print(f"Function result: {result}")
        return jsonify(result), req.status_code
    else:
        print(f"Function execution failed, status code: {req.status_code}")
        return jsonify({}), req.status_code



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

app = Flask(__name__)

badNames = [
    "NIG", "NIIG", "KKK", "NIGA", "NAZI", "BIGNIG", "BLACKNIG", "NIGAH", "BANANANIG", "NIGIS", "GAYNIG",
    "FAG", "NIGGA", "NIGNIG", "NIGZILLA", "NIGG", "NIGABALLS", "NIGMON", "NIGNOG", "NIGSY", "NIGRE",
    "GORILLANIG", "NIGKEY", "GORNIGA", "DADDYNIGA", "NIGMON", "HITLER", "NIIG", "N1GGA", "N1GA", "NIGR",
    "N1GGA", "N1GA", "N199A", "KKKLORD", "KKKMEMBER", "KKKMAN", "KKKMASTER", "KKKLEADER", "STINKYJEW",
    "NIGAB", "NIGAMO", "NIBBA", "NIGLET", "NIGWERD", "NIGUH", "NIGK", "NIGWARD", "NIQQA", "NIGDIRT", "NI99",
    "MONKENIGA", "NIGAB", "NIGHA", "H1TLER", "HITL3R", "H1TL3R", "KKKOFFICIAL", "NIGBA11S", "SPIDERNIG",
    "NIGSLAVE", "NIGILA", "NIGBALL", "NIGILLA", "SPIDANIGA", "BLACKNIGA", "NIG2MONKE", "NIGMAN", "NIGATOES",
    "NIGMAN", "NIGWAD", "MYNIGA", "NIGTARD", "NIGTURD", "NIGWORD", "NIGLIT", "NIGMAN", "NIGLER", "NIGSBALL",
    "SANDNIG", "SNOWNIG", "NIGQA", "DIRTYNIG", "NIGAFUCK", "HITTLER", "NIGFART", "NIGBA", "N1GWARD", "NIGHKA",
    "LITTLENIG", "NIGAH", "NIGBOB", "MASTERNIG", "NIGBOT", "NIGVR", "WARNIG",
    "NIGGER", "NIGGGER", "NIGERZ", "FAGGOT", "NIGAR", "NIGUR", "NIGG3R", "N1GGER", "N1GG3R", "NIGER",
    "NIGKILL", "NIGASLAYER", "NIGERMON", "NI66ER", "GEORGEFL", "GEORGFL", "NIIGGE", "NIIGGR", "CHINK",
    "N1GUR", "N1GER", "NICKG", "NIKGU", "NIKGE", "N199GE", "GASJEW", "KILLJEW", "JEWSLAYER", "JEWSSUCK",
    "GASTHEJEW", "KIKE", "NIBBER", "NIGOR", "NIGCER", "FUCKBLACK", "NIQQER", "FUCKJEW", "NI99ER", "NATEHIG",
    "FUCKLGBT", "FVCKLGBT", "HATELGBT", "NIG5ER", "IHATEGAY", "IH8GAY", "IH8LGBT", "IH8JEW", "IH8BLACK",
    "NICGER", "NIGQER", "H8NIG", "NIG3ER", "NIG3R", "NIGHER", "IHATENIG", "MONKEYNIG", "NIGEATSKFC",
    "FUCKGAYS", "N199ER", "N1663R", "N1993R", "N166ER", "NIGHUR", "N1G3R", "N1GGGERR", "NIG4R", "NIGEER",
    "NIGYR", "NIGBIGGER", "NIGCKER", "NIGIR", "NIG33R", "KXK", "KKX", "XXK", "KXX", "JMAN", "K9", "GAY9", "SLAVE",
    "H1TLER", "PENIS", "VAGINA", "MAXO", "ELLIOT", "KILLNIGGERS", "PORNHUB", "CHILDPORN", "CP", "DICK", "ANAL",
    "MINI99", "GAYSEX", "RAPE", "PORNO", "LESBIAN", "CUMSLUT", "DEEPTHROAT", "JMANCURLY", "DAISY09", "J3VU", "BOT",
    "TTTPIG", "JMANCURLY", "STATUE", "JMANFAN", "TTT", "MOSA", "H4PKY", "WARNING", "HACKER", "GAYMANCURLY",
    "TTTPIGFAN", "ELLIOTFAN", "H4PKYFAN", "MOSAFAN", "TOP1GROUND", "TOP1FLICK", "PIG", "BRN", "BRNMOSA", "GTC",
    "BODA", "K9", "K9FAN", "MAXOFAN", "ELLIOTJR", "TTTPIGJR", "TTTJR", "PIGJR", "MAXOJR", "JMANJR", "JMANCURLYJR",
    "911", "TERRORIST", "TWINTOWERS", "SKIBIDI", "SKIBIDITOILET", "L1RSONISGAY", "SILLYISGAY", "TOP1", "VMT", "VMTFAN",
    "VMTJR", "TTPIG", "LEMMING", "CJVR", "NIGER", "NIGA", "ALECVR", "GAYPIG", "FUCKNIGGERS", "FUCKNIGGAS", "SAVAFAN", 
    "SAVA", "SAVAJR", "FUCKNIGAS", "NIGA", "NIGGERA", "NIGERA", "SUCKMYDICK", "SAVAFAN", "SAVA", "SAVAVR", "COSMO" # add more if needed lol
]

# result : 1 warns the user
# result : 2 kicks the user from the game
# result : 0 means the name is good

@app.route("/api/CheckForBadName", methods=["POST"])
def Check():
    room = request.get_json().get("FunctionArgument", {}).get("forRoom")
    name = request.get_json().get("FunctionArgument", {}).get("name")

    if name in badNames:
        return jsonify({
            "result": 1
        }), 200
    
    else:
        return jsonify({
            "result": 0
        })


class GameInfo:
    def __init__(self):
        self.TitleId: str = "15C8F2"
        self.SecretKey: str = "KTYWMWWYUEXAHURKEENTRQYXCFFCUQ9ONHSAIATOCBHK4S31X7"
        self.ApiKey: str = "OC|7036679606437134|7b6ae85b607f465a418c7e25db8e0ffa"
        self.DiscordWebhook: str = ""

    def get_auth_headers(self):
        return {"content-type": "application/json", "X-SecretKey": self.SecretKey}


settings = GameInfo()
app = Flask(__name__)


def return_function_json(data, funcname, funcparam={}):
    user_id = data["FunctionParameter"]["CallerEntityProfile"]["Lineage"][
        "TitlePlayerAccountId"
    ]

    response = requests.post(
        url=f"https://{settings.TitleId}.playfabapi.com/Server/ExecuteCloudScript",
        json={
            "PlayFabId": user_id,
            "FunctionName": funcname,
            "FunctionParameter": funcparam,
        },
        headers=settings.get_auth_headers(),
    )

    if response.status_code == 200:
        return (
            jsonify(response.json().get("data").get("FunctionResult")),
            response.status_code,
        )
    else:
        return jsonify({}), response.status_code


@app.route("/", methods=["POST", "GET"])
def main():
    return "thanks tictac"


@app.route("/api/PlayFabAuthentication", methods=["POST"])
def playfab_authentication():
    rjson = request.get_json()
    required_fields = ["CustomId", "Nonce", "AppId", "Platform", "OculusId"]
    missing_fields = [field for field in required_fields if not rjson.get(field)]

    if missing_fields:
        return (
            jsonify(
                {
                    "Message": f"Missing parameter(s): {', '.join(missing_fields)}",
                    "Error": f"BadRequest-No{missing_fields[0]}",
                }
            ),
            400,
        )

    if rjson.get("AppId") != settings.TitleId:
        return (
            jsonify(
                {
                    "Message": "Request sent for the wrong App ID",
                    "Error": "BadRequest-AppIdMismatch",
                }
            ),
            400,
        )

    if not rjson.get("CustomId").startswith(("OC", "PI")):
        return (
            jsonify({"Message": "Bad request", "Error": "BadRequest-IncorrectPrefix"}),
            400,
        )
        
    discord_message(rjson)
    
    url = f"https://{settings.TitleId}.playfabapi.com/Server/LoginWithServerCustomId"
    login_request = requests.post(
        url=url,
        json={
            "ServerCustomId": rjson.get("CustomId"),
            "CreateAccount": True
        },
        headers=settings.get_auth_headers()
    )

    if login_request.status_code == 200:
        data = login_request.json().get("data")
        session_ticket = data.get("SessionTicket")
        entity_token = data.get("EntityToken").get("EntityToken")
        playfab_id = data.get("PlayFabId")
        entity_type = data.get("EntityToken").get("Entity").get("Type")
        entity_id = data.get("EntityToken").get("Entity").get("Id")

        link_response = requests.post(
            url=f"https://{settings.TitleId}.playfabapi.com/Server/LinkServerCustomId",
            json={
                "ForceLink": True,
                "PlayFabId": playfab_id,
                "ServerCustomId": rjson.get("CustomId"),
            },
            headers=settings.get_auth_headers()
        ).json()

        return (
            jsonify(
                {
                    "PlayFabId": playfab_id,
                    "SessionTicket": session_ticket,
                    "EntityToken": entity_token,
                    "EntityId": entity_id,
                    "EntityType": entity_type,
                }
            ),
            200,
        )
    else:
        if login_request.status_code == 403:
            ban_info = login_request.json()
            if ban_info.get("errorCode") == 1002:
                ban_message = ban_info.get("errorMessage", "No ban message provided.")
                ban_details = ban_info.get("errorDetails", {})
                ban_expiration_key = next(iter(ban_details.keys()), None)
                ban_expiration_list = ban_details.get(ban_expiration_key, [])
                ban_expiration = (
                    ban_expiration_list[0]
                    if len(ban_expiration_list) > 0
                    else "No expiration date provided."
                )
                print(ban_info)
                return (
                    jsonify(
                        {
                            "BanMessage": ban_expiration_key,
                            "BanExpirationTime": ban_expiration,
                        }
                    ),
                    403,
                )
            else:
                error_message = ban_info.get(
                    "errorMessage", "Forbidden without ban information."
                )
                return (
                    jsonify({"Error": "PlayFab Error", "Message": error_message}),
                    403,
                )
        else:
            error_info = login_request.json()
            error_message = error_info.get("errorMessage", "An error occurred.")
            return (
                jsonify({"Error": "PlayFab Error", "Message": error_message}),
                login_request.status_code,
            )


@app.route("/api/CachePlayFabId", methods=["POST"])
def cache_playfab_id():
    return jsonify({"Message": "Success"}), 200


@app.route("/api/TitleData", methods=["POST", "GET"])
def title_data():
    response = requests.post(
        url=f"https://{settings.TitleId}.playfabapi.com/Server/GetTitleData",
        headers=settings.get_auth_headers()
    )

    if response.status_code == 200:
        return jsonify(response.json().get("data").get("Data"))
    else:
        return jsonify({}), response.status_code


@app.route("/api/TitleDataQuest", methods=["POST", "GET"])
def titled_data():
    response = requests.post(
        url=f"https://{settings.TitleId}.playfabapi.com/Server/GetTitleData",
        headers=settings.get_auth_headers(),
    )

    if response.status_code == 200:
        response_json = response.json()
        data = response_json.get("data", {}).get("Data", {})
        return jsonify(json.loads(json.dumps(data).replace("\\\\", "\\")))
    else:
        return jsonify({"error": "Failed to fetch data"}), response.status_code


@app.route("/api/CheckForBadName", methods=["POST", "GET"])
def check_for_bad_name():
    return jsonify({"result": 0})


@app.route("/api/GetAcceptedAgreements", methods=["POST", "GET"])
def get_accepted_agreements():
    rjson = request.get_json()["FunctionResult"]
    return jsonify(rjson)


@app.route("/api/UploadGorillanalytics", methods=["POST"])
def Upload_Gorillanalytics():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    function_result = data.get("FunctionResult", {})

    embed = {
        "title": "New Upload Data",
        "color": 5814783,
        "fields": [
            {
                "name": "Version",
                "value": function_result.get("version", "N/A"),
                "inline": True,
            },
            {
                "name": "Upload Chance",
                "value": function_result.get("upload_chance", "N/A"),
                "inline": True,
            },
            {"name": "Map", "value": function_result.get("map", "N/A"), "inline": True},
            {
                "name": "Mode",
                "value": function_result.get("mode", "N/A"),
                "inline": True,
            },
            {
                "name": "Queue",
                "value": function_result.get("queue", "N/A"),
                "inline": True,
            },
            {
                "name": "Player Count",
                "value": str(function_result.get("player_count", "N/A")),
                "inline": True,
            },
            {
                "name": "Position",
                "value": f"({function_result.get('pos_x', 'N/A')}, {function_result.get('pos_y', 'N/A')}, {function_result.get('pos_z', 'N/A')})",
                "inline": False,
            },
            {
                "name": "Velocity",
                "value": f"({function_result.get('vel_x', 'N/A')}, {function_result.get('vel_y', 'N/A')}, {function_result.get('vel_z', 'N/A')})",
                "inline": False,
            },
            {
                "name": "Cosmetics Owned",
                "value": function_result.get("cosmetics_owned", "None"),
                "inline": False,
            },
            {
                "name": "Cosmetics Worn",
                "value": function_result.get("cosmetics_worn", "None"),
                "inline": False,
            },
        ],
    }

    payload = {"embeds": [embed]}
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        f"{settings.DiscordWebhook}",
        json=payload,
        headers=headers,
    )

    if response.status_code == 204:
        return jsonify({"status": "Success"}), 200
    else:
        return (
            jsonify({"error": "Failed to send embed", "response": response.text}),
            500,
        )


@app.route("/api/SubmitAcceptedAgreements", methods=["POST", "GET"])
def submit_accepted_agreements():
    rjson = request.get_json()["FunctionResult"]
    return jsonify(rjson)


@app.route("/api/ConsumeOculusIAP", methods=["POST"])
def consume_oculus_iap():
    rjson = request.get_json()

    access_token = rjson.get("userToken")
    user_id = rjson.get("userID")
    nonce = rjson.get("nonce")
    sku = rjson.get("sku")

    response = requests.post(
        url=f"https://graph.oculus.com/consume_entitlement?nonce={nonce}&user_id={user_id}&sku={sku}&access_token={settings.ApiKey}",
        headers={"content-type": "application/json"},
    )

    if response.json().get("success"):
        return jsonify({"result": True})
    else:
        return jsonify({"error": True})


@app.route("/api/photon/authenticate", methods=["POST"])
def photon_authenticate():
    user_id = request.args.get("username")
    token = request.args.get("token")

    return jsonify({"ResultCode": 1, "UserId": user_id.upper()})


@app.route("/api/photon/authenticate/pcvr", methods=["POST"])
def photon_authenticate_pcvr():
    user_id = request.args.get("username")

    try:
        response = requests.post(
            url=f"https://{settings.TitleId}.playfabapi.com/Server/GetUserAccountInfo",
            json={"PlayFabId": user_id},
            headers={
                "content-type": "application/json",
                "X-SecretKey": f"{settings.SecretKey}",
            },
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify(
            {
                "resultCode": 0,
                "message": f"Something went wrong: {str(e)}",
                "userId": None,
                "nickname": None,
            }
        )

    try:
        user_info = response.json().get("UserInfo", {}).get("UserAccountInfo", {})
        nickname = user_info.get("Username", None)
    except (ValueError, KeyError, TypeError) as e:
        return jsonify(
            {
                "resultCode": 0,
                "message": f"Error parsing response: {str(e)}",
                "userId": None,
                "nickname": None,
            }
        )

    return jsonify({"ResultCode": 1, "UserId": user_id.upper()})
    
def discord_message(message):
  payload = {"content": message}
  headers = {'Content-Type': 'application/json'}
  requests.post(
      f"{settings.DiscordWebhook}", 
      json=payload, 
      headers=headers
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
