import json
from flask import Flask, Response, request
from bson import json_util
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config[
    "MONGO_URI"] = "mongodb+srv://chainAI:chain.ai@clusterrevenuechain.wi8m2.mongodb.net/zcash?retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route("/", methods=["GET"])
def base():
    return Response(response=json.dumps({"status": "ok"}),
                    status=200,
                    mimetype="application/json")


@app.route("/signUp/wallet", methods=["POST"])
def signUpWallet():
    data = mongo.db.wallet_user

    firstName = request.json["first_name"]
    middleName = request.json["middle_name"]
    lastName = request.json["last_name"]
    emailAddress = request.json["email_address"]
    mobileNumber = request.json["mobile_number"]
    nidNumber = request.json["nid_number"]
    walletID = request.json["wallet_id"]
    amount = request.json["amount"]
    userPin = request.json["pin"]
    accountType = request.json["account_type"]

    # check user existing Status using two fields mobile number and nid number

    response = data.find_one({"mobNo": {"$eq": mobileNumber}, "nidNo": {"$eq": nidNumber}})
    output = json_util.dumps(response)

    if mobileNumber and nidNumber in output:
        return "user already exist"
    else:
        createProfile = data.insert_one({"first_name": firstName, "middle_name": middleName, "last_name": lastName,
                                         "email_address": emailAddress, "mobile_number": mobileNumber,
                                         "nid_number": nidNumber, "wallet_id": walletID, "amount": amount,
                                         "pin": userPin, "account_type": accountType})
        # output = {'Status': 'Successfully Inserted', 'Document_ID': str(createProfile.inserted_id)}
        output = json_util.dumps(createProfile.inserted_id)

        return output


@app.route("/signIn/wallet", methods=["POST"])
def signInWallet():
    data = mongo.db.wallet_user

    mobileNumber = request.json["mobile_number"]
    userPin = request.json["pin"]

    # check user existing Status using two fields mobile number and nid number

    response = data.find_one({"mobile_number": {"$eq": mobileNumber}, "pin": {"$eq": userPin}}, {"_id": 0})
    output = json_util.dumps(response)
    print(output)

    if mobileNumber and userPin in output:
        return output
    else:
        return "incorrect"


@app.route("/get/profile", methods=["POST"])
def getProfile():
    data = mongo.db.wallet_user

    mobileNumber = request.json["mobile_number"]
    response = data.find_one({"mobile_number": {"$eq": mobileNumber}}, {"_id": 0})
    output = json_util.dumps(response)

    return output


@app.route("/reset/pin", methods=["POST"])
def resetPin():
    data = mongo.db.wallet_user

    mobileNumber = request.json["mobile_number"]
    nidNumber = request.json["nid_number"]
    userPin = request.json["pin"]

    myQuery = {"mobile_number": mobileNumber, "nid_number": nidNumber}
    newValues = {"$set": {"pin": userPin}}

    up_data = data.update_one(myQuery, newValues)

    output = json_util.dumps(up_data.modified_count)

    return output


@app.route("/transfer/balance", methods=["POST"])
def transferBalance():
    data = mongo.db.wallet_user

    receiverID = request.json["wallet_id"]
    sendAmount = request.json["amount"]

    up_data = data.update_one({"wallet_id": receiverID}, {"$inc": {"amount": sendAmount}})

    # existingStatus = data.find_one({"walletId": {"$eq": walletId}}, {"_id": 0})
    output = json_util.dumps(up_data.modified_count)

    return output


@app.route("/update/balance", methods=["POST"])
def updateBalance():
    data = mongo.db.wallet_user

    receiverID = request.json["wallet_id"]
    sendAmount = request.json["amount"]

    up_data = data.update_one({"wallet_id": receiverID}, {"$inc": {"amount": sendAmount}})

    # existingStatus = data.find_one({"walletId": {"$eq": walletId}}, {"_id": 0})
    output = json_util.dumps(up_data.modified_count)

    return output


@app.route("/transaction/record", methods=["POST"])
def transactionRecord():
    data = mongo.db.transaction_record

    uniqueID = request.json["unique_id"]
    dateTime = request.json["date_time"]
    receiverID = request.json["receiver_id"]
    amount = request.json["amount"]
    senderID = request.json["sender_id"]
    additionalData = request.json["additional_info"]
    status = request.json["status"]
    paymentType = request.json["payment_type"]

    createProfile = data.insert_one({"unique_id": uniqueID, "date_time": dateTime, "receiver_id": receiverID,
                                     "amount": amount, "sender_id": senderID, "additional_info": additionalData,
                                     "status": status, "payment_type": paymentType})
    # output = {'Status': 'Successfully Inserted', 'Document_ID': str(createProfile.inserted_id)}
    output = json_util.dumps(createProfile.inserted_id)

    return output


@app.route("/fetch/trx/record", methods=["POST"])
def fetchTransactionRecord():
    data = mongo.db.transaction_record

    senderID = request.json["sender_id"]

    query = {"$or": [{"sender_id": {"$eq": senderID}}, {"receiver_id": {"$eq": senderID}}]}
    response = data.find(query)
    output = json_util.dumps(response)

    return output


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
