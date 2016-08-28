from app import app
import qrcode
import hashlib
import uuid
import json
import base64

fireHash = "https://roboq-7e9fe.firebaseio.com/empresafoo/hash.json"
fireQueue = "https://roboq-7e9fe.firebaseio.com/empresafoo/queue.json"

preped = False


@app.route('/auth_qr',methods=['POST'])
def authenticate_qr:
    if !preped:
        return str("must prep first"), 401
    if (validate_hash(request.args.get("qrhash"))):
        queue = requests.request("GET", fireQueue )
        requests.request("PUT", fireQueue, data={"queue": json.loads(queue)['queue']}+1 )
        update_hash_queue()
        return render_template('success.html')
    else:
        return render_template('fail.html')


def validate_hash(qrhash):
    response = requests.request("get", url, data=payload, headers=headers)
    if response.code == 200:
       return json.loads(response.text)['hash'] == qrhash
    else:
        return None
    
def get_hash():
    response = requests.request("get", url, data=payload, headers=headers)
    return json.loads(response.text)['hash']
        
        
    
def update_hash_queue:
    payload = {'hash':uuid.uuid4().hex}
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    response = requests.request("PUT", url, data=payload, headers=headers)

    
def gen_qr(string):
    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10,
                       border=4)
    qr.add_data(string)
    qr.make(fit=True)
    img = qr.make_image()
    return img

@app.route('/get_qrimg')
def get_qrimg():
    if !preped:
        return str("must prep first"), 401
    img_buf = cStringIO.StringIO()
    img = gen_qr(get_hash)
    img.save(img_buf)
    img_buf.seek(0)
    
    f = open(img)
    data = f.read()
    f.close()
    string = base64.b64encode(data)
    
    return string, 200


@app.route('/prepare'):
    requests.request("PUT", fireQueue, data={'queue':0} )
    update_hash_queue()
    preped = True
    return 200

@app.route("/")
def main():
    if !preped:
        return str("must prep first"), 401
    return render_template('index.html')

