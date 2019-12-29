import urllib.request, json, logging

logger = logging.getLogger("log")
base_url = "https://opentdb.com/api.php?"

def getQuestions(difficulty="",category="", number=10):
    amount = "amount=" + str(number)
    generated_url = base_url + amount
    if category != "":
        generated_url= generated_url + "&" + "category=" + category

    if difficulty != "":
        generated_url= generated_url + "&" + "difficulty=" + difficulty

    with urllib.request.urlopen(generated_url) as url:
        data = json.loads(url.read().decode())
        logger.info("Downloaded:" + str(data))

    return data